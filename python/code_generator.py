"""
Generador de código Python a partir del AST.
"""

import logging
from typing import Dict, List, Any, Optional

from syntax_analyzer import ASTNode
from semantic_analyzer import SemanticAnalyzer, SymbolTable
from utils import format_python_code

logger = logging.getLogger(__name__)

class CodeGenerator:
    """Generador de código Python a partir del AST."""

    def __init__(self, symbol_table: Optional[SymbolTable] = None):
        """
        Inicializa el generador de código.

        Args:
            symbol_table: Tabla de símbolos del análisis semántico
        """
        self.symbol_table = symbol_table
        self.indent_level = 0
        self.indent_size = 4
        logger.info("Generador de código inicializado")

    def generate(self, ast: ASTNode) -> str:
        """
        Genera código Python a partir del AST.

        Args:
            ast: Raíz del AST

        Returns:
            Código Python generado
        """
        try:
            code = self._generate_node(ast)
            formatted_code = format_python_code(code)
            logger.info("Generación de código completada con éxito")
            return formatted_code
        except Exception as e:
            logger.error(f"Error en la generación de código: {e}")
            return f"# Error en la generación de código: {e}"

    def _generate_node(self, node: ASTNode) -> str:
        """
        Genera código para un nodo del AST.

        Args:
            node: Nodo del AST

        Returns:
            Código Python generado para el nodo
        """
        if node.type == 'PROGRAM':
            return self._generate_program(node)
        elif node.type == 'FUNCTION_DEF':
            return self._generate_function_def(node)
        elif node.type == 'BLOCK':
            return self._generate_block(node)
        elif node.type == 'IF_STATEMENT':
            return self._generate_if_statement(node)
        elif node.type == 'FOR_LOOP':
            return self._generate_for_loop(node)
        elif node.type == 'WHILE_LOOP':
            return self._generate_while_loop(node)
        elif node.type == 'ASSIGNMENT':
            return self._generate_assignment(node)
        elif node.type == 'FUNCTION_CALL':
            return self._generate_function_call(node)
        elif node.type == 'VARIABLE':
            return self._generate_variable(node)
        elif node.type == 'LITERAL':
            return self._generate_literal(node)
        elif node.type == 'EXPRESSION':
            return self._generate_expression(node)
        elif node.type == 'CONDITION':
            return self._generate_condition(node)
        elif node.type == 'THEN':
            return self._generate_then(node)
        elif node.type == 'ELSE':
            return self._generate_else(node)
        elif node.type == 'PARAMETERS':
            return self._generate_parameters(node)
        elif node.type == 'ARGUMENTS':
            return self._generate_arguments(node)
        elif node.type == 'ITERABLE':
            return self._generate_iterable(node)
        elif node.type == 'BODY':
            return self._generate_body(node)
        else:
            # Nodo desconocido
            logger.warning(f"Tipo de nodo desconocido: {node.type}")
            return ""

    def _generate_program(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de programa.

        Args:
            node: Nodo de programa

        Returns:
            Código Python generado
        """
        code = "# Código generado automáticamente\n\n"

        for child in node.children:
            code += self._generate_node(child) + "\n\n"

        return code.rstrip()

    def _generate_function_def(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de definición de función.

        Args:
            node: Nodo de definición de función

        Returns:
            Código Python generado
        """
        function_name = node.value

        # Generar parámetros
        params_node = node.children[0]  # Primer hijo: parámetros
        params_code = self._generate_node(params_node)

        # Generar cuerpo de la función
        body_node = node.children[1]  # Segundo hijo: cuerpo

        # Incrementar nivel de indentación para el cuerpo
        self.indent_level += 1
        body_code = self._generate_node(body_node)
        self.indent_level -= 1

        # Si el cuerpo está vacío, agregar un pass
        if not body_code.strip():
            body_code = self._indent() + "pass"

        return f"def {function_name}({params_code}):\n{body_code}"

    def _generate_block(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de bloque.

        Args:
            node: Nodo de bloque

        Returns:
            Código Python generado
        """
        code = ""

        for child in node.children:
            child_code = self._generate_node(child)
            if child_code:
                code += self._indent() + child_code + "\n"

        return code

    def _generate_if_statement(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de declaración if.

        Args:
            node: Nodo de declaración if

        Returns:
            Código Python generado
        """
        # Generar condición
        condition_node = node.children[0]  # Primer hijo: condición
        condition_code = self._generate_node(condition_node)

        # Generar bloque then
        then_node = node.children[1]  # Segundo hijo: then

        # Incrementar nivel de indentación para el bloque then
        self.indent_level += 1
        then_code = self._generate_node(then_node)
        self.indent_level -= 1

        # Si el bloque then está vacío, agregar un pass
        if not then_code.strip():
            then_code = self._indent() + "pass\n"

        code = f"if {condition_code}:\n{then_code}"

        # Generar bloque else si existe
        if len(node.children) > 2:
            else_node = node.children[2]  # Tercer hijo: else

            # Incrementar nivel de indentación para el bloque else
            self.indent_level += 1
            else_code = self._generate_node(else_node)
            self.indent_level -= 1

            # Si el bloque else está vacío, agregar un pass
            if not else_code.strip():
                else_code = self._indent() + "pass\n"

            code += f"else:\n{else_code}"

        return code

    def _generate_for_loop(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de bucle for.

        Args:
            node: Nodo de bucle for

        Returns:
            Código Python generado
        """
        # Variable de iteración
        var_node = node.children[0]  # Primer hijo: variable
        var_code = self._generate_node(var_node)

        # Iterable
        iterable_node = node.children[1]  # Segundo hijo: iterable
        iterable_code = self._generate_node(iterable_node)

        # Cuerpo del bucle
        body_node = node.children[2]  # Tercer hijo: cuerpo

        # Incrementar nivel de indentación para el cuerpo
        self.indent_level += 1
        body_code = self._generate_node(body_node)
        self.indent_level -= 1

        # Si el cuerpo está vacío, agregar un pass
        if not body_code.strip():
            body_code = self._indent() + "pass\n"

        return f"for {var_code} in {iterable_code}:\n{body_code}"

    def _generate_while_loop(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de bucle while.

        Args:
            node: Nodo de bucle while

        Returns:
            Código Python generado
        """
        # Condición
        condition_node = node.children[0]  # Primer hijo: condición
        condition_code = self._generate_node(condition_node)

        # Cuerpo del bucle
        body_node = node.children[1]  # Segundo hijo: cuerpo

        # Incrementar nivel de indentación para el cuerpo
        self.indent_level += 1
        body_code = self._generate_node(body_node)
        self.indent_level -= 1

        # Si el cuerpo está vacío, agregar un pass
        if not body_code.strip():
            body_code = self._indent() + "pass\n"

        return f"while {condition_code}:\n{body_code}"

    def _generate_assignment(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de asignación.

        Args:
            node: Nodo de asignación

        Returns:
            Código Python generado
        """
        # Variable
        var_node = node.children[0]  # Primer hijo: variable
        var_code = self._generate_node(var_node)

        # Expresión
        expr_node = node.children[1]  # Segundo hijo: expresión
        expr_code = self._generate_node(expr_node)

        return f"{var_code} = {expr_code}"

    def _generate_function_call(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de llamada a función.

        Args:
            node: Nodo de llamada a función

        Returns:
            Código Python generado
        """
        function_name = node.value

        # Generar argumentos
        args_node = node.children[0]  # Primer hijo: argumentos
        args_code = self._generate_node(args_node)

        return f"{function_name}({args_code})"

    def _generate_variable(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de variable.

        Args:
            node: Nodo de variable

        Returns:
            Código Python generado
        """
        return node.value

    def _generate_literal(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de literal.

        Args:
            node: Nodo de literal

        Returns:
            Código Python generado
        """
        return str(node.value)

    def _generate_expression(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de expresión.

        Args:
            node: Nodo de expresión

        Returns:
            Código Python generado
        """
        return str(node.value)

    def _generate_condition(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de condición.

        Args:
            node: Nodo de condición

        Returns:
            Código Python generado
        """
        # Generar expresión de la condición
        if node.children:
            return self._generate_node(node.children[0])
        return ""

    def _generate_then(self, node: ASTNode) -> str:
        """
        Genera código para un nodo then.

        Args:
            node: Nodo then

        Returns:
            Código Python generado
        """
        # Generar bloque then
        if node.children:
            return self._generate_node(node.children[0])
        return ""

    def _generate_else(self, node: ASTNode) -> str:
        """
        Genera código para un nodo else.

        Args:
            node: Nodo else

        Returns:
            Código Python generado
        """
        # Generar bloque else
        if node.children:
            return self._generate_node(node.children[0])
        return ""

    def _generate_parameters(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de parámetros.

        Args:
            node: Nodo de parámetros

        Returns:
            Código Python generado
        """
        params = []

        for param in node.children:
            params.append(param.value)

        return ", ".join(params)

    def _generate_arguments(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de argumentos.

        Args:
            node: Nodo de argumentos

        Returns:
            Código Python generado
        """
        args = []

        for arg in node.children:
            args.append(self._generate_node(arg))

        return ", ".join(args)

    def _generate_iterable(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de iterable.

        Args:
            node: Nodo de iterable

        Returns:
            Código Python generado
        """
        # Generar expresión del iterable
        if node.children:
            return self._generate_node(node.children[0])
        return ""

    def _generate_body(self, node: ASTNode) -> str:
        """
        Genera código para un nodo de cuerpo.

        Args:
            node: Nodo de cuerpo

        Returns:
            Código Python generado
        """
        # Generar bloque del cuerpo
        if node.children:
            return self._generate_node(node.children[0])
        return ""

    def _indent(self) -> str:
        """
        Genera la indentación actual.

        Returns:
            String de indentación
        """
        return " " * (self.indent_level * self.indent_size)