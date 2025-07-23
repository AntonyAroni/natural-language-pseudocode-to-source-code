#ifndef LEXER_H
#define LEXER_H

#include <vector>
#include <string>

using namespace std;

enum TipoToken {
    PALABRA_RESERVADA,
    IDENTIFICADOR,
    NUMERO,
    CADENA,
    OPERADOR,
    SIMBOLO,
    COMENTARIO,
    FIN_DE_LINEA,
    DESCONOCIDO
};

struct Token {
    TipoToken tipo;
    string valor;
    int linea;
};

vector<Token> analizarLexico(const string& codigo);

// Palabras reservadas del pseudocódigo
const vector<string> PALABRAS_RESERVADAS = {
    "Algoritmo", "FinAlgoritmo", "Proceso", "FinProceso",
    "SubProceso", "FinSubProceso", "Si", "Entonces",
    "Sino", "FinSi", "Segun", "FinSegun", "Para",
    "FinPara", "Mientras", "FinMientras", "Repetir",
    "Hasta", "Escribir", "Leer", "Funcion", "FinFuncion",
    "Retornar", "Verdadero", "Falso"
};

#endif