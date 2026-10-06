# Hermes remoto

Llama gateway Hermes sin CLI local. Backend `hermes_remote`.

## Uso

`subagent.json` > `backends.hermes_remote`:

- `enabled`, `base_url` (ej `http://hermes-uni:8642`), `profile` (solo label).
- `api_key_env` (default `DEEPTUTOR_HERMES_REMOTE_API_KEY`, solo env, nunca en settings/GET).
- `model`, `effort`, `system_prompt`, `auto_approve`, `idle_timeout_seconds` (default 600).
- URL solo HTTP(S), sin credenciales/query. Prefijo opcional `/p/<profile>`. Sin redirects.

## Endpoints

1. `GET /v1/capabilities` — chequea gateway. Errores: `not_configured key_missing unreachable unauthorized incompatible`.
2. `POST /v1/runs` — inicia (`input`, `instructions`, `model`, `reasoning_effort`, `session_id`). 202 `{run_id, started}`. Resume: trae últimos 40 msgs user/assistant (404 = sesión muerta, arranca fresh).
3. `GET /v1/runs/{id}/events` (SSE) — `message.delta`, `tool.started/completed`, `reasoning.available`, `approval.request`, `run.completed/failed/cancelled`.
4. `POST /v1/runs/{id}/approval` — `{"choice":"once"}` o `"deny"`. Fallo = stop run.
5. `POST /v1/runs/{id}/stop` — cancela. Cancel/timeout siempre intenta stop acotado.

<details>
<summary>Detalles resto</summary>

- Sesión: header `X-Hermes-Session-Id` + field `session_id` + compat `X-Hermes-Session`. `system_prompt` solo en sesión fresh o 404.
- Cada request lleva `CONSULT_ORIGIN_INSTRUCTION` anti-recursión.
- Sin upload imágenes: adjuntos locales no se envían.
- Tools corren en gateway, no en DeepTutor. Un session id por chat, no compartir. No meter `API_SERVER_KEY` ni API key en logs/payloads.
- Contrato full: [Hermes API Server](https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server/).
</details>
