# Despliegue web en VPS — CREEMOS EN TI SAS

Arquitectura: VPS Linux → Docker Compose → **Caddy** (HTTPS automático) → **app** (FastAPI sirve API + frontend compilado). SQLite y `Creemos.xlsx` viven en `datos/` del servidor (volúmenes). Un solo worker.

## 1. Comprar dominio y VPS
- Dominio: Cloudflare Registrar o Namecheap (~USD 10/año).
- VPS: Ubuntu 24.04, 2 GB RAM, 1 vCPU (Hetzner CX22 / DigitalOcean / Contabo).
- DNS: registro **A** `@` (o `app`) → IP del VPS. Si usa Cloudflare, déjelo en "DNS only" (nube gris) hasta que Caddy obtenga el certificado.

## 2. Preparar el servidor (una vez)
```bash
adduser deploy && usermod -aG sudo deploy        # usuario no-root
# copiar su llave SSH: ssh-copy-id deploy@IP  (desde su PC)
sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/; s/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config && sudo systemctl restart ssh
sudo apt update && sudo apt install -y ufw fail2ban unattended-upgrades rclone
sudo ufw allow OpenSSH && sudo ufw allow 80 && sudo ufw allow 443 && sudo ufw enable
curl -fsSL https://get.docker.com | sudo sh && sudo usermod -aG docker deploy
sudo timedatectl set-timezone America/Bogota
```

## 3. Subir código y datos
```bash
sudo mkdir -p /opt/creemos && sudo chown deploy /opt/creemos
git clone <repo> /opt/creemos      # o scp del proyecto (sin datos)
cd /opt/creemos
mkdir -p datos/{database,backups,data,recibos,logs}
```
Desde el PC de la oficina (cerrar Excel y detener la app local primero):
```bash
scp backend/database/prestamos.db backend/database/cartera.db deploy@IP:/opt/creemos/datos/database/
scp Creemos.xlsx deploy@IP:/opt/creemos/datos/
scp -r backend/recibos/* deploy@IP:/opt/creemos/datos/recibos/
```
En el servidor: `sudo chown -R 1000:1000 datos` (el contenedor corre con uid 1000).

## 4. Configurar
```bash
cp backend/.env.example backend/.env && nano backend/.env
echo "DOMINIO=app.su-dominio.com" > .env
```
En `backend/.env` de producción:
- `SECRET_KEY` nuevo: `python3 -c "import secrets; print(secrets.token_urlsafe(48))"` (**no reutilizar el del PC**).
- `CORS_ORIGINS=https://app.su-dominio.com`
- `ENABLE_DOCS=false`
- `AUTO_EXCEL_ON_STARTUP=false` (un reinicio no reescribe `Creemos.xlsx`; el bloque mensual se crea con "Actualizar Excel").
- `DEFAULT_ADMIN_PASSWORD` solo aplica si la BD no tiene al admin. Como se copia la BD existente, **cambie la contraseña del admin desde la app** tras el primer ingreso si la anterior estuvo en el `.env` del PC.

## 5. Levantar
```bash
docker compose up -d --build
docker compose logs -f app      # verificar arranque
curl https://app.su-dominio.com/health
```

## 6. Backups y monitoreo
```bash
chmod +x scripts/backup.sh && ./scripts/backup.sh      # probar
crontab -e
# 0 2 * * * RCLONE_DEST=gdrive:creemos-backups /opt/creemos/scripts/backup.sh >> /opt/creemos/datos/logs/backup.log 2>&1
```
- Copia externa: `rclone config` (Google Drive) y definir `RCLONE_DEST` como arriba.
- **Probar una restauración** al menos una vez (ver §8).
- Monitoreo: UptimeRobot (gratis) → `https://app.su-dominio.com/health`, alerta por email.

## 7. Actualizar a una nueva versión
```bash
cd /opt/creemos && ./scripts/backup.sh && git pull && docker compose up -d --build
```
Rollback: `git checkout <commit-anterior> && docker compose up -d --build`; si hubo daño en datos, restaurar §8.

## 8. Restaurar un backup
```bash
docker compose stop app
cp datos/backups/diario/<FECHA>/prestamos.db datos/backups/diario/<FECHA>/cartera.db datos/database/
cp datos/backups/diario/<FECHA>/Creemos.xlsx datos/
docker compose start app
```

## Flujo del Excel durante la transición
- El servidor **no recalcula fórmulas** (no hay Excel en Linux). Se recalculan al abrir el archivo en Excel.
- Para editar a mano: descargar `Creemos.xlsx` desde la app → editar en Excel → volver a subirlo (tipo "cartera") en la app. La subida sincroniza `cartera.db` y el sistema.
- Para que el Excel refleje los pagos del sistema: botón **"Actualizar Excel"** y luego descargar.
- Evitar editar el Excel descargado mientras otros registran pagos en la app; la última subida sobrescribe el archivo (queda copia en `datos/data/backup_Creemos.xlsx`).
