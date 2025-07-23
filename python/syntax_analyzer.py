"""
Analizador sintáctico para el sistema de conversión de voz a código Python.
"""

import logging
from typing import List, Dict, Any, Optional

from lexical_analyzer import Token, LexicalAnalyzer

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

class SyntaxAnalyzer:
    """Analizador sintáctico para procesar tokens y construir un AST."""
    
    def __init__(self):
        """Inicializa el analizador sintáctico."""
        self.tokens = []
        self.current_token_index = 0
        logger.info("Analizador sintáctico inicializado")
    
    def parse(self, tokens: List[Token]) -> Optional[ASTNode]:
        """
        Analiza una lista de tokens y construye un AST.
        
        Args:
            tokens: Lista de tokens a analizar
            
        Returns:
            Raíz del AST o None si hay un error
        """
        self.tokens = tokens
        self.current_token_index = 0
        
        try:
            # Comenzar el análisis desde el programa
            ast = self.parse_program()
            logger.info("Análisis sintáctico completado con éxito")
            return ast
        except Exception as e:
            logger.error(f"Error en el análisis sintáctico: {e}")
            return None
    
    def current_token(self) -> Token:
        """
        Obtiene el token actual.
        
        Returns:
            Token actual
        """
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return Token('EOF', '', -1)
    
    def consume(self) -> Token:
        """
        Consume el token actual y avanza al siguiente.
        
        Returns:
            Token consumido
        """
        token = self.current_token()
        self.current_token_index += 1
        return token
    
    def expect(self, token_type: str) -> Token:
        """
        Espera un tipo de token específico y lo consume.
        
        Args:
            token_type: Tipo de token esperado
            
        Returns:
            Token consumido
            
        Raises:
            SyntaxError: Si el token actual no es del tipo esperado
        """
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(f"Se esperaba {token_type}, pero se encontró {token.type}")
        
        return self.consume()
    
    def parse_program(self) -> ASTNode:
        """
        Analiza un programa completo.
        
        Returns:
            Nodo raíz del AST
        """
        program_node = ASTNode('PROGRAM')
        
        # Analizar declaraciones hasta el final del archivo
        while self.current_token().type != 'EOF':
            statement = self.parse_statement()
            if statement:
                program_node.add_child(statement)
        
        return program_node
    
    def parse_statement(self) -> Optional[ASTNode]:
        """
        Analiza una declaración.
        
        Returns:
            Nodo de declaración o None si hay un error
        """
        token = self.current_token()
        
        # Función
        if token.type == 'KEYWORD' and token.value == 'def':
            return self.parse_function_definition()
        
        # Condicional
        elif token.type == 'KEYWORD' and token.value == 'if':
            return self.parse_if_statement()
        
        # Bucle
        elif token.type == 'KEYWORD' and token.value in ['for', 'while']:
            return self.parse_loop()
        
        # Asignación o expresión
        else:
            return self.parse_expression_statement()
    
    def parse_function_definition(self) -> ASTNode:
        """
        Analiza una definición de función.
        
        Returns:
            Nodo de definición de función
        """
        # Consumir 'def'
        token = self.consume()
        
        # Imprimir el token actual para depuración
        current = self.current_token()
        print(f"Token actual después de consumir 'def': {current.type}, '{current.value}'")
        
        # Nombre de la función
        name_token = self.current_token()
        if name_token.type != 'IDENTIFIER':
            # Si no es un identificador, intentamos continuar con el valor actual
            print(f"ADVERTENCIA: Se esperaba un identificador, pero se encontró {name_token.type}")
            name_value = name_token.value
            self.consume()
        else:
            name_value = name_token.value
            self.consume()
        
        # Parámetros
        if self.current_token().type == 'DELIMITER' and self.current_token().value == '(':
            self.consume()  # Consumir '('
        else:
            print(f"ADVERTENCIA: Se esperaba '(', pero se encontró {self.current_token().type}: '{self.current_token().value}'")
        
        params_node = ASTNode('PARAMETERS')
        
        # Analizar parámetros si hay
        if self.current_token().type != 'DELIMITER' or self.current_token().value != ')':
            while True:
                param_token = self.current_token()
                if param_token.type != 'IDENTIFIER':
                    print(f"ADVERTENCIA: Se esperaba un identificador para parámetro, pero se encontró {param_token.type}")
                    break
                
                self.consume()  # Consumir el identificador
                params_node.add_child(ASTNode('PARAMETER', param_token.value))
                
                if self.current_token().type == 'DELIMITER' and self.current_token().value == ',':
                    self.consume()  # Consumir ','
                else:
                    break
        
        if self.current_token().type == 'DELIMITER' and self.current_token().value == ')':
            self.consume()  # Consumir ')'
        else:
            print(f"ADVERTENCIA: Se esperaba ')', pero se encontró {self.current_token().type}: '{self.current_token().value}'")
        
        # Cuerpo de la función
        body_node = self.parse_block()
        
        # Crear nodo de función
        function_node = ASTNode('FUNCTION_DEF', name_value)
        function_node.add_child(params_node)
        function_node.add_child(body_node)
        
        return function_node
    
    def parse_if_statement(self) -> ASTNode:
        """
        Analiza una declaración if.
        
        Returns:
            Nodo de declaración if
        """
        # Consumir 'if' o 'si'
        self.consume()
        
        # Condición
        condition_node = self.parse_expression()
        
        # Bloque then
        then_block = self.parse_block()
        
        if_node = ASTNode('IF_STATEMENT')
        if_node.add_child(ASTNode('CONDITION', None, [condition_node]))
        if_node.add_child(ASTNode('THEN', None, [then_block]))
        
        # Bloque else si existe
        if (self.current_token().type == 'KEYWORD' and 
            self.current_token().value == 'else'):
            self.consume()  # Consumir 'else' o 'sino'
            else_block = self.parse_block()
            if_node.add_child(ASTNode('ELSE', None, [else_block]))
        
        return if_node
    
    def parse_loop(self) -> ASTNode:
        """
        Analiza un bucle (for o while).
        
        Returns:
            Nodo de bucle
        """
        token = self.consume()
        
        if token.value == 'for':
            # Bucle for
            var_token = self.expect('IDENTIFIER')
            
            # Consumir 'in'
            if self.current_token().type == 'KEYWORD' and self.current_token().value == 'in':
                self.consume()
            else:
                raise SyntaxError("Se esperaba 'in' después del identificador en un bucle for")
            
            # Iterable
            iterable_node = self.parse_expression()
            
            # Bloque del bucle
            body_node = self.parse_block()
            
            for_node = ASTNode('FOR_LOOP')
            for_node.add_child(ASTNode('VARIABLE', var_token.value))
            for_node.add_child(ASTNode('ITERABLE', None, [iterable_node]))
            for_node.add_child(ASTNode('BODY', None, [body_node]))
            
            return for_node
        else:
            # Bucle while
            condition_node = self.parse_expression()
            
            # Bloque del bucle
            body_node = self.parse_block()
            
            while_node = ASTNode('WHILE_LOOP')
            while_node.add_child(ASTNode('CONDITION', None, [condition_node]))
            while_node.add_child(ASTNode('BODY', None, [body_node]))
            
            return while_node
    
    def parse_block(self) -> ASTNode:
        """
        Analiza un bloque de código.
        
        Returns:
            Nodo de bloque
        """
        # Verificar si hay un delimitador de bloque (':')
        if self.current_token().type == 'DELIMITER' and self.current_token().value == ':':
            self.consume()  # Consumir ':'
        else:
            print(f"ADVERTENCIA: Se esperaba ':', pero se encontró {self.current_token().type}: '{self.current_token().value}'")
        
        block_node = ASTNode('BLOCK')
        
        # En un análisis real, aquí manejaríamos la indentación
        # Para simplificar, asumimos que cada declaración es parte del bloque
        # hasta encontrar un token que indique el fin del bloque
        
        # Analizar declaraciones hasta el final del bloque
        # Para simplificar, solo procesamos una declaración por bloque
        if self.current_token().type != 'EOF':
            statement = self.parse_statement()
            if statement:
                block_node.add_child(statement)
        
        return block_node
    
    def parse_expression_statement(self) -> ASTNode:
        """
        Analiza una declaración de expresión.
        
        Returns:
            Nodo de declaración de expresión
        """
        # Verificar si es una asignación
        if (self.current_token().type == 'IDENTIFIER' and 
            self.peek_next_token().type == 'OPERATOR' and 
            self.peek_next_token().value == '='):
            
            # Asignación
            var_token = self.consume()  # Consumir identificador
            self.consume()  # Consumir '='
            
            expr_node = self.parse_expression()
            
            assign_node = ASTNode('ASSIGNMENT')
            assign_node.add_child(ASTNode('VARIABLE', var_token.value))
            assign_node.add_child(expr_node)
            
            return assign_node
        else:
            # Expresión
            return self.parse_expression()
    
    def parse_expression(self) -> ASTNode:
        """
        Analiza una expresión.
        
        Returns:
            Nodo de expresión
        """
        # Implementación simplificada
        # En un analizador real, aquí manejaríamos precedencia de operadores, etc.
        
        # Por ahora, solo manejamos expresiones simples
        token = self.current_token()
        
        if token.type in ['INTEGER', 'FLOAT']:
            self.consume()
            return ASTNode('LITERAL', token.value)
        
        elif token.type == 'STRING':
            self.consume()
            return ASTNode('LITERAL', token.value)
        
        elif token.type == 'IDENTIFIER':
            self.consume()
            
            # Verificar si es una llamada a función
            if self.current_token().type == 'DELIMITER' and self.current_token().value == '(':
                self.consume()  # Consumir '('
                
                args_node = ASTNode('ARGUMENTS')
                
                # Analizar argumentos si hay
                if self.current_token().type != 'DELIMITER' or self.current_token().value != ')':
                    while True:
                        arg_node = self.parse_expression()
                        args_node.add_child(arg_node)
                        
                        if self.current_token().type == 'DELIMITER' and self.current_token().value == ',':
                            self.consume()  # Consumir ','
                        else:
                            break
                
                self.expect('DELIMITER')  # Consumir ')'
                
                call_node = ASTNode('FUNCTION_CALL', token.value)
                call_node.add_child(args_node)
                
                return call_node
            else:
                return ASTNode('VARIABLE', token.value)
        
        elif token.type == 'DELIMITER' and token.value == '(':
            self.consume()  # Consumir '('
            expr_node = self.parse_expression()
            self.expect('DELIMITER')  # Consumir ')'
            return expr_node
        
        else:
            # Manejar otros tipos de expresiones según sea necesario
            self.consume()
            return ASTNode('EXPRESSION', token.value)
    
    def peek_next_token(self) -> Token:
        """
        Mira el siguiente token sin consumirlo.
        
        Returns:
            Siguiente token
        """
        if self.current_token_index + 1 < len(self.tokens):
            return self.tokens[self.current_token_index + 1]
        return Token('EOF', '', -1)