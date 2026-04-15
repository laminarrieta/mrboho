"""
MR.BOHO - Descargador de imágenes de productos
==============================================
Descarga todas las imágenes de la colección "gafas-de-sol" de mrboho.com
usando la API JSON pública de Shopify.

Nombre de archivo: {nombre_producto}_{numero}.ext
Ejemplo: TREAT - FRELARD_1.png, TREAT - FRELARD_2.png
"""

import os
import re
import time
import requests
from pathlib import Path

# ─── Configuración ────────────────────────────────────────────────────────────
BASE_URL    = "https://www.mrboho.com"
COLLECTION  = "gafas-de-sol"
OUTPUT_DIR  = Path("imagenes_productos")
LIMIT       = 250          # máximo permitido por Shopify por página
DELAY_SEC   = 0.3          # pausa entre descargas para no sobrecargar el servidor
TIMEOUT_SEC = 30
# ──────────────────────────────────────────────────────────────────────────────


def sanitize_filename(name: str) -> str:
    """Convierte el nombre del producto en un nombre de archivo seguro."""
    # Reemplaza caracteres no permitidos en nombres de archivo
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*]', '', name)   # elimina caracteres ilegales
    name = re.sub(r'\s+', ' ', name)            # colapsa espacios múltiples
    return name


def get_extension(url: str) -> str:
    """Extrae la extensión del archivo de la URL, sin parámetros de query."""
    path = url.split("?")[0]  # quita parámetros ?v=…
    ext = os.path.splitext(path)[-1].lower()
    return ext if ext in (".jpg", ".jpeg", ".png", ".webp", ".gif") else ".jpg"


def fetch_products() -> list:
    """Obtiene todos los productos de la primera página vía la API JSON de Shopify."""
    url = f"{BASE_URL}/collections/{COLLECTION}/products.json"
    params = {"limit": LIMIT}

    print(f"📡 Consultando API: {url}")
    response = requests.get(url, params=params, timeout=TIMEOUT_SEC)
    response.raise_for_status()

    products = response.json().get("products", [])
    print(f"✅ {len(products)} productos encontrados.\n")
    return products


def download_image(url: str, dest_path: Path) -> bool:
    """Descarga una imagen desde una URL y la guarda en dest_path."""
    try:
        response = requests.get(url, timeout=TIMEOUT_SEC, stream=True)
        response.raise_for_status()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.RequestException as e:
        print(f"    ⚠️  Error descargando {url}: {e}")
        return False


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    products = fetch_products()

    total_images = 0
    failed_images = 0

    for product in products:
        title      = product.get("title", "sin_nombre")
        images     = product.get("images", [])
        safe_title = sanitize_filename(title)

        if not images:
            print(f"  ⚪ [{safe_title}] — sin imágenes, omitido.")
            continue

        print(f"📦 {safe_title}  ({len(images)} imagen{'es' if len(images) != 1 else ''})")

        for idx, image in enumerate(images, start=1):
            src = image.get("src", "")
            if not src:
                continue

            ext       = get_extension(src)
            filename  = f"{safe_title}_{idx}{ext}"
            dest_path = OUTPUT_DIR / filename

            # Evita re-descargar si ya existe
            if dest_path.exists():
                print(f"    ✔  {filename} (ya existe, omitido)")
                total_images += 1
                continue

            success = download_image(src, dest_path)
            if success:
                size_kb = dest_path.stat().st_size / 1024
                print(f"    ✔  {filename}  ({size_kb:.1f} KB)")
                total_images += 1
            else:
                failed_images += 1

            time.sleep(DELAY_SEC)

    print(f"\n{'─'*55}")
    print(f"✅ Descarga completada.")
    print(f"   Imágenes guardadas : {total_images}")
    print(f"   Errores            : {failed_images}")
    print(f"   Carpeta            : {OUTPUT_DIR.resolve()}")
    print(f"{'─'*55}")


if __name__ == "__main__":
    main()
