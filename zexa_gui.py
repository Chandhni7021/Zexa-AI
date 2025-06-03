import tkinter as tk
import threading
from main import takeCommand, chat, say  # your existing logic

# === Start listening thread ===
def start_listening():
    query = takeCommand()
    if query:
        handle_command(query.lower())

# === Handle commands and update chat log ===
def handle_command(query):
    text_log.config(state=tk.NORMAL)
    text_log.insert(tk.END, f"🧠 You said: {query}\n\n")
    text_log.config(state=tk.DISABLED)
    text_log.see(tk.END)

    response = chat(query)

    text_log.config(state=tk.NORMAL)
    text_log.insert(tk.END, f"🤖 Zexa: {response}\n\n")
    text_log.config(state=tk.DISABLED)
    text_log.see(tk.END)

# === Submit text command ===
def on_submit():
    query = entry.get().strip()
    entry.delete(0, tk.END)
    if query:
        handle_command(query)

# === Styling colors ===
BG_COLOR = "#121212"
TEXT_BG_COLOR = "#1e1e1e"
TEXT_FG_COLOR = "#e0e0e0"
BUTTON_BG = "#3a3a3a"
BUTTON_FG = "#f0f0f0"
ENTRY_BG = "#2b2b2b"
ENTRY_FG = "#ffffff"
FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 20, "bold")

app = tk.Tk()
app.title("Zexa AI Assistant")
app.geometry("520x600")
app.configure(bg=BG_COLOR)

# Title Label
title_label = tk.Label(app, text="🤖 Zexa AI Assistant", font=TITLE_FONT, fg="#00bcd4", bg=BG_COLOR)
title_label.pack(pady=(15, 5))

# Entry Frame for better padding
entry_frame = tk.Frame(app, bg=BG_COLOR)
entry_frame.pack(padx=20, pady=(0, 10), fill=tk.X)

entry = tk.Entry(entry_frame, font=FONT, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground='white')
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0,10))
entry.focus()

# Buttons Frame
btn_frame = tk.Frame(entry_frame, bg=BG_COLOR)
btn_frame.pack(side=tk.RIGHT)

speak_btn = tk.Button(btn_frame, text="🎤 Speak", font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, activebackground="#007c91", activeforeground="white",
                      relief=tk.FLAT, padx=10, command=lambda: threading.Thread(target=start_listening, daemon=True).start())
speak_btn.pack(side=tk.TOP, pady=(0,5), fill=tk.X)

submit_btn = tk.Button(btn_frame, text="⌨️ Submit", font=FONT, bg=BUTTON_BG, fg=BUTTON_FG, activebackground="#007c91", activeforeground="white",
                       relief=tk.FLAT, padx=10, command=on_submit)
submit_btn.pack(side=tk.TOP, fill=tk.X)

# Chat Log Text widget with Scrollbar
text_frame = tk.Frame(app, bg=BG_COLOR)
text_frame.pack(padx=20, pady=(0,20), fill=tk.BOTH, expand=True)

text_log = tk.Text(text_frame, bg=TEXT_BG_COLOR, fg=TEXT_FG_COLOR, font=("Courier New", 11), wrap=tk.WORD, state=tk.DISABLED, relief=tk.FLAT, bd=0)
text_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)

scrollbar = tk.Scrollbar(text_frame, command=text_log.yview, bg=BG_COLOR, troughcolor=TEXT_BG_COLOR, relief=tk.FLAT)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_log.config(yscrollcommand=scrollbar.set)

# Customize scrollbar colors (for Windows, might vary per platform)
try:
    app.tk.call("ttk::style", "theme", "use", "clam")
    style = tk.ttk.Style()
    style.configure("Vertical.TScrollbar", background=BUTTON_BG, troughcolor=TEXT_BG_COLOR, bordercolor=BG_COLOR, arrowcolor="white")
except Exception:
    pass  # fallback if ttk isn't imported or supported

# Add some padding and a welcoming message
text_log.config(state=tk.NORMAL)
text_log.insert(tk.END, "👋 Welcome to Zexa - Your AI Assistant!\n\n")
text_log.config(state=tk.DISABLED)

app.mainloop()
