#!/usr/bin/env python3
import os
import argparse
import torch
from transformers import pipeline
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import subprocess

def test_transcription(audio_file="test_audio.wav", model_name="openai/whisper-base"):
    """Prueba la transcripción de audio usando un modelo transformer."""
    try:
        print(f"Cargando modelo {model_name}...")
        transcriber = pipeline("automatic-speech-recognition", model=model_name)
        print("Transcribiendo audio...")
        result = transcriber(audio_file)
        
        print("\nResultado de la transcripción:")
        print(f"Tipo de resultado: {type(result)}")
        print(f"Contenido: {result}")
        
        if isinstance(result, dict) and "text" in result:
            transcribed_text = result["text"]
            print(f"\nTexto transcrito: {transcribed_text}")
        elif isinstance(result, str):
            transcribed_text = result
            print(f"\nTexto transcrito: {transcribed_text}")
        else:
            print("\nFormato de resultado inesperado")
            
        return result
    except Exception as e:
        print(f"Error al transcribir: {e}")
        return None

def record_test_audio(duration=5, sample_rate=16000, filename="test_audio.wav"):
    """Graba audio de prueba desde el micrófono."""
    print(f"Grabando {duration} segundos de audio de prueba...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    print("Grabación finalizada.")
    wav.write(filename, sample_rate, audio)
    print(f"Audio guardado en {filename}")
    return filename

def main():
    parser = argparse.ArgumentParser(description="Diagnóstico de transcripción de voz")
    parser.add_argument("--duration", type=int, default=5, help="Duración de la grabación en segundos")
    parser.add_argument("--model", type=str, default="openai/whisper-base", help="Modelo de transformers a utilizar")
    parser.add_argument("--file", type=str, help="Archivo de audio existente para probar (opcional)")
    
    args = parser.parse_args()
    
    # Verificar si CUDA está disponible
    print(f"CUDA disponible: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Dispositivo CUDA: {torch.cuda.get_device_name(0)}")
    
    # Usar archivo existente o grabar nuevo
    if args.file and os.path.exists(args.file):
        audio_file = args.file
        print(f"Usando archivo de audio existente: {audio_file}")
    else:
        audio_file = record_test_audio(duration=args.duration)
    
    # Probar transcripción
    result = test_transcription(audio_file, model_name=args.model)
    
    # Verificar si el resultado es válido
    if result:
        print("\nDiagnóstico: La transcripción funciona correctamente.")
    else:
        print("\nDiagnóstico: Hay problemas con la transcripción.")
        print("Sugerencias:")
        print("1. Verifica que el micrófono esté funcionando correctamente")
        print("2. Asegúrate de que todas las dependencias estén instaladas:")
        print("   pip install torch transformers sounddevice scipy numpy sentencepiece protobuf")
        print("3. Prueba con un modelo diferente, por ejemplo:")
        print("   python diagnose_transcription.py --model facebook/wav2vec2-base-960h")

if __name__ == "__main__":
    main()