#!/usr/bin/env python3
"""
Script para verificar las dependencias necesarias.
"""

import importlib
import sys

def check_dependency(module_name, package_name=None):
    """
    Verifica si una dependencia está instalada.
    
    Args:
        module_name: Nombre del módulo a importar
        package_name: Nombre del paquete a instalar (si es diferente del módulo)
    
    Returns:
        True si la dependencia está instalada, False en caso contrario
    """
    package_name = package_name or module_name
    
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name} está instalado")
        return True
    except ImportError:
        print(f"✗ {module_name} no está instalado")
        print(f"  Instálalo con: pip install {package_name}")
        return False

def main():
    """Función principal."""
    print("Verificando dependencias...")
    
    # Lista de dependencias a verificar
    dependencies = [
        ("speech_recognition", "SpeechRecognition"),
        ("pyaudio", "PyAudio"),
    ]
    
    # Verificar cada dependencia
    all_installed = True
    for module_name, package_name in dependencies:
        if not check_dependency(module_name, package_name):
            all_installed = False
    
    if all_installed:
        print("\nTodas las dependencias están instaladas.")
    else:
        print("\nFaltan algunas dependencias. Instálalas con:")
        print("pip install -r requirements.txt")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())