import tkinter as tk
from tkinter import scrolledtext
import threading
import speech_recognition as sr
import openai
import pyttsx3
import os
import webbrowser
import datetime
from PIL import Image, ImageTk
from config import apikey

# === Initialize OpenAI Key ===
openai.api_key = apikey

# === Initialize TTS engine ===
engine = pyttsx3.init()

def say(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

# === Chat History ===
chatStr = ""

# === Chat with OpenAI ===
def chat(query):
    global chatStr
    chatStr += f"User: {query}\nZexa: "
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Zexa, a helpful, sarcastic, badass assistant."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=256,
        )
        text_response = response["choices"][0]["message"]["content"].strip()
        say(text_response)
        chatStr += f"{text_response}\n"
        return text_response
    except Exception as e:
        err_msg = f"OpenAI API error: {e}"
        say(err_msg)
        return err_msg

# === AI File Generator ===
def ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Generate a response for a report."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=512,
    )
    text = f"Zexa AI Output for Prompt: {prompt} \n\n{text_response := response['choices'][0]['message']['content'].strip()}"

    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{'_'.join(prompt.lower().split()[:5])}.txt", "w") as f:
        f.write(text)

# === Voice recognition ===
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        append_to_chatbox("🎤 Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            say("Timeout. Try again.")
            append_to_chatbox("⏰ Timeout: You were too slow, bro.")
            return ""

    append_to_chatbox("🔍 Recognizing...")
    try:
        query = r.recognize_google(audio, language="en-IN")
        append_to_chatbox(f"🧠 You said: {query}")
        return query
    except sr.UnknownValueError:
        say("Sorry, I didn't catch that.")
        append_to_chatbox("🤷 Couldn't understand the audio.")
    except Exception as e:
        say("Mic error. Please try again.")
        append_to_chatbox(f"💥 Error recognizing speech: {e}")
    return ""

# === Command Handler ===
def handle_command(query):
    if not query.strip():
        return
    append_to_chatbox(f"🧑‍💻 You: {query}")
    query = query.lower()

    sites = {
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.com",
        "google": "https://www.google.com"
    }
    for site in sites:
        if f"open {site}" in query:
            say(f"Opening {site}")
            webbrowser.open(sites[site])
            append_to_chatbox(f"🌐 Opened {site}")
            return

    if "play music" in query:
        say("Playing your jam.")
        music_path = r"C:\\Users\\Adarsh\\Downloads\\Veera Raja Veera - Full Video PS2 Tamil @ARRahman Mani Ratnam Jayam Ravi, Sobhita Dhulipala.mp3"
        os.startfile(music_path)
        return

    if "the time" in query:
        time = datetime.datetime.now().strftime("%H:%M")
        say(f"Bro, it's {time} now.")
        append_to_chatbox(f"⏰ Time: {time}")
        return

    if "using artificial intelligence" in query:
        ai(prompt=query)
        append_to_chatbox("📄 AI file created.")
        return

    if "zexa quit" in query or "exit" in query:
        say("Peace out! Zexa signing off.")
        window.quit()
        return

    # Default: Chat with AI
    append_to_chatbox("🤖 Zexa is thinking...")
    response = chat(query)
    append_to_chatbox(f"🤖 Zexa: {response}")

# === GUI Setup ===
window = tk.Tk()
window.title("Zexa - AI Assistant")
window.geometry("520x640")
window.configure(bg="#0a0a0a")

# === Logo ===
logo_img = Image.open(r"C:\Users\Adarsh\OneDrive\Desktop\zexa_ai\zexa_logo.png")
logo_img = logo_img.resize((150, 150), Image.Resampling.LANCZOS)

logo_photo = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(window, image=logo_photo, bg="#0a0a0a")
logo_label.pack(pady=10)

# === Chatbox ===
chatbox = scrolledtext.ScrolledText(window, wrap=tk.WORD, font=("Consolas", 12), bg="#1a1a1a", fg="white", insertbackground="white")
chatbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chatbox.config(state='disabled')

# === Input field ===
entry = tk.Entry(window, font=("Consolas", 14), bg="#0f0f0f", fg="white", insertbackground="white")
entry.pack(pady=10, padx=10, fill=tk.X)

# === Append text ===
def append_to_chatbox(text):
    chatbox.config(state='normal')
    chatbox.insert(tk.END, text + "\n")
    chatbox.config(state='disabled')
    chatbox.see(tk.END)

# === Submit callbacks ===
def on_submit():
    query = entry.get()
    entry.delete(0, tk.END)
    threading.Thread(target=handle_command, args=(query,), daemon=True).start()

def on_voice():
    threading.Thread(target=lambda: handle_command(takeCommand()), daemon=True).start()

# === Buttons ===
btn_frame = tk.Frame(window, bg="#0a0a0a")
btn_frame.pack(pady=10)

submit_btn = tk.Button(btn_frame, text="Send Text", command=on_submit, bg="#007acc", fg="white", font=("Arial", 12), relief="flat")
submit_btn.pack(side=tk.LEFT, padx=10)

voice_btn = tk.Button(btn_frame, text="🎤 Speak", command=on_voice, bg="#00bfff", fg="black", font=("Arial", 12), relief="flat")
voice_btn.pack(side=tk.LEFT, padx=10)

append_to_chatbox("👋 Welcome to Zexa - Your AI Assistant!")
say("Hey, I'm Zexa. How can I help you today?")

window.mainloop()
