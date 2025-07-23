#include <iostream>
#include <fstream>
#include <string>
#include "lexer.h"
#include "parser.h"
#include "generator.h"
#include "utils.h"

using namespace std;

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cerr << "Uso: " << argv[0] << " <archivo.pseudo>" << endl;
        return 1;
    }

    string filename = argv[1];
    string sourceCode = leerArchivo(filename);

    if (sourceCode.empty()) {
        cerr << "Error: No se pudo leer el archivo o está vacío." << endl;
        return 1;
    }

    // Fase 1: Análisis léxico
    vector<Token> tokens = analizarLexico(sourceCode);

    // Fase 2: Análisis sintáctico
    NodoAST* arbol = analizarSintaxis(tokens);

    // Fase 3: Generación de código
    string codigoCpp = generarCodigo(arbol);

    // Guardar el resultado
    string outputFilename = cambiarExtension(filename, ".cpp");
    guardarArchivo(outputFilename, codigoCpp);

    cout << "Compilación exitosa. Código C++ generado en: " << outputFilename << endl;

    return 0;
}