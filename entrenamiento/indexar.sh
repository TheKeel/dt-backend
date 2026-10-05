#!/bin/bash
# Indexa el lote de lógica matemática en el rack central.
# Uso: ./indexar.sh   (desde la raíz del proyecto)
set -e
deeptutor kb add logica-matematica --docs-dir entrenamiento/logica-matematica
