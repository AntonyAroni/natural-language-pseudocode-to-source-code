"""
Analizador semántico para el sistema de conversión de voz a código Python.
"""

import logging
from typing import Dict, List, Any, Set, Optional

from syntax_analyzer import ASTNode

logger = logging.getLogger(__name__)

class Symbol:
    """Clase para representar un símbolo en la tabla de símbolos."""
    
    def __init__(self, name: str, symbol_type: str, scope: str, value: Any = None):
        """
        Inicializa un símbolo.
        
        Args:
            name: Nombre del símbolo
            symbol_type: Tipo del símbolo (variable, función, etc.)
            scope: Ámbito del símbolo
            value: Valor asociado al símbolo
        """
        self.name = name
        self.type = symbol_type
        self.scope = scope
        self.value = value
    
    def __str__(self) -> str:
        return f"Symbol({self.name}, {self.type}, scope={self.scope})"
    
    def __repr__(self) -> str:
        return self.__str__()

class SymbolTable:
    """Tabla de símbolos para el análisis semántico."""
    
    def __init__(self):
        """Inicializa la tabla de símbolos."""
        self.symbols: Dict[str, Dict[str, Symbol]] = {"global": {}}
        self.current_scope = "global"
    
    def enter_scope(self, scope_name: str):
        """
        Entra en un nuevo ámbito.
        
        Args:
            scope_name: Nombre del nuevo ámbito
        """
        if scope_name not in self.symbols:
            self.symbols[scope_name] = {}
        self.current_scope = scope_name
    
    def exit_scope(self):
        """Sale del ámbito actual y vuelve al ámbito global."""
        self.current_scope = "global"
    
    def add_symbol(self, name: str, symbol_type: str, value: Any = None) -> Symbol:
        """
        Agrega un símbolo al ámbito actual.
        
        Args:
            name: Nombre del símbolo
            symbol_type: Tipo del símbolo
            value: Valor asociado al símbolo
            
        Returns:
            Símbolo creado
        """
        symbol = Symbol(name, symbol_type, self.current_scope, value)
        self.symbols[self.current_scope][name] = symbol
        return symbol
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """
        Busca un símbolo en el ámbito actual y en el ámbito global.
        
        Args:
            name: Nombre del símbolo a buscar
            
        Returns:
            Símbolo encontrado o None si no existe
        """
        # Buscar primero en el ámbito actual
        if name in self.symbols[self.current_scope]:
            return self.symbols[self.current_scope][name]
        
        # Si no se encuentra en el ámbito actual, buscar en el ámbito global
        if name in self.symbols["global"]:
            return self.symbols["global"][name]
        
        return None

class SemanticError(Exception):
    """Excepción para errores semánticos."""
    pass

