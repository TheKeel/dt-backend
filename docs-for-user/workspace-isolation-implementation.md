# Workspace isolation — nota de auditoría

Auditoría 2026-09-19, instancia local. No uso diario. Canónico: `workspaces.md`.

- Contrato: chat/libros/mastery/reading/watching aíslan materiales, sesiones, progreso, quizzes, archivos, cachés por workspace. Global: memoria, credenciales, settings, registro.
- Default conserva rutas históricas; custom vive en `.deeptutor/data/` + `outputs/`.
- Límites: migración = traslado agregado, no merge (ID en conflicto = rechazo). Formatos viejos = archivo, no auto-lectura. Partición a nivel app, no sandbox.

<details><summary>Evidencia (resumen)</summary>

- 94 borde + 45 CLI/app + 17 migración/HTTP pasaron. Browser QA aislado OK (historial cruzado, draft restore, ZIP 14 entradas).
- Backup privado SHA-256: `DeepTutor-backups/workspace-isolation-20260919-023534/`. Artefactos: `output/playwright/workspace-*.png`.

</details>
