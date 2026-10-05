# DeepTutor Backend

Backend agent-native: turnos durables, Tools nivel 1 + Capabilities nivel 2.

```
CLI (Typer) | WebSocket `/ws` | SDK Python
              ↓
`TurnApplicationService`: persiste, coordina, replay turnos
              ↓
`TurnEngine` → `ChatOrchestrator`: `UnifiedContext` → Capability (`chat` defecto)
              ↓
`ToolRegistry` (Nivel 1) | `CapabilityRegistry` (Nivel 2)
```

Cada ejecución usa `StreamBus` por turno. Orquestador emite eventos, runtime persiste, adaptadores replay. Settings en `data/user/settings/*.json`. `.env` raíz ignorado.

## Entry points

| Vía | Código | Uso |
|---|---|---|
| CLI | `deeptutor_cli/main.py` | `deeptutor run`, `deeptutor chat`, `deeptutor kb`, `deeptutor serve`, `deeptutor start` |
| WebSocket | `deeptutor/api/routers/unified_ws.py` | endpoint unificado `/ws`, contratos en `deeptutor/api/contracts/` |
| SDK | `deeptutor/app.py` | fachada `DeepTutorApp` |

## Nivel 1 — Tools

Función única invocada por LLM. Toggleables en `/settings/tools`, lista autoritativa `USER_TOGGLEABLE_TOOL_NAMES` en `deeptutor/tools/builtin/__init__.py`:

`brainstorm`, `web_search`, `paper_search`, `reason`, `geogebra_analysis`, `imagegen`, `videogen`

Resto context-gated o capability-owned. `CONFIGURABLE_BUILTIN_TOOL_NAMES` declara superficie configurable. `deeptutor/agents/_shared/tool_composition.py` define montaje (`ToolMountFlags`) + workspace tools siempre disponibles. Incluye `rag`, memoria, notebook, `read_skill`, MCP/CLI diferidos, `exec`, `ask_user`, navegación mastery. `--tool` filtra whitelist toggleable, no salta gates.

## Nivel 2 — Capabilities

Pipeline multi-etapa dueño del turno. Registro en `deeptutor/runtime/bootstrap/builtin_capabilities.py`. Convergen en `emit_capability_result()` en `deeptutor/capabilities/_shared.py`: payload + `cost_summary` desde `UsageTracker`. Prompts i18n en `capabilities/prompts/{en,zh}/<name>.yaml`.

| Capability | Etapas |
|---|---|
| `chat` | exploring → responding, loop agéntico único, defecto |
| `ask_questions` | responding vía `ask_user` forzado |
| `deep_solve` | responding + solve planning tools |
| `deep_question` | ideation → generation |
| `deep_research` | rephrasing → decomposing → researching → reporting |
| `visualize` | analyzing → generating → reviewing (`SVG`/`Chart.js`/`Mermaid`/`HTML`, o Manim vía `render_type`) |
| `math_animator` | concept_analysis → concept_design → code_generation → code_retry → summary → render_output |
| `mastery_path` | responding + mastery tools, gate por tipo tema |
| `immersive_reading` | responding grounding documento |
| `course_study` | responding sensing estado curso + hand-off |
| `immersive_watching` | responding grounding timestamps video |

## Archivos clave

| Path | Propósito |
|---|---|
| `deeptutor/runtime/orchestrator.py` | `ChatOrchestrator`, entrada unificada |
| `deeptutor/runtime/turn_engine.py` | motor turnos |
| `deeptutor/runtime/stream_bus.py` | fan-out async por turno |
| `deeptutor/runtime/launcher.py` | ciclo vida backend + puertos |
| `deeptutor/runtime/registry/` | `tool_registry.py`, `capability_registry.py`, `deferred_tools.py` |
| `deeptutor/runtime/bootstrap/builtin_capabilities.py` | paths capabilities built-in |
| `deeptutor/services/config/runtime_settings.py` | settings JSON + overrides env |
| `deeptutor/services/subagent/` | conectores agentes, registro en `registry.py`, modelos en `models.py` |
| `deeptutor/core/stream.py` | protocolo `StreamEvent` |
| `deeptutor/core/tool_protocol.py` | `BaseTool` + `ToolDefinition` |
| `deeptutor/core/capability_protocol.py` | `TurnCapability` + `CapabilityManifest` |
| `deeptutor/core/context.py` | dataclass `UnifiedContext` |
| `deeptutor/tools/builtin/__init__.py` | wrappers built-in |
| `deeptutor/capabilities/` | implementaciones built-in |
| `deeptutor/app.py` | fachada SDK |
| `deeptutor_cli/main.py` | entry Typer |
| `deeptutor/api/routers/unified_ws.py` | endpoint WS unificado |

