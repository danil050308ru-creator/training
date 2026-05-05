import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.file_name = "trainings.json"
        self.data = self.load_data()

        # --- Поля ввода ---
        frame_input = tk.LabelFrame(root, text="Добавить тренировку", padx=10, pady=10)
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.insert(0, datetime.now().strftime("%d.%m.%Y"))
        self.entry_date.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="Тип:").grid(row=0, column=2)
        self.entry_type = tk.Entry(frame_input)
        self.entry_type.grid(row=0, column=3, padx=5)

        tk.Label(frame_input, text="Мин:").grid(row=0, column=4)
        self.entry_duration = tk.Entry(frame_input, width=10)
        self.entry_duration.grid(row=0, column=5, padx=5)

        btn_add = tk.Button(frame_input, text="Добавить", command=self.add_training, bg="lightgreen")
        btn_add.grid(row=0, column=6, padx=10)

        # --- Фильтрация ---
        frame_filter = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=10)
        frame_filter.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filter, text="По типу:").grid(row=0, column=0)
        self.filter_type = tk.Entry(frame_filter)
        self.filter_type.grid(row=0, column=1, padx=5)
        self.filter_type.bind("<KeyRelease>", lambda e: self.update_table())

        tk.Label(frame_filter, text="По дате:").grid(row=0, column=2)
        self.filter_date = tk.Entry(frame_filter)
        self.filter_date.grid(row=0, column=3, padx=5)
        self.filter_date.bind("<KeyRelease>", lambda e: self.update_table())

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("Дата", "Тип", "Длительность"), show="headings")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип тренировки")
        self.tree.heading("Длительность", text="Длительность (мин)")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_table()

    def add_training(self):
        date_str = self.entry_date.get()
        train_type = self.entry_type.get().strip()
        duration_str = self.entry_duration.get()

        # Валидация
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
        except ValueError:
            return messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ДД.ММ.ГГГГ")

        if not train_type:
            return messagebox.showerror("Ошибка", "Введите тип тренировки")

        if not duration_str.isdigit() or int(duration_str) <= 0:
            return messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")

        # Сохранение данных
        new_entry = {"date": date_str, "type": train_type, "duration": duration_str}
        self.data.append(new_entry)
        self.save_data()
        self.update_table()
        
        # Очистка полей
        self.entry_type.delete(0, tk.END)
        self.entry_duration.delete(0, tk.END)

    def load_data(self):
        try:
            with open(self.file_name, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def update_table(self):
        # Очистка
        for item in self.tree.get_children():
            self.tree.delete(item)

        f_type = self.filter_type.get().lower()
        f_date = self.filter_date.get()

        # Отображение с фильтром
        for entry in self.data:
            if f_type in entry["type"].lower() and f_date in entry["date"]:
                self.tree.insert("", tk.END, values=(entry["date"], entry["type"], entry["duration"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
