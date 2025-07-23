#ifndef UTILS_H
#define UTILS_H

#include <string>
#include <fstream>

using namespace std;

string leerArchivo(const string& filename);
void guardarArchivo(const string& filename, const string& contenido);
string cambiarExtension(const string& filename, const string& nuevaExtension);

#endif