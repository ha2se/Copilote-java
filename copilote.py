import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import subprocess
import os

def send_message(event=None):
    user_input = entry.get()
    if user_input:
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, "You: " + user_input + "\n", "user")
        
        llm_response = get_gemini_response(user_input)
        
        chat_window.insert(tk.END, "Copilot: " + llm_response + "\n", "bot")
        chat_window.config(state=tk.DISABLED)
        
        entry.delete(0, tk.END)
        entry.insert(0, "Enter prompt")  # Restore placeholder text

def get_gemini_response(user_input):
    command = f'ollama run model "{user_input}"'
    
    try:
        with open(os.devnull, 'w') as devnull:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=devnull,
                text=True
            )
            stdout, _ = process.communicate()
        
        if process.returncode == 0:
            # Split the output into lines and skip the first two lines
            lines = stdout.strip().split('\n')
            return '\n'.join(lines[2:])  # Skip the first two lines
        else:
            return "An error occurred, but it was hidden."
    except Exception as e:
        return f"Error: {str(e)}"

def on_entry_focus(event):
    if entry.get() == "Enter prompt":
        entry.delete(0, tk.END)
        entry.config(fg='white', font=("Arial", 14))  # Larger font

def on_entry_focusout(event):
    if entry.get() == "":
        entry.insert(0, "Enter prompt")
        entry.config(fg='gray', font=("Arial", 14, "italic"))  # Placeholder styling

def create_rounded_button(frame, text, command):
    canvas = tk.Canvas(frame, width=50, height=50, bg='#444444', highlightthickness=0, bd=0)
    canvas.create_oval(10, 10, 40, 40, fill='#555555')
    canvas.create_text(25, 25, text=text, fill='white', font=("Arial", 16, "bold"))
    canvas.pack(side=tk.RIGHT, padx=10)
    
    # Bind the button click event to the command function
    canvas.bind("<Button-1>", command)
    
    return canvas

def new_chat():
    # Save the current chat history to the history section
    history_text = chat_window.get(1.0, tk.END).strip()
    if history_text:
        chat_history_list.insert(tk.END, f"Chat {len(chat_history_list.get(0, tk.END)) + 1}:\n{history_text}\n")
    
    # Clear the current chat window
    chat_window.config(state=tk.NORMAL)
    chat_window.delete(1.0, tk.END)
    chat_window.config(state=tk.DISABLED)
    
    # Clear the entry widget
    entry.delete(0, tk.END)
    entry.insert(0, "Enter prompt")

# Initialize the main window
root = tk.Tk()
root.title("Copilot Chat Interface")
root.geometry("800x600")
root.configure(bg='#1e1e1e')

# Header
header_frame = tk.Frame(root, bg='#333333', height=60)
header_frame.pack(side=tk.TOP, fill=tk.X)

# Load and display the logo
logo_image = Image.open(r"C:\Users\readf\OneDrive\Desktop\finetuningmodel\pythia-70m-deduped\step3000\models--EleutherAI--pythia-70m-deduped\vermeg_logo.jpg")  # Replace with your logo path
logo_image = logo_image.resize((40, 40), Image.LANCZOS)  # Use LANCZOS for high-quality downsampling
logo_photo = ImageTk.PhotoImage(logo_image)

logo = tk.Label(header_frame, image=logo_photo, bg='#333333')
logo.image = logo_photo  # Keep a reference to avoid garbage collection
logo.pack(side=tk.LEFT, padx=10, pady=5)

header_title = tk.Label(header_frame, text="Your Chat", font=("Arial", 18, "bold"), bg='#333333', fg='white')
header_title.pack(side=tk.LEFT, padx=10, pady=5)

# Sidebar for new chats and chat history
sidebar_frame = tk.Frame(root, bg='#333333', width=200)
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

new_chat_button = tk.Button(sidebar_frame, text="New Chat", fg="white", bg="#444444", font=("Arial", 12), relief=tk.FLAT, command=new_chat)
new_chat_button.pack(pady=20, padx=10, fill=tk.X)

# Chat history listbox
chat_history_list = tk.Listbox(sidebar_frame, bg='#444444', fg='white', font=("Arial", 12), selectmode=tk.SINGLE)
chat_history_list.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Main chat window
chat_frame = tk.Frame(root, bg='#1e1e1e')
chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

chat_window = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state=tk.DISABLED, bg='#1e1e1e', fg='white', font=("Arial", 12), relief=tk.FLAT)
chat_window.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Set tag configurations for user and bot messages
chat_window.tag_configure("user", foreground="#00ffff", font=("Arial", 12, "bold"))
chat_window.tag_configure("bot", foreground="#ffcc00", font=("Arial", 12, "bold"))

# Entry widget for input
entry_frame = tk.Frame(root, bg='#1e1e1e')
entry_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

entry = tk.Entry(entry_frame, fg='gray', bg='#333333', insertbackground='white', relief=tk.FLAT, font=("Arial", 14))
entry.insert(0, "Enter prompt")
entry.bind("<FocusIn>", on_entry_focus)
entry.bind("<FocusOut>", on_entry_focusout)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)

# Rounded Send button using Canvas
send_button = create_rounded_button(entry_frame, "➤", send_message)

root.mainloop()
