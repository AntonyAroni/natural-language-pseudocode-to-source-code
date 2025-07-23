#ifndef PARSER_H
#define PARSER_H

#include "lexer.h"
#include <vector>

struct NodoAST {
    string tipo;
    string valor;
    vector<NodoAST*> hijos;

    ~NodoAST() {
        for (auto hijo : hijos) {
            delete hijo;
        }
    }
};

NodoAST* analizarSintaxis(const vector<Token>& tokens);

#endif