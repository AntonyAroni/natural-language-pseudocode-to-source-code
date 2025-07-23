"""
Configuración para el sistema de conversión de voz a código Python.
"""

# Configuración para el reconocimiento de voz
SPEECH_RECOGNITION = {
    "language": "es-ES",  # Idioma para reconocimiento de voz
    "sample_rate": 16000,  # Tasa de muestreo para audio
    "timeout": 8,         # Tiempo máximo de espera para reconocimiento
}

# Configuración para el modelo transformer
TRANSFORMER = {
    "model_name": "Salesforce/codegen-350M-mono",  # Modelo pre-entrenado de Hugging Face
    "max_length": 512,                           # Longitud máxima de secuencia
    "temperature": 0.7,                          # Temperatura para generación
    "top_p": 0.9,                                # Top-p sampling
}

# Tokens especiales para el analizador léxico
SPECIAL_TOKENS = {
    "VARIABLE": ["var", "variable"],
    "FUNCTION": ["función", "funcion", "def", "definir"],
    "LOOP": ["para", "mientras", "for", "while"],
    "CONDITION": ["si", "if", "sino", "else"],
    "OPERATOR": ["más", "mas", "menos", "por", "dividido", "igual", "mayor", "menor"],
    "DATA_TYPE": ["entero", "flotante", "cadena", "booleano", "lista", "diccionario"],
}

# Mapeo de palabras clave en español a Python
KEYWORD_MAPPING = {
    "si": "if",
    "sino": "else",
    "para": "for",
    "mientras": "while",
    "en": "in",
    "rango": "range",
    "función": "def",
    "funcion": "def",
    "devolver": "return",
    "verdadero": "True",
    "falso": "False",
    "y": "and",
    "o": "or",
    "no": "not",
    "imprimir": "print",
    "clase": "class",
}

# Configuración para la generación de código
CODE_GENERATION = {
    "indent_size": 4,
    "max_line_length": 79,  # PEP 8
}