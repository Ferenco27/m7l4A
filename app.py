# sistema interactivo de evaluación oral con procesamiento de audio en tiempo real
# Librería para grabar audio desde el micrófono
import sounddevice as sd

# Librería para guardar archivos de audio en formato WAV
import scipy.io.wavfile as wav

# Librería para reconocimiento de voz
import speech_recognition as sr

# Librería para traducción automática
from googletrans import Translator

import random
import time


# Frecuencia de muestreo del audio (44.1 kHz = calidad estándar)
sample_rate = 44100

# Duración de la grabación en segundos
duration = 4

# Número máximo de errores permitidos antes de terminar el juego
max_errors = 3

# Contador de respuestas correctas
score = 0

# Contador de errores cometidos
errors = 0


words_by_level = {
    "easy": ["martillo", "lugar", "mano", "dedo", "pollo", "cocina", "árbol"],
    "medium": ["Vecindad", "Telefono", "Palmera", "Mediano"],
    "hard": ["Cacatúa", "alfombra", "Tela", "Estuche", "Fibra de carbono", "Difícil"]
}

print("Welcome to Type Answer")
level = input("Choose a difficulty level (easy, medium, hard): ").lower()
while level not in words_by_level:
    print("Invalid level. Please choose 'easy', 'medium', or 'hard'.")
    level = input("Choose a difficulty level (easy, medium, hard): ").lower()

word_list = words_by_level[level]
random.shuffle(word_list)
print(f"veras una palabra en español, tradúcela al inglés y dilo en voz alta. Tienes {max_errors} intentos para acertar.")
time.sleep(3)
#inicializa el traductor
recongnizer = sr.Recognizer()
translator = Translator()

#bucle principal del juego
for word in word_list:
    print(f"🔹 Palabra en español: {word}")
    time.sleep(2)
    print("🎤 Grabando tu respuesta...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Espera a que termine la grabación
    wav.write("user_input.wav", sample_rate, recording)  # Guarda la grabación en un archivo WAV

    try:
        with sr.AudioFile("user_input.wav") as source:
            
            audio = recongnizer.record(source)

            recognised = recongnizer.recognize_google(audio, language="en-US").lower()
            print(f"Has dicho: {recognised}")

            translation = translator.translate(word, src="es", dest="en").text.lower()
            print("🔹 Traducción:", translation)

            if recognised == translation:
                score += 1
                print("✅ Correcto!")
            else:
                errors += 1
                print("❌ Incorrecto.")

            if errors > max_errors:
                print("Juego terminado. Has cometido demasiados errores.")
                break

    except Exception:
        errors += 1
        print("❌ No reconocimos el audio.")
        if errors > max_errors:
            print("Juego terminado. Has cometido demasiados errores.")
            break











