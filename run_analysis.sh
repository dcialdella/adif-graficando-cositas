#!/bin/bash

# Script rápido para ejecutar solo el análisis ADI
# (asume que el entorno ya está configurado)

echo "=== Ejecutando análisis ADI ==="

# Verificar si existe el entorno virtual
if [ ! -d "venv_adi" ]; then
    echo "Error: Entorno virtual no encontrado. Ejecuta primero setup_and_run.sh"
    exit 1
fi

# Activar entorno virtual
source venv_adi/bin/activate

# Verificar que existe el archivo ADI
if [ ! -f "aaa.adi" ]; then
    echo "Error: Archivo aaa.adi no encontrado"
    deactivate
    exit 1
fi

# Ejecutar el analizador
python analizar_adi_grafico.py

echo "=== Análisis completado ==="

# Desactivar entorno virtual
deactivate