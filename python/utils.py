"""
Funciones de utilidad para el sistema de conversión de voz a código Python.
"""

import re
import logging
from typing import List, Dict, Any, Optional

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def normalize_text(text: str) -> str:
    """
    Normaliza el texto eliminando caracteres especiales y normalizando espacios.
    
    Args:
        text: Texto a normalizar
        
    Returns:
        Texto normalizado
    """
    # Convertir a minúsculas
    text = text.lower()
    
    # Eliminar caracteres especiales excepto espacios y puntuación básica
    text = re.sub(r'[^\w\s.,;:?!¿¡]', '', text)
    
    # Normalizar espacios
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def tokenize(text: str) -> List[str]:
    """
    Divide el texto en tokens.
    
    Args:
        text: Texto a tokenizar
        
    Returns:
        Lista de tokens
    """
    # Separar por espacios y puntuación
    tokens = re.findall(r'\w+|[.,;:?!¿¡]', text)
    return tokens

def format_python_code(code: str) -> str:
    """
    Formatea el código Python generado para que cumpla con PEP 8.
    
    Args:
        code: Código Python a formatear
        
    Returns:
        Código Python formateado
    """
    # Esta es una implementación básica
    # En un sistema real, se podría usar black, autopep8 u otra herramienta
    
    lines = code.split('\n')
    formatted_lines = []
    
    indent_level = 0
    for line in lines:
        # Eliminar espacios en blanco al inicio y final
        stripped = line.strip()
        
        # Ajustar nivel de indentación
        if stripped.endswith(':'):
            formatted_lines.append('    ' * indent_level + stripped)
            indent_level += 1
        elif stripped in ['else:', 'elif:', 'except:', 'finally:']:
            indent_level = max(0, indent_level - 1)
            formatted_lines.append('    ' * indent_level + stripped)
            indent_level += 1
        elif stripped in ['break', 'continue', 'pass', 'return']:
            formatted_lines.append('    ' * indent_level + stripped)
        elif stripped:
            formatted_lines.append('    ' * indent_level + stripped)
    
    return '\n'.join(formatted_lines)

def save_to_file(code: str, filename: str) -> bool:
    """
    Guarda el código generado en un archivo.
    
    Args:
        code: Código a guardar
        filename: Nombre del archivo
        
    Returns:
        True si se guardó correctamente, False en caso contrario
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(code)
        logger.info(f"Código guardado en {filename}")
        return True
    except Exception as e:
        logger.error(f"Error al guardar el código: {e}")
        return False