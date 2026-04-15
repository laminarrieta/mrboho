# MR.BOHO — Descargador de imágenes de productos

Descarga automáticamente todas las imágenes de la colección **Gafas de Sol** de [mrboho.com](https://www.mrboho.com/collections/gafas-de-sol).

Las imágenes se nombran como:
```
{Nombre del producto}_{número}.ext
Ejemplo: TREAT - FRELARD_1.png
         TREAT - FRELARD_2.png
         HONEY - JORDAAN_1.png
```

---

## Opción A — Ejecutar desde GitHub Actions (recomendado)

1. Sube este repositorio a tu cuenta de GitHub.
2. Ve a la pestaña **Actions** del repositorio.
3. Selecciona el workflow **"Descargar imágenes MR.BOHO"**.
4. Pulsa **"Run workflow"** → **"Run workflow"**.
5. Espera a que termine (≈ 1-2 minutos).
6. Descarga el artefacto **`imagenes-gafas-de-sol.zip`** desde la sección *Artifacts* de la ejecución.

---

## Opción B — Ejecutar en local

```bash
# 1. Clona el repositorio
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd TU_REPO

# 2. Instala dependencias (solo requests)
pip install requests

# 3. Ejecuta el script
python download_images.py
```

Las imágenes se guardarán en la carpeta `imagenes_productos/`.

---

## Estructura del proyecto

```
.
├── download_images.py              # Script principal
├── .github/
│   └── workflows/
│       └── download_images.yml    # Workflow de GitHub Actions
└── README.md
```
