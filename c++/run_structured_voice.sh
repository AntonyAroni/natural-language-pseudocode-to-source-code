#!/bin/bash

# Activar entorno virtual
source venv/bin/activate

# Verificar si el compilador existe
if [ ! -f "./build/proyecto_compiladores" ]; then
    echo "El compilador no está compilado. Compilando..."
    mkdir -p build
    cd build
    cmake ..
    make
    cd ..
    echo "Compilador compilado correctamente."
fi

# Ejecutar el script de instrucciones estructuradas a código
python structured_voice_to_code.py "$@"