class SemanticAnalyzer:
    """Analizador semántico para verificar la corrección semántica del AST."""
    
    def __init__(self):
        """Inicializa el analizador semántico."""
        self.symbol_table = SymbolTable()
        self.errors: List[str] = []
        logger.info("Analizador semántico inicializado")
    
    def analyze(self, ast: ASTNode) -> bool:
        """
        Analiza un AST para verificar su corrección semántica.
        
        Args:
            ast: Raíz del AST a analizar
            
        Returns:
            True si el análisis es exitoso, False si hay errores
        """
        self.errors = []
        
        try:
            self._analyze_node(ast)
            
            if not self.errors:
                logger.info("Análisis semántico completado con éxito")
                return True
            else:
                logger.error(f"Análisis semántico completado con {len(self.errors)} errores")
                for error in self.errors:
                    logger.error(f"Error semántico: {error}")
                return False
        except Exception as e:
            logger.error(f"Error en el análisis semántico: {e}")
            return False
    
    def _analyze_node(self, node: ASTNode):
        """
        Analiza un nodo del AST.
        
        Args:
            node: Nodo a analizar
        """
        if node.type == 'PROGRAM':
            self._analyze_program(node)
        elif node.type == 'FUNCTION_DEF':
            self._analyze_function_def(node)
        elif node.type == 'BLOCK':
            self._analyze_block(node)
        elif node.type == 'IF_STATEMENT':
            self._analyze_if_statement(node)
        elif node.type == 'FOR_LOOP':
            self._analyze_for_loop(node)
        elif node.type == 'WHILE_LOOP':
            self._analyze_while_loop(node)
        elif node.type == 'ASSIGNMENT':
            self._analyze_assignment(node)
        elif node.type == 'FUNCTION_CALL':
            self._analyze_function_call(node)
        elif node.type == 'VARIABLE':
            self._analyze_variable(node)
        else:
            # Analizar recursivamente los nodos hijos
            for child in node.children:
                self._analyze_node(child)
    
    def _analyze_program(self, node: ASTNode):
        """
        Analiza un nodo de programa.
        
        Args:
            node: Nodo de programa
        """
        # Analizar cada declaración en el programa
        for child in node.children:
            self._analyze_node(child)
    
    def _analyze_function_def(self, node: ASTNode):
        """
        Analiza un nodo de definición de función.
        
        Args:
            node: Nodo de definición de función
        """
        function_name = node.value
        
        # Verificar si la función ya está definida
        if self.symbol_table.lookup(function_name):
            self.errors.append(f"Función '{function_name}' ya definida")
        
        # Agregar la función a la tabla de símbolos
        self.symbol_table.add_symbol(function_name, 'FUNCTION')
        
        # Entrar en el ámbito de la función
        self.symbol_table.enter_scope(function_name)
        
        # Analizar parámetros
        params_node = node.children[0]  # Primer hijo: parámetros
        for param in params_node.children:
            param_name = param.value
            self.symbol_table.add_symbol(param_name, 'PARAMETER')
        
        # Analizar cuerpo de la función
        body_node = node.children[1]  # Segundo hijo: cuerpo
        self._analyze_node(body_node)
        
        # Salir del ámbito de la función
        self.symbol_table.exit_scope()
    
    def _analyze_block(self, node: ASTNode):
        """
        Analiza un nodo de bloque.
        
        Args:
            node: Nodo de bloque
        """
        # Analizar cada declaración en el bloque
        for child in node.children:
            self._analyze_node(child)
    
    def _analyze_if_statement(self, node: ASTNode):
        """
        Analiza un nodo de declaración if.
        
        Args:
            node: Nodo de declaración if
        """
        # Analizar condición
        condition_node = node.children[0]  # Primer hijo: condición
        self._analyze_node(condition_node)
        
        # Analizar bloque then
        then_node = node.children[1]  # Segundo hijo: then
        self._analyze_node(then_node)
        
        # Analizar bloque else si existe
        if len(node.children) > 2:
            else_node = node.children[2]  # Tercer hijo: else
            self._analyze_node(else_node)
    
    def _analyze_for_loop(self, node: ASTNode):
        """
        Analiza un nodo de bucle for.
        
        Args:
            node: Nodo de bucle for
        """
        # Variable de iteración
        var_node = node.children[0]  # Primer hijo: variable
        var_name = var_node.value
        
        # Agregar la variable a la tabla de símbolos
        self.symbol_table.add_symbol(var_name, 'VARIABLE')
        
        # Analizar iterable
        iterable_node = node.children[1]  # Segundo hijo: iterable
        self._analyze_node(iterable_node)
        
        # Analizar cuerpo del bucle
        body_node = node.children[2]  # Tercer hijo: cuerpo
        self._analyze_node(body_node)
    
    def _analyze_while_loop(self, node: ASTNode):
        """
        Analiza un nodo de bucle while.
        
        Args:
            node: Nodo de bucle while
        """
        # Analizar condición
        condition_node = node.children[0]  # Primer hijo: condición
        self._analyze_node(condition_node)
        
        # Analizar cuerpo del bucle
        body_node = node.children[1]  # Segundo hijo: cuerpo
        self._analyze_node(body_node)
    
    def _analyze_assignment(self, node: ASTNode):
        """
        Analiza un nodo de asignación.
        
        Args:
            node: Nodo de asignación
        """
        # Variable
        var_node = node.children[0]  # Primer hijo: variable
        var_name = var_node.value
        
        # Verificar si la variable ya está definida
        if not self.symbol_table.lookup(var_name):
            # Si no está definida, agregarla a la tabla de símbolos
            self.symbol_table.add_symbol(var_name, 'VARIABLE')
        
        # Analizar expresión
        expr_node = node.children[1]  # Segundo hijo: expresión
        self._analyze_node(expr_node)
    
    def _analyze_function_call(self, node: ASTNode):
        """
        Analiza un nodo de llamada a función.
        
        Args:
            node: Nodo de llamada a función
        """
        function_name = node.value
        
        # Verificar si la función está definida
        function_symbol = self.symbol_table.lookup(function_name)
        if not function_symbol:
            self.errors.append(f"Función '{function_name}' no definida")
        elif function_symbol.type != 'FUNCTION':
            self.errors.append(f"'{function_name}' no es una función")
        
        # Analizar argumentos
        args_node = node.children[0]  # Primer hijo: argumentos
        for arg in args_node.children:
            self._analyze_node(arg)
    
    def _analyze_variable(self, node: ASTNode):
        """
        Analiza un nodo de variable.
        
        Args:
            node: Nodo de variable
        """
        var_name = node.value
        
        # Verificar si la variable está definida
        if not self.symbol_table.lookup(var_name):
            self.errors.append(f"Variable '{var_name}' no definida")
    
    def get_symbol_table(self) -> SymbolTable:
        """
        Obtiene la tabla de símbolos.
        
        Returns:
            Tabla de símbolos
        """
        return self.symbol_table
    
    def get_errors(self) -> List[str]:
        """
        Obtiene la lista de errores semánticos.
        
        Returns:
            Lista de errores
        """
        return self.errors