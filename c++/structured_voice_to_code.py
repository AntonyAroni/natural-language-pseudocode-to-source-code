#!/usr/bin/env python3
import os
import argparse
import torch
from transformers import pipeline
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import subprocess

def record_audio(duration=5, sample_rate=16000):
    """Graba audio desde el micrófono."""
    print(f"Grabando por {duration} segundos...")
    print("Habla las instrucciones de forma estructurada (por ejemplo: 'algoritmo suma, declarar variable x, leer x, si x mayor que cero, escribir x...')")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    print("Grabación finalizada.")
    return audio, sample_rate

def save_audio(audio, sample_rate, filename="temp_audio.wav"):
    """Guarda el audio en un archivo WAV."""
    wav.write(filename, sample_rate, audio)
    return filename

def transcribe_audio(audio_file, model_name="openai/whisper-base"):
    """Transcribe el audio a texto usando un modelo transformer."""
    try:
        print(f"Cargando modelo {model_name}...")
        transcriber = pipeline("automatic-speech-recognition", model=model_name)
        print("Transcribiendo audio...")
        result = transcriber(audio_file)
        
        # Verificar el resultado
        if isinstance(result, dict) and "text" in result:
            transcribed_text = result["text"]
        elif isinstance(result, str):
            transcribed_text = result
        else:
            print(f"Formato de resultado inesperado: {type(result)}")
            print(f"Contenido: {result}")
            transcribed_text = str(result)
            
        if not transcribed_text.strip():
            print("ADVERTENCIA: La transcripción está vacía.")
            return ""
            
        return transcribed_text
    except Exception as e:
        print(f"Error al transcribir: {e}")
        return ""

def convert_to_pseudocode(text):
    """Convierte instrucciones estructuradas a pseudocódigo."""
    # Normalizar el texto
    text = text.strip().lower()
    
    # Palabras clave para reconocer
    keywords = {
        "algoritmo": "algoritmo",
        "declarar": "var",
        "variable": "var",
        "entero": "entero",
        "real": "real",
        "cadena": "cadena",
        "leer": "leer",
        "escribir": "escribir",
        "imprimir": "escribir",
        "mostrar": "escribir",
        "si": "si",
        "entonces": "entonces",
        "sino": "sino",
        "fin si": "finsi",
        "finsi": "finsi",
        "para": "para",
        "desde": "desde",
        "hasta": "hasta",
        "hacer": "hacer",
        "fin para": "finpara",
        "finpara": "finpara",
        "mientras": "mientras",
        "fin mientras": "finmientras",
        "finmientras": "finmientras"
    }
    
    # Estructura básica
    if not any(text.startswith(k) for k in ["algoritmo", "programa"]):
        text = "algoritmo programa\n" + text
    
    if "inicio" not in text:
        # Buscar la primera instrucción después del nombre del algoritmo
        lines = text.split("\n")
        if len(lines) > 1:
            # Insertar "inicio" después de la primera línea
            text = lines[0] + "\ninicio\n" + "\n".join(lines[1:])
        else:
            text = text + "\ninicio\n"
    
    if "fin" not in text.split():
        text = text + "\nfin"
    
    # Procesar el texto línea por línea para aplicar formato
    lines = text.split("\n")
    formatted_lines = []
    indent_level = 0
    
    for line in lines:
        line = line.strip()
        
        # Ajustar indentación basada en palabras clave
        if any(k in line for k in ["finsi", "fin si", "finpara", "fin para", "finmientras", "fin mientras"]):
            indent_level = max(0, indent_level - 1)
        
        # Aplicar indentación
        if line and indent_level > 0:
            formatted_line = "  " * indent_level + line
        else:
            formatted_line = line
        
        formatted_lines.append(formatted_line)
        
        # Ajustar indentación para la siguiente línea
        if any(k in line for k in ["si", "para", "mientras"]) and "fin" not in line:
            indent_level += 1
    
    return "\n".join(formatted_lines)

