#include "generator.h"
#include <sstream>
#include <set>

using namespace std;

class CodeGenerator {
public:
    ostringstream codigo;
    int indentLevel;
    set<string> declaredVars;
    
    CodeGenerator() : indentLevel(0) {}
    
    string indent() {
        return string(indentLevel * 4, ' ');
    }
    
    void generateNode(NodoAST* nodo) {
        if (!nodo) return;
        
        if (nodo->tipo == "PROGRAMA") {
            codigo << "#include <iostream>\n";
            codigo << "#include <string>\n";
            codigo << "using namespace std;\n\n";
            
            for (auto hijo : nodo->hijos) {
                generateNode(hijo);
            }
        }
        else if (nodo->tipo == "ALGORITMO") {
            codigo << "int main() {\n";
            indentLevel++;
            
            for (auto hijo : nodo->hijos) {
                generateNode(hijo);
            }
            
            indentLevel--;
            codigo << indent() << "return 0;\n";
            codigo << "}\n";
        }
        else if (nodo->tipo == "ESCRIBIR") {
            codigo << indent() << "cout << ";
            if (!nodo->hijos.empty()) {
                generateNode(nodo->hijos[0]);
            }
            codigo << " << endl;\n";
        }
        else if (nodo->tipo == "LEER") {
            codigo << indent() << "cin >> ";
            if (!nodo->hijos.empty()) {
                generateNode(nodo->hijos[0]);
            }
            codigo << ";\n";
        }
        else if (nodo->tipo == "SI") {
            codigo << indent() << "if (";
            if (!nodo->hijos.empty()) {
                generateNode(nodo->hijos[0]); // condición
            }
            codigo << ") {\n";
            
            indentLevel++;
            if (nodo->hijos.size() > 1) {
                generateNode(nodo->hijos[1]); // bloque then
            }
            indentLevel--;
            
            codigo << indent() << "}";
            
            if (nodo->hijos.size() > 2) { // bloque else
                codigo << " else {\n";
                indentLevel++;
                generateNode(nodo->hijos[2]);
                indentLevel--;
                codigo << indent() << "}";
            }
            codigo << "\n";
        }
        else if (nodo->tipo == "PARA") {
            codigo << indent() << "for (int " << nodo->valor << " = ";
            if (!nodo->hijos.empty()) {
                generateNode(nodo->hijos[0]); // inicio
            }
            codigo << "; " << nodo->valor << " <= ";
            if (nodo->hijos.size() > 1) {
                generateNode(nodo->hijos[1]); // fin
            }
            codigo << "; " << nodo->valor << "++) {\n";
            
            indentLevel++;
            if (nodo->hijos.size() > 2) {
                generateNode(nodo->hijos[2]); // bloque
            }
            indentLevel--;
            
            codigo << indent() << "}\n";
        }
        else if (nodo->tipo == "MIENTRAS") {
            codigo << indent() << "while (";
            if (!nodo->hijos.empty()) {
                generateNode(nodo->hijos[0]); // condición
            }
            codigo << ") {\n";
            
            indentLevel++;
            if (nodo->hijos.size() > 1) {
                generateNode(nodo->hijos[1]); // bloque
            }
            indentLevel--;
            
            codigo << indent() << "}\n";
        }
        else if (nodo->tipo == "ASIGNACION") {
            if (declaredVars.find(nodo->valor) == declaredVars.end()) {
                codigo << indent() << "int " << nodo->valor << " = ";
                declaredVars.insert(nodo->valor);
            } else {
                codigo << indent() << nodo->valor << " = ";
            }
            if (!nodo->hijos.empty()) {
                generateNode(nodo->hijos[0]);
            }
            codigo << ";\n";
        }
        else if (nodo->tipo == "BLOQUE") {
            for (auto hijo : nodo->hijos) {
                generateNode(hijo);
            }
        }
        else if (nodo->tipo == "NUMERO") {
            codigo << nodo->valor;
        }
        else if (nodo->tipo == "CADENA") {
            codigo << "\"" << nodo->valor << "\"";
        }
        else if (nodo->tipo == "IDENTIFICADOR") {
            codigo << nodo->valor;
        }
        else if (nodo->tipo == "OPERACION_BINARIA") {
            if (nodo->hijos.size() >= 2) {
                generateNode(nodo->hijos[0]);
                codigo << " " << nodo->valor << " ";
                generateNode(nodo->hijos[1]);
            }
        }
    }
};

string generarCodigo(NodoAST* arbol) {
    CodeGenerator generator;
    generator.generateNode(arbol);
    return generator.codigo.str();
}