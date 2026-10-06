# Immersive Reading extensions

Server-side plugins vía entry-point `deeptutor.reading_extensions`. Sin paquetes instalados, no hay toolbar.

```toml
[project.entry-points."deeptutor.reading_extensions"]
example = "example_reading_plugin:ExampleExtension"
```

```python
from deeptutor.reading.extensions import ReadingAction, ReadingExtensionManifest, ReadingExtensionResult

class ExampleExtension:
    manifest = ReadingExtensionManifest(id="example", version="1.0.0", name="Example",
        actions=[ReadingAction(id="explain", label="Explain")], result_types=["card"])
    def run_action(self, action, context):
        return ReadingExtensionResult(type="card", title="Example",
            payload={"body": context.visible_text[:500]})
```
Protocolo v1 (cambios incompatibles → nueva versión). Entry point = objeto con `manifest` validado + `run_action(action, context)`.

<details>
<summary>Límites seguridad</summary>

- Auth global Reading API; servidor resuelve material/locator/texto, browser no los suplanta; selección solo si verbatim en unidad.
- Resultados: `card/quiz/feedback/browser_speech`, techo 64 KB, texto React (sin JS/HTML).
- Unidad >60k chars → error sin invocar; timeout 30s → fail-fast + circuito abierto (restart tras arreglar); fallos aislados.
</details>
