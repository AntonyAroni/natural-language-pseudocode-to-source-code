#include "lexer.h"
#include <cctype>
#include <algorithm>

using namespace std;

vector<Token> analizarLexico(const string& codigo) {
    vector<Token> tokens;
    int linea = 1;
    size_t i = 0;
    size_t n = codigo.length();

    while (i < n) {
        // Saltar espacios en blanco
        if (isspace(codigo[i])) {
            if (codigo[i] == '\n') linea++;
            i++;
            continue;
        }

        // Comentarios (//)
        if (i + 1 < n && codigo[i] == '/' && codigo[i+1] == '/') {
            while (i < n && codigo[i] != '\n') i++;
            linea++;
            continue;
        }

        // Identificadores y palabras reservadas
        if (isalpha(codigo[i])) {
            size_t start = i;
            while (i < n && (isalnum(codigo[i]) || codigo[i] == '_')) i++;

            string valor = codigo.substr(start, i - start);
            TipoToken tipo = (find(PALABRAS_RESERVADAS.begin(), PALABRAS_RESERVADAS.end(), valor) != PALABRAS_RESERVADAS.end())
                            ? PALABRA_RESERVADA : IDENTIFICADOR;

            tokens.push_back({tipo, valor, linea});
            continue;
        }

        // Números
        if (isdigit(codigo[i])) {
            size_t start = i;
            while (i < n && isdigit(codigo[i])) i++;
            tokens.push_back({NUMERO, codigo.substr(start, i - start), linea});
            continue;
        }

        // Cadenas
        if (codigo[i] == '"') {
            size_t start = ++i;
            while (i < n && codigo[i] != '"') {
                if (codigo[i] == '\n') linea++;
                i++;
            }
            tokens.push_back({CADENA, codigo.substr(start, i - start), linea});
            if (i < n) i++; // Saltar la comilla de cierre
            continue;
        }

        // Operadores y símbolos
        string op(1, codigo[i]);
        if (i + 1 < n) {
            string posibleOp = op + codigo[i+1];
            if (posibleOp == "<=" || posibleOp == ">=" || posibleOp == "==" || posibleOp == "!=" || posibleOp == "<-") {
                tokens.push_back({OPERADOR, posibleOp, linea});
                i += 2;
                continue;
            }
        }
        
        // Operadores simples
        if (op == "+" || op == "-" || op == "*" || op == "/" || op == "=" || 
            op == "<" || op == ">" || op == "(" || op == ")" || op == ",") {
            tokens.push_back({OPERADOR, op, linea});
        } else {
            tokens.push_back({SIMBOLO, op, linea});
        }
        i++;
    }

    return tokens;
}