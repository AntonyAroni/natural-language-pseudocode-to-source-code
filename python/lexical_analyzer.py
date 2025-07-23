"""
Analizador léxico para el sistema de conversión de voz a código Python.
"""

import re
import logging
from typing import List, Dict, Any, Tuple

from config import SPECIAL_TOKENS, KEYWORD_MAPPING
from utils import normalize_text

logger = logging.getLogger(__name__)

class Token:
    """Clase para representar un token."""

    def __init__(self, token_type: str, value: str, position: int):
        """
        Inicializa un token.
        
        Args:
            token_type: Tipo de token
            value: Valor del token
            position: Posición en el texto original
        """
        self.type = token_type
        self.value = value
        self.position = position
    
    def __str__(self) -> str:
        return f"Token({self.type}, '{self.value}', pos={self.position})"
    
    def __repr__(self) -> str:
        return self.__str__()

class LexicalAnalyzer:
    """Analizador léxico para procesar texto en lenguaje natural o pseudocódigo."""
    
    def __init__(self, special_tokens: Dict[str, List[str]] = None, keyword_mapping: Dict[str, str] = None):
        """
        Inicializa el analizador léxico.
        
        Args:
            special_tokens: Diccionario de tokens especiales
            keyword_mapping: Mapeo de palabras clave en español a Python
        """
        self.special_tokens = special_tokens or SPECIAL_TOKENS
        self.keyword_mapping = keyword_mapping or KEYWORD_MAPPING
        
        # Construir expresiones regulares para tokens
        self._build_token_patterns()
        
        logger.info("Analizador léxico inicializado")
    
    def _build_token_patterns(self):
        """Construye patrones de expresiones regulares para identificar tokens."""
        self.patterns = [
            # Identificadores y palabras clave
            (r'[a-zA-Z_][a-zA-Z0-9_]*', self._identify_word),
            
            # Números
            (r'\d+\.\d+', lambda m, p: Token('FLOAT', m.group(), p)),
            (r'\d+', lambda m, p: Token('INTEGER', m.group(), p)),
            
            # Operadores
            (r'[+\-*/=<>!]=?', lambda m, p: Token('OPERATOR', m.group(), p)),
            
            # Delimitadores
            (r'[\(\)\[\]\{\},;:]', lambda m, p: Token('DELIMITER', m.group(), p)),
            
            # Cadenas
            (r'"[^"]*"', lambda m, p: Token('STRING', m.group(), p)),
            (r"'[^']*'", lambda m, p: Token('STRING', m.group(), p)),
            
            # Espacios en blanco (ignorar)
            (r'\s+', None)
        ]
    
    def _identify_word(self, match, position: int) -> Token:
        """
        Identifica el tipo de una palabra (keyword, identificador, etc.).
        
        Args:
            match: Objeto match de regex
            position: Posición en el texto
            
        Returns:
            Token identificado
        """
        word = match.group().lower()
        
        # Verificar si es una palabra clave de Python
        if word in ['def', 'if', 'else', 'elif', 'for', 'while', 'in', 'return', 'and', 'or', 'not', 'True', 'False', 'None', 'print', 'class']:
            return Token('KEYWORD', word, position)
        
        # Verificar si es una palabra clave en español que debe mapearse a Python
        if word in self.keyword_mapping:
            return Token('KEYWORD', self.keyword_mapping[word], position)
        
        # Verificar si es un token especial
        for token_type, words in self.special_tokens.items():
            if word in words:
                return Token(token_type, word, position)
        
        # Si no es ninguno de los anteriores, es un identificador
        return Token('IDENTIFIER', word, position)
    
    def tokenize(self, text: str) -> List[Token]:
        """
        Convierte el texto en una lista de tokens.
        
        Args:
            text: Texto a tokenizar
            
        Returns:
            Lista de tokens
        """
        normalized_text = normalize_text(text)
        tokens = []
        position = 0
        
        while position < len(normalized_text):
            match = None
            
            for pattern, token_func in self.patterns:
                regex = re.compile(pattern)
                match = regex.match(normalized_text, position)
                
                if match:
                    if token_func:  # Si no es None, procesar el token
                        token = token_func(match, position)
                        tokens.append(token)
                    
                    position = match.end()
                    break
            
            if not match:
                # Si no coincide con ningún patrón, avanzar un carácter
                position += 1
        
        # Agregar token de fin de archivo
        tokens.append(Token('EOF', '', position))
        
        return tokens
    
    def map_to_python_tokens(self, tokens: List[Token]) -> List[Token]:
        """
        Mapea tokens en español a sus equivalentes en Python.
        
        Args:
            tokens: Lista de tokens
            
        Returns:
            Lista de tokens mapeados a Python
        """
        mapped_tokens = []
        
        for token in tokens:
            if token.type == 'KEYWORD' and token.value in self.keyword_mapping:
                # Mapear palabras clave a Python
                mapped_tokens.append(Token(token.type, self.keyword_mapping[token.value], token.position))
            else:
                mapped_tokens.append(token)
        
        return mapped_tokens