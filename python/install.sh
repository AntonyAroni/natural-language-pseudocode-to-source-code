#!/bin/bash

# Script de instalación para el sistema de conversión de voz a código Python

echo "Instalando el sistema de conversión de voz a código Python..."
echo "============================================================"

# Crear entorno virtual
echo "Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Descargar modelo pre-entrenado
echo "Descargando modelo pre-entrenado..."
python download_model.py

echo "============================================================"
echo "Instalación completada."
echo "Para activar el entorno virtual, ejecuta: source venv/bin/activate"
echo "Para usar el sistema, ejecuta: python main.py"
echo "============================================================"