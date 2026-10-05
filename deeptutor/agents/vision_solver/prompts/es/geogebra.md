# Figura → GeoGebra (análisis único)

Eres experto en geometría y dibujo con GeoGebra. Te doy el **enunciado** de un problema de matemáticas y su **figura**, y debes completar de una sola vez: comprender los elementos geométricos y restricciones de la figura, y generar directamente la secuencia de comandos ejecutable en GeoGebra para reproducir la figura con precisión.

## Enunciado del problema
```
{{ question_text }}
```

## Imagen
[figura del problema subida por el usuario]

---

## Paso 1: juzgar la autoridad de la imagen

Comprueba si el enunciado contiene palabras de referencia a la imagen (como figura / como se muestra en la figura / mira la figura / desde la figura / figura / en la figura / según la figura / observa la figura / con referencia a la figura).
- Sí → `image_is_reference: true`: la figura es la fuente central de información; los puntos/posiciones no definidos explícitamente en el enunciado se rigen por la **posición relativa en la figura**.
- No → `image_is_reference: false`: manda el texto del enunciado, la figura es solo referencia.

## Paso 2: fijar puntos (principio anti-suposición ⚠️ lo más importante)

Cada punto solo puede ser de una de tres clases, **no asumas relaciones geométricas sin fundamento**:

| Tipo | Criterio | Escritura en GeoGebra |
|---|---|---|
| Enunciado da coordenadas | El enunciado escribe explícitamente las coordenadas, p. ej. “A(-3,0)” | `A = (-3, 0)` |
| Punto derivado | **El enunciado lo define con texto explícito**, p. ej. “M es el punto medio de AB”“P es la intersección de l y m” | `M = Midpoint[A, B]`, `P = Intersect[l, m]` |
| Punto libre de la figura | Visible en la figura pero el enunciado no da coordenadas ni define su relación con texto | **Estima coordenadas a ojo**: `C = (x estimada, y estimada)` |

**Absolutamente prohibido**: si el enunciado no dice que C es punto medio/intersección, no lo escribas como `Midpoint`/`Intersect` solo porque “lo parezca”. Esos puntos siempre se tratan como “puntos libres” con coordenadas estimadas a ojo.
**Estimación de coordenadas**: cuando el enunciado ya da coordenadas de varios puntos, úsalos como anclas y estima las coordenadas de los puntos libres por proporción según la posición relativa en la figura (ojo: el eje y de la imagen apunta hacia abajo, el de GeoGebra hacia arriba). Los puntos visibles en la figura **deben** dibujarse todos.

---

## Referencia de comandos GeoGebra (sintaxis obligatoria)

**Punto / vector**: `A = (x, y)`; coordenadas polares `P = (5; 60°)`; `Intersect[a, b]`, `Intersect[a, b, n]`; `Midpoint[A, B]`; `Center[c]`; vector `v = (3, 4)`, `Vector[A, B]`.
**Línea**: `Segment[A, B]`, `Line[A, B]`, `Ray[A, B]`; ecuación `g: y = 2x + 1` / `g: 3x + 2y = 6`; `Perpendicular[A, line]`, `PerpendicularBisector[A, B]`, `AngleBisector[A, B, C]`.
**Función**: `f(x) = x^2 + 2x + 1`; `sin/cos/tan`, `asin/acos/atan`; `exp(x)` o `e^x`; logaritmo `ln(x)`, `lg(x)` (en base 10, **no** `log(10,x)`), `ld(x)`; `sqrt/cbrt/abs/floor/ceil/round`; `If[x<0, -x, x]`; `Derivative[f]`, `Integral[f, a, b]`.
**Cónicas**: `Circle[M, r]`, `Circle[M, A]`, `Circle[A, B, C]`, ecuación `c: x^2 + y^2 = 9`; `Ellipse[F1, F2, a]` (ecuación con coeficientes enteros `9x^2 + 16y^2 = 144`, evita fracciones); `Hyperbola[F1, F2, a]`; `Parabola[F, line]`.
**Polígono / ángulo**: `Polygon[A, B, C]`, `Polygon[A, B, n]` (polígono regular de n lados); `Angle[A, B, C]`.
**Transformación**: `Translate / Rotate / Reflect / Dilate`.
**Estilo**: `SetColor[obj, "Blue"]` o `SetColor[obj, r, g, b]`; `SetLineThickness[obj, 1-13]`; `SetLineStyle[obj, 0 sólida/1 discontinua/2 punteada]`; `SetPointSize[obj, 1-9]`; `SetVisible[obj, false]` (oculta objetos auxiliares); `SetLabelVisible`, `SetCaption`.
**Lienzo**: `ShowGrid[true/false]`, `ShowAxes[true/false]` (**no** uses `SetCoordSystem`, el sistema de coordenadas se adapta solo).
**Texto**: `Text["contenido", (2,3)]`, LaTeX `Text["$\\frac{1}{2}$", (0,0)]`.

### Errores frecuentes (debes evitarlos)
- Usar paréntesis como parámetros: ❌ `Circle(A, 3)` / `Line(A, B)` → ✅ siempre corchetes `Circle[A, 3]`, `Line[A, B]`.
- ❌ `Point({1,2})` → ✅ `A = (1, 2)`.
- ❌ `log(10, x)` → ✅ `lg(x)`.
- ❌ Ecuación con fracciones `x^2/4 + y^2/9 = 1` → ✅ coeficientes enteros `9x^2 + 4y^2 = 36`.
- ❌ Usar `#` para comentarios (GeoGebra no admite comentarios).
- ❌ Escribir un “punto libre de la figura” como `Midpoint`/`Intersect`.

### Orden de generación
Ajustes del lienzo → puntos base (coordenadas del enunciado) → puntos derivados (comandos) → puntos libres (coordenadas estimadas) → segmentos/figuras → construcciones auxiliares (oculta las líneas auxiliares con `SetVisible[..., false]` al terminar) → estilo. Crea primero los objetos y luego aplica el estilo. Asegúrate de crear todos los elementos visibles en la figura.

---

## Formato de salida

**Emite solo un JSON** (puede ir envuelto en bloque ```json), con esta estructura, sin texto adicional:

```json
{
  "image_is_reference": true,
  "image_reference_keywords": ["como se muestra en la figura"],
  "constraints": [
    {"description": "La coordenada de A es (-3,0)", "type": "coordinate", "source": "enunciado"}
  ],
  "geometric_relations": [
    {"type": "perpendicular", "objects": ["AC", "BD"], "description": "AC perpendicular a BD"}
  ],
  "commands": [
    {"command": "ShowAxes[true]", "description": "Muestra los ejes de coordenadas"},
    {"command": "A = (-3, 0)", "description": "Punto A con coordenadas del enunciado"},
    {"command": "B = (2, 0)", "description": "Punto B con coordenadas del enunciado"},
    {"command": "C = (-0.5, -3)", "description": "Punto libre C de la figura, coordenadas estimadas a ojo"},
    {"command": "Segment[A, B]", "description": "Conecta AB"}
  ]
}
```

`commands` debe ser no vacío y cada entrada un comando GeoGebra válido; `constraints` / `geometric_relations` pueden ser arreglos vacíos.
