# DeepTutor Containerization

Imagen `ghcr.io/hkuds/deeptutor:latest`: backend (`:8001`) + frontend (`:3782`) en un contenedor. Datos en `/app/data`.

## Uso core

```bash
docker run --rm --name deeptutor \
  -p 127.0.0.1:3782:3782 \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest
# abrir http://127.0.0.1:3782
```

```bash
cp .env.example .env
podman compose -f compose.yaml up -d   # hardened: rootless + read-only rootfs
```

Config: edita `data/user/settings/*.json`, reinicia. No uses env vars para eso. `.env` del proyecto se ignora.

| Archivo | Para qué |
|---|---|
| `system.json` | puertos, API base, CORS |
| `auth.json` | auth on/off, usuario/pass |
| `integrations.json` | PocketBase/sidecars |
| `model_catalog.json` | providers, keys, modelos |

<details>
<summary>Resto: workspace, Unraid, Codex OAuth, proxy, LLM host, podman run, PocketBase, troubleshooting, seguridad</summary>

**Workspace contenido separado:**
```bash
mkdir -p "$PWD/deeptutor-workspace/outputs"
docker run --rm --name deeptutor \
  -p 127.0.0.1:3782:3782 \
  -v deeptutor-data:/app/data \
  -v "$PWD/deeptutor-workspace:/workspace" \
  -e DEEPTUTOR_WORKSPACE_ROOT=/workspace \
  -e DEEPTUTOR_WORKSPACE_ALLOWED_ROOTS=/workspace \
  ghcr.io/hkuds/deeptutor:latest
```
Solo `3782` necesita `-p`. `:8001` solo para curl/debug.

**Unraid/NAS (dueño ≠ UID 1000):**
```bash
docker run --rm --name deeptutor \
  -e PUID=99 -e PGID=100 \
  -p 127.0.0.1:3782:3782 \
  -v /mnt/user/appdata/deeptutor:/app/data \
  ghcr.io/hkuds/deeptutor:latest
```
Sin `chown` manual. `PUID=0` rechazado.

**Codex OAuth (puertos 1455/1457 loopback, solo durante login):**
```bash
docker run --rm --name deeptutor \
  -p 127.0.0.1:3782:3782 \
  -p 127.0.0.1:1455:3782 -p 127.0.0.1:1457:3782 \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest
# Settings → Models → OpenAI Codex → Sign in. Luego vuelve al comando normal.
# Compose: añade `-f compose.codex-oauth.yaml up -d --force-recreate deeptutor`, luego quítalo.
```

**Migración `docker-compose.ghcr.yml`:** ahora monta todo `./data`. Antes de recrear, copia estado o pierdes auth/cuentas:
```bash
for tree in system users partners cli-apps; do
  docker cp "deeptutor:/app/data/$tree" "./data/$tree" 2>/dev/null || true
done
```

**Reverse proxy:** apunta a `:3782`, nada más. Solo split-backend necesita `system.json → next_public_api_base` (ej. `http://backend:8001`). CORS: orígenes frontend exactos en `cors_origins` si auth on.

**LLM en host (Ollama/LM Studio/etc):** `localhost` = contenedor. Usa gateway:
```bash
docker run --rm --name deeptutor \
  -p 127.0.0.1:3782:3782 \
  --add-host=host.docker.internal:host-gateway \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest
```
URLs: Ollama `http://host.docker.internal:11434/v1`, LM Studio `:1234/v1`, llama.cpp `:8080/v1`, Lemonade `:13305/api/v1`. Alternativa Linux: `--network=host` + `BACKEND_HOST=FRONTEND_HOST=127.0.0.1`.

**Podman manual:**
```bash
mkdir -p data/user/settings && echo '{}' > data/user/settings/system.json
podman run --rm -d --name deeptutor \
  -p 127.0.0.1:8001:8001 -p 127.0.0.1:3782:3782 \
  -v $(pwd)/data:/app/data:U --read-only \
  --tmpfs /tmp:size=512m,mode=1777 --tmpfs /run:size=32m,mode=0755 \
  --tmpfs /var/run:size=8m,mode=0755 --tmpfs /var/log:size=64m,mode=0755 \
  --tmpfs /root:size=16m,mode=0700 --tmpfs /home:size=16m,mode=0755 \
  --userns=keep-id ghcr.io/hkuds/deeptutor:latest
```
App corre como `deeptutor` (UID 1000). Pidfile en `/tmp/supervisord.pid`.

**PocketBase (opcional):** `integrations.json → pocketbase_url: http://pocketbase:8090`, levanta servicio `pocketbase`. Monta `/pb_data /pb_public /pb_hooks`.

**Troubleshooting:**
- `Backend unreachable` → backend no arrancó (`docker logs`), no falta `-p 8001`.
- `Cannot connect to Docker daemon` en podman → `systemctl --user start podman.socket` o `DOCKER_HOST=...podman.sock`.
- `Permission denied` volumen → bind mount propio, no named volume; o `:U`.
- `Knowledge base not initialized` en Unraid → fija `PUID/PGID`, no corras como root.

**Seguridad:** app non-root; `read_only + tmpfs` = rootfs inmutable; `userns keep-id` = escape sin root; sandbox-runner solo en `docker-compose.yml`; auth vía `auth.json` + cookie `dt_token`.

</details>
