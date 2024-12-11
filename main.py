import os
import customtkinter as ctk
from gtts import gTTS
import pygame
from PIL import Image, ImageTk
import tkinter as tk

def generate_response(prompt, model):
    response = os.popen(f"ollama run {model} '{prompt}'").read()
    return response.strip()

def text_to_speech(text, lang='en', tld='co.uk'):
    if text:
        tts = gTTS(text, lang=lang, slow=False, tld=tld)
        tts.save("response.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("response.mp3")
        pygame.mixer.music.play()
    else:
        print("No text to speak.")

def on_submit():
    prompt = prompt_entry.get("1.0", 'end-1c')
    model = model_combobox.get()  # Get the selected model from the ComboBox
    response = generate_response(prompt, model)
    chat_history.configure(state=ctk.NORMAL)
    chat_history.insert(ctk.END, "🤵: " + prompt + "\n")
    chat_history.insert(ctk.END, "🤖 (" + model + "): " + response + "\n\n")
    chat_history.configure(state=ctk.DISABLED)
    chat_history.yview(ctk.END)
    prompt_entry.delete("1.0", ctk.END)
    global latest_response
    latest_response = response

def on_vocal():
    try:
        text_to_speech(latest_response)
    except NameError:
        print("No response to vocalize")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("❖ Ollama Chat Hub ❖")
    app.geometry("650x660")
    app.resizable(False, False)

    # Create main frame to hold left and right sections
    main_frame = tk.Frame(app)
    main_frame.pack(fill='both', expand=True)

    # Create left frame for the image and information
    left_frame = tk.Frame(main_frame, bg='black')
    left_frame.grid(row=0, column=0, sticky="nsew")

    # Create right frame for chat interface
    right_frame = tk.Frame(main_frame)
    right_frame.grid(row=0, column=1, sticky="nsew")

    # Ensure equal size for left and right frames
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)

    # Load and display image in the left frame
    image = Image.open("main.png")#.resize((400, 400), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(left_frame, image=photo)
    image_label.image = photo  # Keep a reference to avoid garbage collection
    image_label.pack(side=tk.TOP, padx=20, pady=20)


    # Create a frame for model selection label and combobox
    model_frame = tk.Frame(right_frame)
    model_frame.pack(pady=(10, 0))

    model_textbox = ctk.CTkTextbox(model_frame, width=120, height=30, corner_radius=8, fg_color="white", font=("Trebuchet MS", 14))
    model_textbox.insert("1.0", "✦ Select Model:")
    model_textbox.configure(state=ctk.DISABLED, text_color="black", fg_color="white")
    model_textbox.pack(side=tk.LEFT, padx=5)

    model_combobox = ctk.CTkComboBox(model_frame, values=["Llama3.2", "phi3", "mistral", "qwen2.5", "starcoder2"], font=("Trebuchet MS", 12))
    model_combobox.set("phi3")  # Set default value
    model_combobox.pack(side=tk.LEFT, padx=5)

    # Add widgets to the right frame
    chat_history_label = ctk.CTkLabel(right_frame, text="Ollama Live Chat 📜", font=("Trebuchet MS", 16), text_color="white", corner_radius=8, fg_color="#158542")
    chat_history_label.pack(pady=(5, 0))

    chat_history = ctk.CTkTextbox(right_frame, wrap=ctk.WORD, width=360, height=250, corner_radius=8)
    chat_history.pack(padx=5, pady=5)
    chat_history.configure(state=ctk.DISABLED)

    prompt_entry_label = ctk.CTkLabel(right_frame, text="Your Prompts 💭", font=("Trebuchet MS", 16), text_color="white", corner_radius=8, fg_color="#158542")
    prompt_entry_label.pack(pady=(5, 0))

    prompt_entry = ctk.CTkTextbox(right_frame, wrap=ctk.WORD, width=360, height=100, corner_radius=8)
    prompt_entry.pack(padx=5, pady=5)

    # Create a frame for the buttons to align them in the same row
    button_frame = tk.Frame(right_frame)
    button_frame.pack(pady=5)

    submit_button = ctk.CTkButton(button_frame, text="Send Prompt ➤", font=("Trebuchet MS", 12), command=on_submit, corner_radius=8, fg_color="#424bf5", hover_color="#8a8fed")
    submit_button.pack(side=tk.LEFT, padx=5)

    vocal_button = ctk.CTkButton(button_frame, text="Listen 🔊", font=("Trebuchet MS", 12),  command=on_vocal, corner_radius=8, fg_color="#424bf5", hover_color="#8a8fed")
    vocal_button.pack(side=tk.LEFT, padx=5)

    # Add copyright label with text wrapping
    copyright_label = ctk.CTkLabel(
        right_frame, 
        text="🔗 To install Ollama visit:\nhttps://ollama.com/download\n🔽 To clone Models run:\nollama pull llama3.2\n\n⚙ Install dependencies:\npip3 install -r requirements.txt\n\n© 2023 Amir Faramarzpour.", 
        text_color="black", 
        font=("Trebuchet MS", 12),
        corner_radius=4, 

        wraplength=380  # Set wrap length to fit within the right frame

    )
    copyright_label.pack(pady=(10, 0))

    app.mainloop()
