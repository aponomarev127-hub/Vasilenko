import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

FILE_NAME = "password_history.json"

class PasswordGeneratorApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Random Password Generator")
        self.window.geometry("900x600")

        self.history = []

        self.build_ui()
        self.load_history()

    def build_ui(self):
        top = tk.Frame(self.window)
        top.pack(pady=15)

        # Length slider
        tk.Label(top, text="Длина пароля").grid(row=0, column=0, padx=5)
        self.length_slider = tk.Scale(top, from_=4, to=32, orient="horizontal")
        self.length_slider.set(12)
        self.length_slider.grid(row=0, column=1, padx=5)

        # Checkboxes
        self.use_letters = tk.IntVar(value=1)
        self.use_digits = tk.IntVar(value=1)
        self.use_symbols = tk.IntVar(value=0)

        tk.Checkbutton(top, text="Буквы", variable=self.use_letters).grid(row=0, column=2)
        tk.Checkbutton(top, text="Цифры", variable=self.use_digits).grid(row=0, column=3)
        tk.Checkbutton(top, text="Символы", variable=self.use_symbols).grid(row=0, column=4)

        tk.Button(top, text="Сгенерировать", command=self.generate_password).grid(row=0, column=5, padx=10)

        self.result_label = tk.Label(self.window, text="Пароль появится здесь", font=("Arial", 14))
        self.result_label.pack(pady=10)

        # History table
        self.tree = ttk.Treeview(self.window, columns=("date", "password"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("password", text="Пароль")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(self.window, text="Сохранить историю", command=self.save_history).pack(pady=5)

    def generate_password(self):
        length = self.length_slider.get()

        if length < 4 or length > 32:
            messagebox.showerror("Ошибка", "Недопустимая длина пароля")
            return

        chars = ""

        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_digits.get():
            chars += string.digits
        if self.use_symbols.get():
            chars += "!@#$%^&*()_+-=<>?/"

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
            return

        password = "".join(random.choice(chars) for _ in range(length))

        self.result_label.config(text=password)

        row = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "password": password
        }

        self.history.append(row)
        self.update_table()
        self.save_history()

    def update_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for row in self.history:
            self.tree.insert("", "end", values=(row["date"], row["password"]))

    def save_history(self):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                self.history = json.load(f)
        self.update_table()


window = tk.Tk()
app = PasswordGeneratorApp(window)
window.mainloop()
