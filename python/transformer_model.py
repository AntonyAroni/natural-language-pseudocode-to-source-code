"""
Módulo para el modelo transformer que convierte instrucciones en lenguaje natural a código Python.
"""

import logging
import re
from typing import Dict, Any, Optional

from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

from config import TRANSFORMER
from utils import normalize_text

logger = logging.getLogger(__name__)

class TransformerModel:
    """Clase para manejar el modelo transformer."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicializa el modelo transformer.
        
        Args:
            config: Configuración para el modelo
        """
        self.config = config or TRANSFORMER
        self.model_name = self.config.get("model_name", "gpt2")
        self.max_length = self.config.get("max_length", 512)
        self.temperature = self.config.get("temperature", 0.7)
        self.top_p = self.config.get("top_p", 0.9)
        
        # Cargar el modelo pre-entrenado
        try:
            logger.info(f"Cargando modelo transformer: {self.model_name}")
            print(f"Cargando modelo transformer: {self.model_name}...")
            
            # Intentar cargar el modelo y tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Crear el pipeline de generación de texto
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if torch.cuda.is_available() else -1
            )
            
            logger.info("Modelo transformer cargado correctamente")
            print("Modelo transformer cargado correctamente")
            self.model_loaded = True
        except Exception as e:
            logger.error(f"Error al cargar el modelo transformer: {e}")
            print(f"Error al cargar el modelo transformer: {e}")
            print("Se usará un sistema basado en patrones como fallback")
            self.model_loaded = False
            
            # Patrones para fallback
            self._init_fallback_patterns()
    
    def _init_fallback_patterns(self):
        """Inicializa los patrones de fallback."""
        self.patterns = {
            # Patrones para funciones
            "factorial": {
                "regex": r"(crear|hacer|definir)\s+(una\s+)?funci[oó]n\s+.*(factorial).*",
                "pseudocode": """def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)
"""
            },
            "suma": {
                "regex": r"(crear|hacer|definir)\s+(una\s+)?funci[oó]n\s+.*(sum[a|ar]).*",
                "pseudocode": """def sumar(a, b):
    return a + b
"""
            },
            "resta": {
                "regex": r"(crear|hacer|definir)\s+(una\s+)?funci[oó]n\s+.*(rest[a|ar]).*",
                "pseudocode": """def restar(a, b):
    return a - b
"""
            },
            "multiplicacion": {
                "regex": r"(crear|hacer|definir)\s+(una\s+)?funci[oó]n\s+.*(multiplic[a|ar]).*",
                "pseudocode": """def multiplicar(a, b):
    return a * b
"""
            },
            "division": {
                "regex": r"(crear|hacer|definir)\s+(una\s+)?funci[oó]n\s+.*(divid[e|ir]).*",
                "pseudocode": """def dividir(a, b):
    if b == 0:
        return "Error: division por cero"
    else:
        return a / b
"""
            },
            # Patrones para bucles
            "bucle_for": {
                "regex": r"(crear|hacer|definir)\s+(un\s+)?bucle\s+.*(for|para).*",
                "pseudocode": """for i in range(1, 11):
    print(i)
"""
            },
            "bucle_while": {
                "regex": r"(crear|hacer|definir)\s+(un\s+)?bucle\s+.*(while|mientras).*",
                "pseudocode": """i = 1
while i <= 10:
    print(i)
    i = i + 1
"""
            },
            # Patrones para condicionales
            "condicional": {
                "regex": r"(crear|hacer|definir)\s+(un\s+)?condicional.*",
                "pseudocode": """numero = int(input("Ingrese un numero: "))
if numero % 2 == 0:
    print("El numero es par")
else:
    print("El numero es impar")
"""
            },
            # Patrón por defecto
            "default": {
                "pseudocode": """# No se pudo generar codigo para la entrada
print("Comando no reconocido")
"""
            }
        }
    
    def natural_to_pseudocode(self, text: str) -> str:
        """
        Convierte texto en lenguaje natural a código Python.
        
        Args:
            text: Texto en lenguaje natural
            
        Returns:
            Código Python generado
        """
        normalized_text = normalize_text(text)
        logger.info(f"Convirtiendo a código Python: {normalized_text}")
        print(f"Convirtiendo a código Python: {normalized_text}")
        
        # Si el modelo está cargado, usarlo para generar código
        if self.model_loaded:
            try:
                # Crear el prompt para el modelo
                prompt = f"Convierte la siguiente instrucción a código Python. Solo devuelve el código, sin explicaciones adicionales:\n\n{normalized_text}\n\nCódigo Python:"
                
                # Generar código con el modelo
                outputs = self.generator(
                    prompt,
                    max_length=self.max_length,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    num_return_sequences=1
                )
                
                # Extraer el código generado
                generated_text = outputs[0]['generated_text']
                
                # Extraer solo la parte del código (después del prompt)
                if "Código Python:" in generated_text:
                    code = generated_text.split("Código Python:")[1].strip()
                else:
                    code = generated_text.replace(prompt, "").strip()
                
                logger.info("Código generado con el modelo transformer")
                return code
            except Exception as e:
                logger.error(f"Error al generar código con el modelo transformer: {e}")
                print(f"Error al generar código con el modelo transformer: {e}")
                print("Usando sistema basado en patrones como fallback")
        
        # Si el modelo no está cargado o falló, usar el sistema basado en patrones
        # Buscar patrones en el texto
        for pattern_name, pattern_info in self.patterns.items():
            if pattern_name == "default":
                continue
                
            if "regex" in pattern_info and re.search(pattern_info["regex"], normalized_text, re.IGNORECASE):
                logger.info(f"Patrón encontrado: {pattern_name}")
                return pattern_info["pseudocode"]
        
        # Si no se encontró ningún patrón, devolver el código por defecto
        return self.patterns["default"]["pseudocode"]
    
    def natural_to_python(self, text: str) -> str:
        """
        Convierte texto en lenguaje natural directamente a código Python.
        Este método es un alias de natural_to_pseudocode para mantener
        la compatibilidad con el flujo existente.
        
        Args:
            text: Texto en lenguaje natural
            
        Returns:
            Código Python que será procesado por los analizadores
        """
        return self.natural_to_pseudocode(text)