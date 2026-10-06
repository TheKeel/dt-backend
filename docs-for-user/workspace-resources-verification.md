# Workspace resources — nota de verificación

Verificado 2026-09-19, árbol local. No uso diario. Canónico: `workspaces.md`.

- Regla: null = hereda; lista vacía = desactiva ese tipo. Sin política = reglas viejas, nada se mueve.
- Workspace solo restringe (MCP/KB/skills), nunca amplía grants admin ni toca credenciales.

<details><summary>Evidencia (resumen)</summary>

- 153 + 143 + 25 tests backend, 24 frontend, typecheck/lint/contract/locale/build OK.
- Suite Node completa: 1150 OK / 34 fallos ajenos (URLs viejas sin `dt_workspace`, etc.), no cuentan como validación.

</details>
