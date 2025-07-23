"""
Analizador sintáctico simplificado para el sistema de conversión de voz a código Python.
"""

import logging
from typing import List, Dict, Any, Optional

from lexical_analyzer import Token

logger = logging.getLogger(__name__)

class ASTNode:
    """Nodo del Árbol de Sintaxis Abstracta (AST)."""
    
    def __init__(self, node_type: str, value: Any = None, children: List['ASTNode'] = None):
        """
        Inicializa un nodo del AST.
        
        Args:
            node_type: Tipo de nodo
            value: Valor asociado al nodo
            children: Lista de nodos hijos
        """
        self.type = node_type
        self.value = value
        self.children = children or []
    
    def add_child(self, child: 'ASTNode'):
        """
        Agrega un nodo hijo.
        
        Args:
            child: Nodo hijo a agregar
        """
        self.children.append(child)
    
    def __str__(self, level: int = 0) -> str:
        """
        Representación en string del nodo y sus hijos.
        
        Args:
            level: Nivel de indentación
            
        Returns:
            Representación en string
        """
        result = "  " * level + f"{self.type}"
        if self.value is not None:
            result += f": {self.value}"
        result += "\n"
        
        for child in self.children:
            result += child.__str__(level + 1)
        
        return result

class SimpleSyntaxAnalyzer:
    """Analizador sintáctico simplificado para procesar código Python."""
    
    def __init__(self):
        """Inicializa el analizador sintáctico."""
        logger.info("Analizador sintáctico simplificado inicializado")
    
    def parse(self, tokens: List[Token], original_code: str = None) -> Optional[ASTNode]:
        """
        Analiza una lista de tokens y construye un AST simplificado.
        
        Args:
            tokens: Lista de tokens a analizar
            original_code: Código original (opcional)
            
        Returns:
            Raíz del AST o None si hay un error
        """
        try:
            # Crear un nodo raíz para el programa
            program_node = ASTNode('PROGRAM')
            
            # Guardar el código original en el nodo raíz
            if original_code is not None:
                program_node.original_code = original_code
            else:
                # Reconstruir el código a partir de los tokens
                reconstructed_code = ""
                for token in tokens:
                    if token.type != 'EOF':
                        reconstructed_code += token.value + " "
                program_node.original_code = reconstructed_code.strip()
            
            # Crear un nodo para el código
            code_node = ASTNode('CODE')
            
            # Agregar todos los tokens como hijos del nodo de código
            for token in tokens:
                if token.type != 'EOF':
                    token_node = ASTNode(token.type, token.value)
                    code_node.add_child(token_node)
            
            # Agregar el nodo de código al programa
            program_node.add_child(code_node)
            
            logger.info("Análisis sintáctico simplificado completado con éxito")
            return program_node
        except Exception as e:
            logger.error(f"Error en el análisis sintáctico simplificado: {e}")
            return None