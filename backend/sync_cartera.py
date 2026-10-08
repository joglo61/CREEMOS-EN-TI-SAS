#!/usr/bin/env python
"""
CLI para sincronización de cartera entre Excel y base SQLite.

Uso:
    python sync_cartera.py [--dry-run] [--creemos RUTA]
"""
import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.cartera.sincronizador import SincronizadorCartera


def main():
    parser = argparse.ArgumentParser(description="Sincronizar cartera Excel ↔ SQLite")
    parser.add_argument("--dry-run", action="store_true", help="Solo mostrar qué se haría, sin escribir")
    parser.add_argument("--creemos", default=None, help="Ruta al archivo Creemos.xlsx")
    parser.add_argument("--db", default=None, help="Ruta a la base de datos cartera.db")
    args = parser.parse_args()

    sync = SincronizadorCartera(
        ruta_creemos=args.creemos,
        db_path=args.db,
        dry_run=args.dry_run,
    )

    resultado = sync.ejecutar()

    for nivel, msg in sync.log:
        prefix = {"info": "  ", "warning": "  [!]", "error": "  [X]"}.get(nivel, "  ")
        print(f"{prefix} {msg}")

    if resultado["status"] == "ok":
        print(f"\n✅ Sincronización exitosa: {resultado['creditos']} créditos, "
              f"{resultado['pagos']} pagos, {resultado['snapshots']} snapshots")
    elif resultado["status"] == "dry_run":
        print("\n🔷 Dry-run completado. No se escribió nada.")
    else:
        print(f"\n❌ Error: {resultado.get('error')}")


if __name__ == "__main__":
    main()
