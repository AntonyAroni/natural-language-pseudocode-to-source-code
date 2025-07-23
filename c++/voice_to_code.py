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
            return "algoritmo programa\ninicio\n  escribir(\"No se pudo transcribir el audio\")\nfin"
            
        return transcribed_text
    except Exception as e:
        print(f"Error al transcribir: {e}")
        return "algoritmo programa\ninicio\n  escribir(\"Error en la transcripción\")\nfin"

def process_transcription(text):
    """Procesa el texto transcrito para convertirlo en pseudocódigo válido."""
    # Normalizar el texto
    text = text.strip().lower()
    
    # Estructura básica del pseudocódigo
    if not text.startswith("algoritmo"):
        text = "algoritmo programa\n" + text
    
    if not "inicio" in text:
        text = text + "\ninicio\n"
    
    if not "fin" in text:
        text = text + "\nfin"
    
    # Reemplazar palabras comunes en la transcripción con sintaxis de pseudocódigo
    replacements = {
        "imprimir": "escribir",
        "mostrar": "escribir",
        "print": "escribir",
        "si": "si",
        "entonces": "entonces",
        "sino": "sino",
        "finsi": "finsi",
        "para": "para",
        "hasta": "hasta",
        "hacer": "hacer",
        "finpara": "finpara",
        "mientras": "mientras",
        "finmientras": "finmientras",
        "leer": "leer",
        "input": "leer",
        "variable": "var",
        "entero": "entero",
        "real": "real",
        "cadena": "cadena",
        "booleano": "booleano"
    }
    
    for old, new in replacements.items():
        # Reemplazar solo palabras completas
        text = text.replace(f" {old} ", f" {new} ")
        if text.startswith(old + " "):
            text = new + text[len(old):]
        if text.endswith(" " + old):
            text = text[:-len(old)] + new
    
    # Formatear el pseudocódigo para que sea más legible
    lines = text.split('\n')
    formatted_lines = []
    indent = 0
    
    for line in lines:
        line = line.strip()
        formatted_lines.append(line)
    
    return "\n".join(formatted_lines)

def save_pseudocode(text, filename="input.pseudo"):
    """Guarda el texto como pseudocódigo."""
    # Procesar el texto transcrito
    processed_text = process_transcription(text)
    
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
        
    parser = argparse.ArgumentParser(description="Convierte voz a código usando un modelo transformer")
    parser.add_argument("--duration", type=int, default=10, help="Duración de la grabación en segundos")
    parser.add_argument("--model", type=str, default="openai/whisper-base", help="Modelo de transformers a utilizar")
    parser.add_argument("--output", type=str, default="input.pseudo", help="Nombre del archivo de pseudocódigo")
    parser.add_argument("--compile", action="store_true", help="Compilar automáticamente el pseudocódigo")
    parser.add_argument("--example", action="store_true", help="Usar un ejemplo predefinido en lugar de grabar audio")
    parser.add_argument("--edit", action="store_true", help="Abrir el pseudocódigo en un editor antes de compilar")
    
    args = parser.parse_args()
    
    if args.example:
        # Usar ejemplo predefinido
        print("Usando ejemplo predefinido...")
        with open("ejemplo_valido.pseudo", "r") as f:
            text = f.read()
        pseudo_file = args.output
        with open(pseudo_file, "w") as f:
            f.write(text)
        print(f"Ejemplo guardado en: {pseudo_file}")
    else:
        # Grabar audio
        audio, sample_rate = record_audio(duration=args.duration)
        
        # Guardar audio temporalmente
        audio_file = save_audio(audio, sample_rate)
        
        # Transcribir audio a texto
        print("Transcribiendo audio...")
        text = transcribe_audio(audio_file, model_name=args.model)
        print(f"Texto transcrito: {text}")
        
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
    
    # Ya se eliminó el archivo de audio temporal en la sección correspondiente

if __name__ == "__main__":
    main()