def save_pseudocode(text, filename="input.pseudo"):
    """Guarda el texto como pseudocódigo."""
    # Convertir a pseudocódigo
    processed_text = convert_to_pseudocode(text)
    
    print("\nPseudocódigo generado:")
    print("--------------------")
    print(processed_text)
    print("--------------------\n")
    
    # Asegurarse de que el texto no esté vacío
    if not processed_text.strip():
        processed_text = "algoritmo programa\ninicio\n  escribir(\"Texto transcrito vacío\")\nfin"
        print("ADVERTENCIA: La transcripción estaba vacía. Se ha generado un pseudocódigo básico.")
    
    with open(filename, "w") as f:
        f.write(processed_text)
    
    return filename

def compile_pseudocode(pseudo_file, compiler_path="./build/proyecto_compiladores"):
    """Compila el pseudocódigo usando el compilador C++."""
    try:
        result = subprocess.run([compiler_path, pseudo_file], 
                               capture_output=True, text=True)
        if result.returncode == 0:
            print("Compilación exitosa:")
            print(result.stdout)
        else:
            print("Error en la compilación:")
            print(result.stderr)
    except Exception as e:
        print(f"Error al ejecutar el compilador: {e}")

def check_dependencies():
    """Verifica que las dependencias externas estén instaladas."""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True)
        return True
    except FileNotFoundError:
        print("ERROR: ffmpeg no está instalado. Por favor instálalo con:")
        print("sudo apt-get update && sudo apt-get install -y ffmpeg")
        return False

def verify_pseudocode(filename):
    """Verifica si el pseudocódigo generado tiene la estructura básica necesaria."""
    with open(filename, 'r') as f:
        content = f.read()
    
    required_elements = ["algoritmo", "inicio", "fin"]
    missing = [elem for elem in required_elements if elem not in content.lower()]
    
    if missing:
        print(f"ADVERTENCIA: El pseudocódigo generado puede no ser válido. Faltan elementos: {', '.join(missing)}")
        return False
    return True

def main():
    # Verificar dependencias
    if not check_dependencies():
        return
        
    parser = argparse.ArgumentParser(description="Convierte instrucciones habladas a pseudocódigo")
    parser.add_argument("--duration", type=int, default=15, help="Duración de la grabación en segundos")
    parser.add_argument("--model", type=str, default="openai/whisper-base", help="Modelo de transformers a utilizar")
    parser.add_argument("--output", type=str, default="input.pseudo", help="Nombre del archivo de pseudocódigo")
    parser.add_argument("--compile", action="store_true", help="Compilar automáticamente el pseudocódigo")
    parser.add_argument("--edit", action="store_true", help="Abrir el pseudocódigo en un editor antes de compilar")
    
    args = parser.parse_args()
    
    # Grabar audio
    audio, sample_rate = record_audio(duration=args.duration)
    
    # Guardar audio temporalmente
    audio_file = save_audio(audio, sample_rate)
    
    # Transcribir audio a texto
    print("Transcribiendo audio...")
    text = transcribe_audio(audio_file, model_name=args.model)
    print(f"Texto transcrito: {text}")
    
    if not text:
        print("Error: No se pudo transcribir el audio. Intenta de nuevo.")
        os.remove(audio_file)
        return
    
    # Guardar como pseudocódigo
    pseudo_file = save_pseudocode(text, filename=args.output)
    print(f"Pseudocódigo guardado en: {pseudo_file}")
    
    # Eliminar archivo de audio temporal
    os.remove(audio_file)
    
    # Abrir en editor si se solicita
    if args.edit:
        editor = os.environ.get("EDITOR", "nano")
        subprocess.run([editor, pseudo_file])
    
    # Verificar si el pseudocódigo es válido
    is_valid = verify_pseudocode(pseudo_file)
    
    # Compilar si se solicita y el pseudocódigo es válido
    if args.compile:
        if is_valid:
            print("Compilando pseudocódigo...")
            compile_pseudocode(pseudo_file)
        else:
            print("No se compiló debido a posibles problemas en el pseudocódigo.")
            print("Puedes editar el archivo manualmente y luego compilarlo con:")
            print(f"./build/proyecto_compiladores {pseudo_file}")

if __name__ == "__main__":
    main()