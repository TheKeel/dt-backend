# Immersive Watching workspace

Watching = video + conversación con marcas de tiempo. Concepto workspace: ver `workspaces.md` (canónico).

- Uso: sidebar **Immersive Watching** o `/watching` → pega YouTube URL → pregunta → se guarda en `/watching/{sessionId}`.
- Click caption / Explain here / nota con timestamp → salta al punto del video.

<details><summary>Invidious (admin)</summary>

- Settings admin → video-learning: `invidious.api_base_url` (alcanzable por backend), `invidious.public_base_url` (alcanzable por navegador), `default_provider: invidious|youtube`. No va en `.env`.
- Sin cuenta funciona (búsqueda). Conectar cuenta = feed subs + playlists (scopes `GET:feed`, `GET:playlists`, `GET:playlists/*`). Nunca pide password; revocar reintenta.
- Falla visible; a YouTube solo por acción explícita. Sin captions → Retry, no sustitución silenciosa.

</details>
