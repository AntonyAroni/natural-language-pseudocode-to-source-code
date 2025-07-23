"""
Punto de entrada principal para el sistema de conversión de voz a código Python.
"""

import argparse
import logging
import os
import sys
from typing import Optional

from voice_recognition import SpeechRecognizer
from transformer_model import TransformerModel
from lexical_analyzer import LexicalAnalyzer
from simple_syntax_analyzer import SimpleSyntaxAnalyzer
from simple_semantic_analyzer import SimpleSemanticAnalyzer
from simple_code_generator import SimpleCodeGenerator
from utils import save_to_file

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_voice_to_code(audio_file: Optional[str] = None, output_file: Optional[str] = None, use_pseudocode: bool = False) -> str:
    """
    Procesa voz a código Python.
    
    Args:
        audio_file: Ruta al archivo de audio (None para usar micrófono)
        output_file: Ruta al archivo de salida (None para no guardar)
        use_pseudocode: Si es True, genera pseudocódigo intermedio
        
    Returns:
        Código Python generado
    """
    # Paso 1: Reconocimiento de voz
    recognizer = SpeechRecognizer()
    
    if audio_file:
        text = recognizer.recognize_from_file(audio_file)
    else:
        text = recognizer.recognize_from_microphone()
    
    if not text:
        logger.error("No se pudo reconocer ningún texto")
        return ""
    
    logger.info(f"Texto reconocido: {text}")
    
    # Paso 2: Transformación a pseudocódigo o directamente a Python
    transformer = TransformerModel()
    
    # Generar código Python inicial
    python_code = transformer.natural_to_pseudocode(text)
    logger.info(f"Código Python generado:\n{python_code}")
    
    # Si solo queremos el código Python generado directamente
    if use_pseudocode and output_file:
        save_to_file(python_code, output_file)
        print(f"\nCódigo Python guardado en: {output_file}")
        return python_code
    
    # Usar el código Python como entrada para los analizadores
    input_text = python_code
    
    # Paso 3: Análisis léxico
    lexical_analyzer = LexicalAnalyzer()
    tokens = lexical_analyzer.tokenize(input_text)
    tokens = lexical_analyzer.map_to_python_tokens(tokens)
    
    logger.info(f"Tokens generados: {len(tokens)} tokens")
    
    # Paso 4: Análisis sintáctico simplificado
    syntax_analyzer = SimpleSyntaxAnalyzer()
    ast = syntax_analyzer.parse(tokens, input_text)
    
    if not ast:
        logger.error("Error en el análisis sintáctico simplificado")
        return ""
    
    logger.info("AST generado correctamente")
    
    # Paso 5: Análisis semántico simplificado
    semantic_analyzer = SimpleSemanticAnalyzer()
    is_valid = semantic_analyzer.analyze(ast)
    
    if not is_valid:
        logger.error("Error en el análisis semántico simplificado")
        errors = semantic_analyzer.get_errors()
        for error in errors:
            logger.error(f"Error semántico: {error}")
        return ""
    
    logger.info("Análisis semántico completado con éxito")
    
    # Paso 6: Generación de código simplificada
    code_generator = SimpleCodeGenerator(semantic_analyzer.get_symbol_table())
    python_code = code_generator.generate(ast)
    
    logger.info(f"Código Python generado:\n{python_code}")
    
    # Guardar el código si se especificó un archivo de salida
    if output_file:
        save_to_file(python_code, output_file)
    
    return python_code

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='Convierte voz a código Python.')
    parser.add_argument('--audio', type=str, help='Ruta al archivo de audio')
    parser.add_argument('--output', type=str, help='Ruta al archivo de salida')
    parser.add_argument('--pseudocode', action='store_true', help='Generar pseudocódigo intermedio')
    
    args = parser.parse_args()
    
    try:
        code = process_voice_to_code(args.audio, args.output, args.pseudocode)
        
        if code:
            print("\nCódigo Python generado:")
            print("------------------------")
            print(code)
            print("------------------------")
            
            if args.output:
                print(f"\nCódigo guardado en: {args.output}")
        else:
            print("\nNo se pudo generar código Python.")
    
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        print(f"\nError inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())