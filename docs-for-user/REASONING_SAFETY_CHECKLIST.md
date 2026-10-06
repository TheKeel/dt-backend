# Reasoning safety checklist
Diagnostica respuestas poco fiables: prompt, retrieval, contexto o bug.
## Uso
1. Qué pidió y qué restricciones valen? 2. Qué capability/tools/llamadas?
3. En qué fuente se basó (KB, adjunto, libro, web)? 4. Citó evidencia o solo sonó autoritario?
5. Ignoró/mezcló turnos? 6. Dijo qué no sabe?

## Fallos

- Olvida restricciones: restate en turno nuevo y compara.
- Drift: reintenta una sola fuente; revisa chunk IDs.
- Overconfidence sin cita: pide pasaje exacto; retry evidence-only.
- No grounded: verifica locator y versión fuente.

<details>
<summary>Resto patrones retrieval (16)</summary>

No retrieval, wrong scope, stale source, chunk split, near-topic drift, keyword mismatch, translation mismatch, duplicados, top-k amplio, sin rerank, fuentes en conflicto, web sin verificar, citation mismatch, locator mismatch, resultado vacío/filtrado, evidencia alucinada.
</details>

## Reporte

- Versión, SO, capability, modelo. Fuentes, tools, citation IDs.
- Request/respuesta sin personales, logs sin keys.
- Ya probé: retry, una fuente, rebuild índice, restate.

<details>
<summary>Template issue</summary>

```markdown
Capability: / Model: / Versión:
Pidió: / Respondió: / Por qué falla:
Fuentes: / Tools: / Citas:
Pasos: / Esperado: / Actual: / Ya probé:
```
</details>
