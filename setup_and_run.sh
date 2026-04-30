#!/bin/bash

# Script para configurar entorno virtual y ejecutar el analizador ADI
# Autor: Generado para análisis de logs de radioaficionado

echo "=== Configurando entorno para análisis ADI ==="

# Crear entorno virtual si no existe
if [ ! -d "venv_adi" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv_adi
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv_adi/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Ejecutar el analizador
echo "Ejecutando análisis ADI..."
python analizar_adi_grafico.py

echo "=== Análisis completado ==="
echo "Revisa los archivos generados:"
echo "- estadisticas_adi.json (datos en JSON)"
echo "- grafico_paises.png (gráfico de países)"
echo "- grafico_localizadores.png (gráfico de localizadores)"
echo "- grafico_modos_bandas.png (gráfico de modos y bandas)"
echo "- grafico_estaciones_top.png (top estaciones)"
echo "- grafico_distribucion_horaria.png (distribución por horas)"

# Desactivar entorno virtual
deactivate