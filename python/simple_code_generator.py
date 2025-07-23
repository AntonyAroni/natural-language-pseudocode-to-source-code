"""
Generador de código Python simplificado a partir del AST.
"""

import logging
from typing import Dict, Any, Optional

from simple_syntax_analyzer import ASTNode

logger = logging.getLogger(__name__)

class SimpleCodeGenerator:
    """Generador de código Python simplificado a partir del AST."""
    
    def __init__(self, symbol_table: Optional[Dict[str, Any]] = None):
        """
        Inicializa el generador de código.
        
        Args:
            symbol_table: Tabla de símbolos del análisis semántico
        """
        self.symbol_table = symbol_table or {}
        logger.info("Generador de código simplificado inicializado")
    
    def generate(self, ast: ASTNode) -> str:
        """
        Genera código Python a partir del AST.
        
        Args:
            ast: Raíz del AST
            
        Returns:
            Código Python generado
        """
        try:
            # En esta implementación simplificada, simplemente devolvemos el código original
            # que se pasó al analizador sintáctico
            
            # Obtener el código original del atributo 'original_code' del AST
            # Este atributo se establece en el método parse() de SimpleSyntaxAnalyzer
            if hasattr(ast, 'original_code'):
                code = ast.original_code
            else:
                # Si no hay código original, devolver un mensaje de error
                logger.error("No se encontró el código original en el AST")
                return "# Error: No se encontró el código original en el AST"
            
            logger.info("Generación de código simplificada completada con éxito")
            return code
        except Exception as e:
            logger.error(f"Error en la generación de código simplificada: {e}")
            return f"# Error en la generación de código: {e}"