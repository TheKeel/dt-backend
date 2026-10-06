# Visuales de fuente en KBs
Guarda imágenes extraídas de PDF/EPUB para que el modelo las vea.
## Uso

- Parser emite PNG/JPEG/GIF/WebP → `visual_assets/` (fuera del índice). Servir: `/api/knowledge-bases/{kb}/visual-assets/{id}`. Borrar fuente borra sus assets.
- `rag` recupera por caption/contexto: modelo con visión recibe píxeles, solo-texto recibe caption + aviso.
- Límites: 64 imgs/doc, 5 MiB c/u, 2 por respuesta.

<details>
<summary>Parsers</summary>

MinerU: figuras PDF sí. PyMuPDF4LLM: PDF/EPUB sí, sin page boxes. Texto default y Docling: no. Dibujos vectoriales u OCR sin motor: ausente. Otros providers RAG: aún no.
</details>
