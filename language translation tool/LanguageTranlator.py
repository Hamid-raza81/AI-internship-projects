import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator

# Supported languages
language_names = GoogleTranslator().get_supported_languages(as_dict=True)
lang_name_to_code = {v: k for k, v in language_names.items()}
language_list = sorted(list(lang_name_to_code.keys()))

def translate_text():
    src_name = source_lang.get()
    dest_name = target_lang.get()
    src = lang_name_to_code.get(src_name, "en")
    dest = lang_name_to_code.get(dest_name, "hi")
    text = text_input.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Input Required", "Please enter text to translate.")
        return

    try:
        translated = GoogleTranslator(source=src, target=dest).translate(text)
        text_output.config(state="normal")
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, translated)
        text_output.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

# Main Window
root = tk.Tk()
root.title("🌍 Language Translator")
root.geometry("800x600")
root.config(bg="#17a5d0")

# Style
style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground="white", background="white", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12, "bold"), padding=6)
style.configure("TLabel", font=("Arial", 12), background="#f5f7fa")

# Title
title_frame = tk.Frame(root, bg="#f5f7fa")
title_frame.pack(pady=18)
tk.Label(title_frame, text="🌍 Language Translator", font=("Helvetica", 26, "bold"), fg="#1a73e8", bg="#f5f7fa").pack()

# Input Text
input_frame = tk.LabelFrame(root, text="Enter Text to Translate", font=("Arial", 13, "bold"), bg="#f5f7fa", fg="#1a73e8", bd=2, relief="groove")
input_frame.pack(fill="x", padx=30, pady=10)
text_input = tk.Text(input_frame, height=7, width=90, font=("Arial", 12), bd=1, relief="solid", wrap="word")
text_input.pack(padx=10, pady=8)

# Language Selection
lang_frame = tk.Frame(root, bg="#FFFFFF")
lang_frame.pack(pady=10)

tk.Label(lang_frame, text="From:", font=("Arial", 12, "bold"), bg="#060707").grid(row=0, column=0, padx=10, pady=5, sticky="e")
source_lang = ttk.Combobox(lang_frame, values=language_list, width=25, state="readonly")
source_lang.set("english")
source_lang.grid(row=0, column=1, padx=10)

swap_btn = tk.Button(lang_frame, text="⇄", font=("Arial", 14, "bold"), bg="#f7f8fa", fg="#1a73e8", bd=0, width=3, command=lambda: swap_languages())
swap_btn.grid(row=0, column=2, padx=10)

tk.Label(lang_frame, text="To:", font=("Arial", 12, "bold"), bg="#070708").grid(row=0, column=3, padx=10, pady=5, sticky="e")
target_lang = ttk.Combobox(lang_frame, values=language_list, width=25, state="readonly")
target_lang.set("hindi")
target_lang.grid(row=0, column=4, padx=10)

def swap_languages():
    src = source_lang.get()
    tgt = target_lang.get()
    source_lang.set(tgt)
    target_lang.set(src)

# Translate Button
btn_frame = tk.Frame(root, bg="#f5f7fa")
btn_frame.pack(pady=18)
translate_btn = ttk.Button(btn_frame, text="Translate", command=translate_text)
translate_btn.pack(ipadx=20)

# Output Text
output_frame = tk.LabelFrame(root, text="Translated Text", font=("Arial", 13, "bold"), bg="#F5F8FB", fg="#1a73e8", bd=2, relief="groove")
output_frame.pack(fill="x", padx=30, pady=10)
text_output = tk.Text(output_frame, height=7, width=90, font=("Arial", 12), bd=1, relief="solid", wrap="word", state="disabled")
text_output.pack(padx=10, pady=8)



root.mainloop()