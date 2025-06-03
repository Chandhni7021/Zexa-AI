import speech_recognition as sr

def listen_and_recognize():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {text}")
            return text
    except sr.RequestError:
        print("💥 Could not request results from Google Speech Recognition service")
    except sr.UnknownValueError:
        print("💥 Could not understand audio")
    except Exception as e:
        print(f"💥 Error recognizing speech: {e}")
    return ""

if __name__ == "__main__":
    print("💻 Welcome to Zexa A.I")
    while True:
        listen_and_recognize()
