#!/bin/bash

# Crear entorno virtual de Python
echo "Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Configuración completada. Para activar el entorno virtual, ejecuta:"
echo "source venv/bin/activate"