## Config

Home runtime: directorio lanzamiento o `DEEPTUTOR_HOME` / `deeptutor start --home`. Estado privado en `data/` dentro del home.

| File | Propósito |
|---|---|
| `data/user/settings/model_catalog.json` | providers, perfiles LLM/task/embedding/search/TTS/STT/image/video |
| `data/user/settings/system.json` | puertos, API base, CORS, SSL, uploads, sandbox |
| `data/user/settings/auth.json` | toggle auth, hash, token/cookie |
| `data/user/settings/integrations.json` | PocketBase, sidecars |
| `data/user/settings/interface.json` | idioma, tema |
| `data/user/settings/document_parsing.json` | motor parsing, endpoints |
| `data/user/settings/video_learning.json` | provider YouTube/Invidious, transcripts |
| `main.yaml` | defaults runtime |
| `agents.yaml` | temperatura/tokens capability/tool |

`sandbox_allow_subprocess` en `system.json` (default `true`) controla solo fallback subprocess. Orden backend: `DEEPTUTOR_SANDBOX_RUNNER_URL` > `bwrap` > subprocess. `web_search_source_filtering` filtra URLs públicas `http`/`https`.

## Instalación backend

Requiere `Python 3.11–3.14`.

```bash
mkdir -p my-deeptutor && cd my-deeptutor
pip install -U deeptutor
deeptutor init
deeptutor start
```

Fuente:

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -e .
deeptutor init
deeptutor start --dev
```

Solo CLI desde checkout:

```bash
python -m pip install -e ./packaging/deeptutor-cli
deeptutor init --cli
deeptutor chat
```

## Comandos backend

```bash
deeptutor run chat "Explique transformada Fourier"
deeptutor run deep_solve "Solve x^2=4" -t rag --kb my-kb
deeptutor run visualize "Animate sine wave" --config render_mode=manim_video
deeptutor chat
deeptutor chat --capability deep_solve --tool rag --kb my-kb
deeptutor kb create my-kb --doc textbook.pdf
deeptutor kb list
deeptutor memory show
deeptutor config show
deeptutor partner list
deeptutor serve --port 8001
deeptutor start
```

## Deploy backend

```bash
docker run --rm --name deeptutor \
  -p 127.0.0.1:3782:3782 \
  -v deeptutor-data:/app/data \
  ghcr.io/hkuds/deeptutor:latest
```

Workspace contenido montado:

```bash
-v "$PWD/deeptutor-workspace:/workspace" \
-e DEEPTUTOR_WORKSPACE_ROOT=/workspace \
-e DEEPTUTOR_WORKSPACE_ALLOWED_ROOTS=/workspace \
```

Host modelos (`localhost` dentro contenedor ≠ host):

```bash
--add-host=host.docker.internal:host-gateway
```

Bases: Ollama `http://host.docker.internal:11434/v1`, LM Studio `http://host.docker.internal:1234/v1`, llama.cpp `http://host.docker.internal:8080/v1`, Lemonade `http://host.docker.internal:13305/api/v1`. Extras persistentes vía `DEEPTUTOR_EXTRAS`, sistema vía `DEEPTUTOR_APT_PACKAGES`. Solo `3782` publicado salvo curl directo API.

## Extras fuente (`pyproject.toml`)

`.[cli]`, `.[server]`, `.[partners]`, `.[matrix]`, `.[matrix-e2e]`, `.[math-animator]`, `.[dev]`, `.[all]`, más `parse-*`, `rag-lightrag`, `rag-rerank`, `graphrag`, `codebuddy`, `video-learning`.
