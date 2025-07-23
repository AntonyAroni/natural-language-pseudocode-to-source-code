#ifndef GENERATOR_H
#define GENERATOR_H

#include "parser.h"
#include <string>
#include <map>

string generarCodigo(NodoAST* arbol);

// Mapeo de pseudocódigo a C++
const map<string, string> MAPEO_FUNCIONES = {
    {"Escribir", "cout <<"},
    {"Leer", "cin >>"}
};

#endif