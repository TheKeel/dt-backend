# Knowledge migration guide

Mueve notas Obsidian/Hermes/Markdown a DeepTutor (v1.6.0 Knowledge Center).

| Ruta | Qué hace | Cuándo |
|---|---|---|
| Conectar vault Obsidian | puntero vivo, sin índice RAG | sigues editando en Obsidian |
| Importar KB indexada | copia a `raw/` + índice | quieres búsqueda semántica |

Sin importador Hermes: exporta a Markdown y usa ruta importar.

## Uso core

**Conectar Obsidian:** Knowledge Center → Create KB → Link existing → Obsidian → path absoluto visible por el servidor (en contenedor: path dentro del contenedor, monta vault primero). Solo puntero; borrar KB no toca vault.

**Importar (web):** Create KB → Create new → sube archivos/carpeta/`.zip` → espera indexado → verifica antes de borrar backup. Carpeta preserva estructura; `.zip` aplana y salta duplicados/ocultos.

**Importar (CLI):**
```bash
deeptutor kb create hermes-notes --docs-dir /path/to/hermes-export
deeptutor kb add hermes-notes --docs-dir /path/to/more-notes
deeptutor kb list && deeptutor kb info hermes-notes
```
CLI aplana a `raw/` (duplicados se pisan). Si hay nombres repetidos o jerarquía, usa subida web.

<details>
<summary>Resto: preparación, reglas, verificación</summary>

- Backup completo antes de migrar. Exporta `.md`/`.markdown` + assets. HTML → convierte a Markdown fuera y verifica links.
- Obsidian: ignora `.obsidian/.trash/.git`; sigue links/tags; escritura solo aditiva (crear/append/frontmatter, no borra ni reescribe).
- Extensiones Markdown: `.md`, `.markdown` (+ texto/docs/sheets/slides/EPUB/imagen/código según UI).
- Verifica: abre muestra pequeña/mediana/anidada; busca nombre exacto, frase y concepto; en Obsidian prueba link + crear/borrar scratch note. Guarda backup hasta confirmar.
</details>
