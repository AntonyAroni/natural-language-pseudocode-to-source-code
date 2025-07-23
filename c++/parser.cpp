#include "parser.h"
#include <stdexcept>

using namespace std;

class Parser {
public:
    vector<Token> tokens;
    size_t pos;
    
    Parser(const vector<Token>& t) : tokens(t), pos(0) {}
    
    Token peek() { return pos < tokens.size() ? tokens[pos] : Token{DESCONOCIDO, "", 0}; }
    Token consume() { return pos < tokens.size() ? tokens[pos++] : Token{DESCONOCIDO, "", 0}; }
    bool match(const string& valor) { return peek().valor == valor; }
    
    NodoAST* parsePrograma() {
        NodoAST* programa = new NodoAST{"PROGRAMA", ""};
        
        if (match("Algoritmo")) {
            programa->hijos.push_back(parseAlgoritmo());
        }
        
        return programa;
    }
    
    NodoAST* parseAlgoritmo() {
        consume(); // "Algoritmo"
        Token nombre = consume();
        
        NodoAST* algoritmo = new NodoAST{"ALGORITMO", nombre.valor};
        
        while (!match("FinAlgoritmo") && pos < tokens.size()) {
            algoritmo->hijos.push_back(parseStatement());
        }
        
        if (match("FinAlgoritmo")) consume();
        
        return algoritmo;
    }
    
    NodoAST* parseStatement() {
        if (match("Escribir")) return parseEscribir();
        if (match("Leer")) return parseLeer();
        if (match("Si")) return parseSi();
        if (match("Para")) return parsePara();
        if (match("Mientras")) return parseMientras();
        if (peek().tipo == IDENTIFICADOR) return parseAsignacion();
        
        // Skip unknown tokens
        consume();
        return nullptr;
    }
    
    NodoAST* parseEscribir() {
        consume(); // "Escribir"
        NodoAST* escribir = new NodoAST{"ESCRIBIR", ""};
        escribir->hijos.push_back(parseExpresion());
        return escribir;
    }
    
    NodoAST* parseLeer() {
        consume(); // "Leer"
        NodoAST* leer = new NodoAST{"LEER", ""};
        Token var = consume();
        leer->hijos.push_back(new NodoAST{"IDENTIFICADOR", var.valor});
        return leer;
    }
    
    NodoAST* parseSi() {
        consume(); // "Si"
        NodoAST* si = new NodoAST{"SI", ""};
        si->hijos.push_back(parseExpresion()); // condición
        
        if (match("Entonces")) consume();
        
        NodoAST* bloqueThen = new NodoAST{"BLOQUE", ""};
        while (!match("Sino") && !match("FinSi") && pos < tokens.size()) {
            NodoAST* stmt = parseStatement();
            if (stmt) bloqueThen->hijos.push_back(stmt);
        }
        si->hijos.push_back(bloqueThen);
        
        if (match("Sino")) {
            consume();
            NodoAST* bloqueElse = new NodoAST{"BLOQUE", ""};
            while (!match("FinSi") && pos < tokens.size()) {
                NodoAST* stmt = parseStatement();
                if (stmt) bloqueElse->hijos.push_back(stmt);
            }
            si->hijos.push_back(bloqueElse);
        }
        
        if (match("FinSi")) consume();
        return si;
    }
    
    NodoAST* parsePara() {
        consume(); // "Para"
        Token var = consume();
        consume(); // "<-" or "="
        
        NodoAST* para = new NodoAST{"PARA", var.valor};
        para->hijos.push_back(parseExpresion()); // inicio
        
        if (match("Hasta")) {
            consume();
            para->hijos.push_back(parseExpresion()); // fin
        }
        
        NodoAST* bloque = new NodoAST{"BLOQUE", ""};
        while (!match("FinPara") && pos < tokens.size()) {
            NodoAST* stmt = parseStatement();
            if (stmt) bloque->hijos.push_back(stmt);
        }
        para->hijos.push_back(bloque);
        
        if (match("FinPara")) consume();
        return para;
    }
    
    NodoAST* parseMientras() {
        consume(); // "Mientras"
        NodoAST* mientras = new NodoAST{"MIENTRAS", ""};
        mientras->hijos.push_back(parseExpresion()); // condición
        
        NodoAST* bloque = new NodoAST{"BLOQUE", ""};
        while (!match("FinMientras") && pos < tokens.size()) {
            NodoAST* stmt = parseStatement();
            if (stmt) bloque->hijos.push_back(stmt);
        }
        mientras->hijos.push_back(bloque);
        
        if (match("FinMientras")) consume();
        return mientras;
    }
    
    NodoAST* parseAsignacion() {
        Token var = consume();
        consume(); // "<-" or "="
        
        NodoAST* asignacion = new NodoAST{"ASIGNACION", var.valor};
        asignacion->hijos.push_back(parseExpresion());
        return asignacion;
    }
    
    NodoAST* parseExpresion() {
        NodoAST* left = parseTerm();
        
        while (pos < tokens.size() && (peek().valor == "+" || peek().valor == "-" || 
               peek().valor == ">" || peek().valor == "<" || peek().valor == "<=" || 
               peek().valor == ">=" || peek().valor == "==" || peek().valor == "!=")) {
            Token op = consume();
            NodoAST* right = parseTerm();
            
            NodoAST* binOp = new NodoAST{"OPERACION_BINARIA", op.valor};
            binOp->hijos.push_back(left);
            binOp->hijos.push_back(right);
            left = binOp;
        }
        
        return left;
    }
    
    NodoAST* parseTerm() {
        Token token = consume();
        
        if (token.tipo == NUMERO) {
            return new NodoAST{"NUMERO", token.valor};
        } else if (token.tipo == CADENA) {
            return new NodoAST{"CADENA", token.valor};
        } else if (token.tipo == IDENTIFICADOR) {
            return new NodoAST{"IDENTIFICADOR", token.valor};
        }
        
        return new NodoAST{"EXPRESION", token.valor};
    }
};

NodoAST* analizarSintaxis(const vector<Token>& tokens) {
    try {
        Parser parser(tokens);
        return parser.parsePrograma();
    } catch (const exception& e) {
        throw runtime_error(string("Error de sintaxis: ") + e.what());
    }
}