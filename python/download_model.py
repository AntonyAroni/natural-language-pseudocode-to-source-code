#!/usr/bin/env python3
"""
Script para descargar el modelo pre-entrenado.
"""

import os
import sys
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import TRANSFORMER

def download_model():
    """Descarga el modelo pre-entrenado."""
    model_name = TRANSFORMER.get("model_name", "Salesforce/codegen-350M-mono")
    
    print(f"Descargando modelo {model_name}...")
    
    try:
        # Descargar el tokenizer
        print("Descargando tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Descargar el modelo
        print("Descargando modelo...")
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        print(f"Modelo {model_name} descargado correctamente.")
        return True
    except Exception as e:
        print(f"Error al descargar el modelo: {e}")
        return False

if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)