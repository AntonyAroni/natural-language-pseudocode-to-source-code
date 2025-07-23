#include "utils.h"
#include <fstream>
#include <sstream>
#include <iostream>

string leerArchivo(const string& filename) {
    ifstream file(filename);
    if (!file.is_open()) {
        return "";
    }
    
    stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

void guardarArchivo(const string& filename, const string& contenido) {
    // Extraer el nombre del archivo sin la ruta
    string basename = filename;
    size_t lastSlash = filename.find_last_of("/\\");
    if (lastSlash != string::npos) {
        basename = filename.substr(lastSlash + 1);
    }
    
    // Construir la ruta en cmake-build-debug
    string outputPath = basename;
    
    ofstream file(outputPath);
    if (file.is_open()) {
        file << contenido;
        std::cout << "Archivo guardado en: " << outputPath << endl;
    } else {
        std::cerr << "Error: No se pudo guardar en " << outputPath << ". Intentando en ubicación original." << endl;
        // Fallback a la ubicación original
        ofstream originalFile(filename);
        if (originalFile.is_open()) {
            originalFile << contenido;
        }
    }
}

string cambiarExtension(const string& filename, const string& nuevaExtension) {
    size_t lastdot = filename.find_last_of(".");
    if (lastdot == string::npos) return filename + nuevaExtension;
    return filename.substr(0, lastdot) + nuevaExtension;
}