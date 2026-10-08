#!/usr/bin/env bash
# Backup diario: copia consistente de ambas BD + Creemos.xlsx + recibos.
# Cron (como el usuario que corre docker):  0 2 * * * /opt/creemos/scripts/backup.sh >> /opt/creemos/datos/logs/backup.log 2>&1
# Copia externa opcional: definir RCLONE_DEST (p. ej. "gdrive:creemos-backups") tras configurar `rclone config`.
set -euo pipefail
cd "$(dirname "$0")/.."

STAMP=$(date +%Y%m%d_%H%M)
DEST="datos/backups/diario/$STAMP"
mkdir -p "$DEST"

# sqlite3 .backup vía Python dentro del contenedor (seguro con la app corriendo)
docker compose exec -T app python - "$STAMP" <<'PY'
import sqlite3, sys
for nombre in ("prestamos.db", "cartera.db"):
    src = sqlite3.connect(f"database/{nombre}")
    dst = sqlite3.connect(f"backups/diario/{sys.argv[1]}/{nombre}")
    src.backup(dst)
    dst.close(); src.close()
PY

cp datos/Creemos.xlsx "$DEST/"
tar -czf "$DEST/recibos.tar.gz" -C datos recibos

# Retención local: 30 días
find datos/backups/diario -mindepth 1 -maxdepth 1 -type d -mtime +30 -exec rm -rf {} +

if [ -n "${RCLONE_DEST:-}" ]; then
  rclone copy "$DEST" "$RCLONE_DEST/$STAMP"
  rclone delete --min-age 90d "$RCLONE_DEST"
fi
echo "Backup OK: $DEST"
