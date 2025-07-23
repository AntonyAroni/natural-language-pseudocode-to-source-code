"""
Módulo para el reconocimiento de voz.
"""

import logging
from typing import Optional, Dict, Any
import os
import speech_recognition as sr_lib

from config import SPEECH_RECOGNITION

logger = logging.getLogger(__name__)

class SpeechRecognizer:
    """Clase para manejar el reconocimiento de voz."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicializa el reconocedor de voz.
        
        Args:
            config: Configuración para el reconocedor de voz
        """
        self.config = config or SPEECH_RECOGNITION
        self.language = self.config.get("language", "es-ES")
        self.sample_rate = self.config.get("sample_rate", 16000)
        self.timeout = self.config.get("timeout", 5)
        
        # Inicializar el reconocedor
        self.recognizer = sr_lib.Recognizer()
        logger.info("Inicializando reconocedor de voz")
    
    def recognize_from_microphone(self) -> Optional[str]:
        """
        Reconoce voz desde el micrófono.
        
        Returns:
            Texto reconocido o None si hubo un error
        """
        logger.info("Escuchando desde el micrófono...")
        
        try:
            with sr_lib.Microphone(sample_rate=self.sample_rate) as source:
                print("Ajustando para ruido ambiental... Espere un momento")
                self.recognizer.adjust_for_ambient_noise(source)
                print("Habla ahora...")
                audio = self.recognizer.listen(source, timeout=self.timeout)
                
            print("Procesando audio...")
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info(f"Texto reconocido: {text}")
            return text
        except sr_lib.WaitTimeoutError:
            logger.error("Tiempo de espera agotado")
            print("Tiempo de espera agotado. Por favor, intente de nuevo.")
        except sr_lib.UnknownValueError:
            logger.error("No se pudo reconocer el audio")
            print("No se pudo reconocer lo que dijiste. Por favor, intenta de nuevo.")
        except sr_lib.RequestError as e:
            logger.error(f"Error en la solicitud al servicio de reconocimiento: {e}")
            print(f"Error en el servicio de reconocimiento: {e}")
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            print(f"Error inesperado: {e}")
        
        return None
    
    def recognize_from_file(self, audio_file: str) -> Optional[str]:
        """
        Reconoce voz desde un archivo de audio.
        
        Args:
            audio_file: Ruta al archivo de audio
            
        Returns:
            Texto reconocido o None si hubo un error
        """
        if not os.path.exists(audio_file):
            logger.error(f"El archivo {audio_file} no existe")
            print(f"El archivo {audio_file} no existe")
            return None
        
        logger.info(f"Reconociendo voz desde {audio_file}...")
        print(f"Reconociendo voz desde {audio_file}...")
        
        try:
            with sr_lib.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info(f"Texto reconocido: {text}")
            return text
        except sr_lib.UnknownValueError:
            logger.error("No se pudo reconocer el audio")
            print("No se pudo reconocer el audio. Verifica que el archivo sea válido.")
        except sr_lib.RequestError as e:
            logger.error(f"Error en la solicitud al servicio de reconocimiento: {e}")
            print(f"Error en el servicio de reconocimiento: {e}")
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            print(f"Error inesperado: {e}")
        
        return None