import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.database.database import engine, Base, SessionLocal
from app.models import *  # noqa: F401, F403
from app.api.auth import router as auth_router
from app.api.clientes import router as clientes_router
from app.api.prestamos import router as prestamos_router
from app.api.pagos import router as pagos_router
from app.api.facturas import router as facturas_router
from app.api.dashboard import router as dashboard_router
from app.api.excel import exportar_todo
from app.api.configuracion import router as config_router
from app.api.usuarios import router as usuarios_router
from app.api.backups import router as backups_router
from app.api.reportes import router as reportes_router

os.makedirs(settings.LOGS_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        RotatingFileHandler(os.path.join(settings.LOGS_DIR, "app.log"), maxBytes=5_000_000, backupCount=5, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def create_directories():
    os.makedirs(settings.BACKUP_DIR, exist_ok=True)
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    os.makedirs(settings.RECIBOS_DIR, exist_ok=True)
    os.makedirs(settings.LOGS_DIR, exist_ok=True)
    os.makedirs("./database", exist_ok=True)


def create_tables():
    Base.metadata.create_all(bind=engine)
    # create_all no agrega columnas a tablas existentes (Alembic no se usa en la BD real)
    from sqlalchemy import inspect, text
    columnas = {c["name"] for c in inspect(engine).get_columns("prestamos")}
    if "placa" not in columnas:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE prestamos ADD COLUMN placa VARCHAR(20)"))
            conn.execute(text("UPDATE prestamos SET placa = (SELECT placa FROM clientes WHERE clientes.id = prestamos.cliente_id)"))


def seed_initial_data():
    from app.repositories.usuario_repository import UsuarioRepository
    from app.security.auth import hash_password
    from app.models.usuario import Usuario
    from app.models.configuracion import Configuracion

    db = SessionLocal()
    try:
        usuario_repo = UsuarioRepository(db)
        admin = usuario_repo.get_by_usuario("jugarciamar")
        if not admin:
            import secrets
            admin_pass = settings.DEFAULT_ADMIN_PASSWORD or secrets.token_urlsafe(12)
            admin_user = Usuario(
                nombre="Administrador",
                usuario="jugarciamar",
                password_hash=hash_password(admin_pass),
                rol="ADMINISTRADOR",
                activo=True,
            )
            usuario_repo.create(admin_user)
            if settings.DEFAULT_ADMIN_PASSWORD:
                logger.warning("Usuario admin creado con DEFAULT_ADMIN_PASSWORD.")
            else:
                # Sin contraseña configurada: se muestra solo por consola (no en app.log).
                print(f"Contraseña inicial del admin (cámbiela): {admin_pass}", flush=True)

        config = db.query(Configuracion).first()
        if not config:
            config_data = Configuracion(
                empresa="CREEMOS EN TI SAS",
                nit="",
                direccion="",
                telefono="",
                tasa_interes=2.5,
                dias_gracia=5,
                siguiente_factura=1,
                ruta_recibos=settings.RECIBOS_DIR,
                ruta_backups=settings.BACKUP_DIR,
            )
            db.add(config_data)
            db.commit()
    finally:
        db.close()


def create_app() -> FastAPI:
    create_directories()
    create_tables()
    seed_initial_data()

    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.ENABLE_DOCS else None,
        redoc_url="/redoc" if settings.ENABLE_DOCS else None,
        openapi_url="/openapi.json" if settings.ENABLE_DOCS else None,
    )

    origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins if origins else ["*"],
        allow_credentials=bool(origins),
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled error on {request.method} {request.url.path}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor. Contacte al administrador."},
        )

    # El sistema es la fuente de verdad: el arranque ya no sincroniza ni escribe Creemos.xlsx
    # (migración única: backend/migrar_excel.py).

    app.include_router(auth_router)
    app.include_router(clientes_router)
    app.include_router(prestamos_router)
    app.include_router(pagos_router)
    app.include_router(facturas_router)
    app.include_router(dashboard_router)
    # Del módulo Excel solo queda el respaldo completo (clientes, préstamos, pagos, facturas)
    app.add_api_route("/api/v1/excel/exportar-todo", exportar_todo, methods=["GET"], tags=["Excel"])
    app.include_router(config_router)
    app.include_router(usuarios_router)
    app.include_router(backups_router)
    app.include_router(reportes_router)

    @app.get("/")
    def root():
        frontend_index = frontend_dist / "index.html"
        if frontend_dist.is_dir() and frontend_index.is_file():
            return FileResponse(str(frontend_index))
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running",
        }

    @app.get("/health")
    def health():
        return {"status": "ok"}

    frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
    if frontend_dist.is_dir():
        app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

        @app.get("/{full_path:path}")
        def serve_spa(full_path: str):
            if full_path.startswith("api/"):
                return JSONResponse(status_code=404, content={"detail": "Not Found"})
            file_path = (frontend_dist / full_path).resolve()
            if file_path.is_file() and file_path.is_relative_to(frontend_dist.resolve()):
                return FileResponse(str(file_path))
            return FileResponse(str(frontend_dist / "index.html"))

    return app


app = create_app()
