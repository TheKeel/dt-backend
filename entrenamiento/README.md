# Entrenamiento — rack central `logica-matematica`

Lote 1: 53 PDF de ejercicios de lógica matemática con solución
(`entrenamiento/logica-matematica/`, origen: `/home/rafael/Downloads/kb`).

## Indexar

```bash
./entrenamiento/indexar.sh
# equivale a:
deeptutor kb add logica-matematica --docs-dir entrenamiento/logica-matematica
```

## Requisitos

- Embedding activo en Settings › Embedding models (lote 1: `Gemini/gemini-embedding-2`).
- El KB `logica-matematica` debe existir (`deeptutor kb list`); si no:
  `deeptutor kb create logica-matematica --doc <algun.pdf>` y luego el comando de arriba.

## Notas

- Solo PDF con texto. Los 30 `.doc` del lote original son escaneos sin capa
  de texto y se excluyen hasta pasarles OCR (`tesseract -l spa`).
- `pagina29` estaba duplicada (doc+pdf): se conserva el PDF.
- El índice vive en `data/` (gitignored); aquí solo fuentes + comando.
