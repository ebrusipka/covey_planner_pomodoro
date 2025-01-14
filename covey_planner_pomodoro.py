import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry # type: ignore
from plyer import notification # type: ignore
from datetime import datetime, timedelta
import threading
import time
import json
import os

class CoveyQuadrant:
    def __init__(self, title, color):
        self.title = title
        self.color = color
        self.tasks = []

    def add_task(self, task, date, note, recurrence="Tekrar Yok"):
        self.tasks.append({
            "title": task,
            "date": date,
            "note": note,
            "recurrence": recurrence,
            "completed": False,
            "progress": 0,
            "var": tk.BooleanVar(value=False)
        })

    def remove_task(self, task):
        self.tasks.remove(task)

class PomodoroTimer:
    def __init__(self, frame, label, time):
        self.frame = frame
        self.timer_label_text = label
        self.initial_time = time
        self.current_time = time
        self.timer_running = False
        self.timer_thread = None
        self.create_pomodoro_widgets()

    def create_pomodoro_widgets(self):
        ttk.Label(self.frame, text=self.timer_label_text, font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        self.timer_label = ttk.Label(self.frame, text="Süre", font=('Helvetica', 12))
        self.timer_label.grid(row=1, column=0, columnspan=2)
        self.time_label = ttk.Label(self.frame, text=f"{self.initial_time // 60}:00", font=('Helvetica', 48))
        self.time_label.grid(row=2, column=0, columnspan=2, pady=20)
        self.start_button = ttk.Button(self.frame, text="Başlat", command=self.start_timer)
        self.start_button.grid(row=3, column=0, padx=5, pady=10)
        self.reset_button = ttk.Button(self.frame, text="Sıfırla", command=self.reset_timer)
        self.reset_button.grid(row=3, column=1, padx=5, pady=10)

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_button.config(text="Durdur")
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.daemon = True
            self.timer_thread.start()
        else:
            self.timer_running = False
            self.start_button.config(text="Başlat")

    def run_timer(self):
        while self.current_time > 0 and self.timer_running:
            minutes, seconds = divmod(self.current_time, 60)
            self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")
            time.sleep(1)
            self.current_time -= 1
        if self.current_time <= 0 and self.timer_running:
            self.timer_completed()

    def timer_completed(self):
        self.timer_running = False
        self.start_button.config(text="Başlat")
        self.current_time = self.initial_time
        self.time_label.config(text=f"{self.initial_time // 60}:00")
        try:
            notification.notify(
                title=f"{self.timer_label_text} Tamamlandı",
                message="Süre doldu!",
                timeout=10
            )
        except:
            pass

    def reset_timer(self):
        self.timer_running = False
        self.current_time = self.initial_time
        self.timer_label.config(text="Süre")
        self.time_label.config(text=f"{self.initial_time // 60}:00")
        self.start_button.config(text="Başlat")

class CoveyMatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Covey Matrix ve Pomodoro")
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 1. KISIM: Görev Detayları
        self.details_frame = ttk.LabelFrame(main_frame, text="Görev Detayları", padding="10")
        self.details_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.N, tk.S))

        tk.Label(self.details_frame, text="Görev Tarihi:").grid(row=0, column=0, padx=10, pady=10)
        self.date_entry = DateEntry(self.details_frame, width=12, background='lightblue', foreground='black', borderwidth=2, 
                                    headersbackground='lightgray', headersforeground='black', weekendbackground='pink', 
                                    weekendforeground='black', othermonthbackground='lightyellow', othermonthforeground='gray', 
                                    othermonthwebackground='lightyellow', othermonthweforeground='gray')
        self.date_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.details_frame, text="Görev Adı:").grid(row=1, column=0, padx=10, pady=10)
        self.task_entry = tk.Entry(self.details_frame, relief='flat', bd=1)
        self.task_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self.details_frame, text="Bu görev önemli mi?").grid(row=2, column=0, padx=10, pady=5)
        self.importance_var = tk.StringVar(value="Önemsiz")
        tk.Radiobutton(self.details_frame, text="Evet", variable=self.importance_var, value="Önemli", relief='flat').grid(row=2, column=1)
        tk.Radiobutton(self.details_frame, text="Hayır", variable=self.importance_var, value="Önemsiz", relief='flat').grid(row=2, column=2)

        tk.Label(self.details_frame, text="Bu görev acil mi?").grid(row=3, column=0, padx=10, pady=5)
        self.urgency_var = tk.StringVar(value="Acil Değil")
        tk.Radiobutton(self.details_frame, text="Evet", variable=self.urgency_var, value="Acil", relief='flat').grid(row=3, column=1)
        tk.Radiobutton(self.details_frame, text="Hayır", variable=self.urgency_var, value="Acil Değil", relief='flat').grid(row=3, column=2)

        tk.Label(self.details_frame, text="Not Ekle:").grid(row=4, column=0, padx=10, pady=10)
        self.note_entry = tk.Entry(self.details_frame, relief='flat', bd=1)
        self.note_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self.details_frame, text="Tekrar Sıklığı:").grid(row=5, column=0, padx=10, pady=10)
        self.recurrence_var = tk.StringVar(value="Tekrar Yok")
        tk.OptionMenu(self.details_frame, self.recurrence_var, "Tekrar Yok", "Günlük", "Haftalık", "Aylık").grid(row=5, column=1, padx=10, pady=10)

        # 2. KISIM: Görev Yönetimi (Covey Matrisi)
        self.task_frame = ttk.LabelFrame(main_frame, text="Görev Yönetimi", padding="10")
        self.task_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.task_frame.grid_columnconfigure(1, weight=1)  # Görev yönetimi alanını genişlet

        # Görevleri filtrelemek için menü
        self.filter_frame = tk.Frame(self.task_frame)
        self.filter_frame.pack(pady=10)
        self.filter_var = tk.StringVar(value="Tüm Görevler")
        self.filter_dropdown = tk.OptionMenu(self.filter_frame, self.filter_var,
                                             "Bugünkü Görevler", "Bu Haftaki Görevler", "Bu Aylık Görevler",
                                             "Tamamlanmamış Görevler", "Tamamlanmış Görevler", "Tüm Görevler",
                                             command=self.filter_tasks)
        self.filter_dropdown.pack(side=tk.LEFT, padx=5)

        # Görev Ekle butonu
        tk.Button(self.filter_frame, text="Görev Ekle", command=self.add_task, relief='flat', bd=0, padx=5, pady=2).pack(side=tk.LEFT, padx=10)

        self.quadrant_frames = {}
        self.quadrants = {
            "Önemli/Acil": CoveyQuadrant("Önemli/Acil", "#FFE4E4"),
            "Önemsiz/Acil": CoveyQuadrant("Önemsiz/Acil", "#FFFDE4"),
            "Önemli/Acil Değil": CoveyQuadrant("Önemli/Acil Değil", "#E4FFE4"),
            "Önemsiz/Acil Değil": CoveyQuadrant("Önemsiz/Acil Değil", "#E4F4FF")
        }
        for idx, (title, quadrant) in enumerate(self.quadrants.items()):
            frame = tk.LabelFrame(self.task_frame, text=title, padx=10, pady=10, bg=quadrant.color, relief="flat", borderwidth=0)
            frame.pack(fill='both', expand=True, padx=5, pady=5)
            self.quadrant_frames[title] = frame

        # 3. KISIM: Pomodoro karesi
        self.pomodoro_frame = ttk.Notebook(main_frame)
        self.pomodoro_frame.grid(row=0, column=2, padx=30, pady=10, sticky=(tk.N, tk.S))

        self.pomodoro_tab = ttk.Frame(self.pomodoro_frame)
        self.short_break_tab = ttk.Frame(self.pomodoro_frame)
        self.long_break_tab = ttk.Frame(self.pomodoro_frame)

        self.pomodoro_frame.add(self.pomodoro_tab, text="Pomodoro")
        self.pomodoro_frame.add(self.short_break_tab, text="Kısa Mola")
        self.pomodoro_frame.add(self.long_break_tab, text="Uzun Mola")

        self.pomodoro_timer = PomodoroTimer(self.pomodoro_tab, "Pomodoro Zamanlayıcı", 25 * 60)
        self.short_break_timer = PomodoroTimer(self.short_break_tab, "Kısa Mola Zamanlayıcı", 5 * 60)
        self.long_break_timer = PomodoroTimer(self.long_break_tab, "Uzun Mola Zamanlayıcı", 15 * 60)

        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get()
        importance = self.importance_var.get()
        urgency = self.urgency_var.get()
        date = self.date_entry.get()
        note = self.note_entry.get()
        recurrence = self.recurrence_var.get()

        if not task:
            messagebox.showwarning("Uyarı", "Lütfen görev adını girin!")
            return

        quadrant_title = f"{importance}/{urgency}"
        if quadrant_title in self.quadrants:
            quadrant = self.quadrants[quadrant_title]
            quadrant.add_task(task, date, note, recurrence)
            self.update_quadrants()
            self.task_entry.delete(0, tk.END)
            self.note_entry.delete(0, tk.END)
            self.save_tasks()

    def update_quadrants(self):
        self.filter_tasks()

    def complete_task(self, task, quadrant_title):
        task["completed"] = task["var"].get()
        self.update_quadrants()
        self.save_tasks()

    def show_note(self, task):
        messagebox.showinfo("Görev Notu", task["note"] if task["note"] else "Not bulunmuyor.")

    def delete_task(self, task, quadrant_title):
        if messagebox.askyesno("Onay", "Bu görevi silmek istediğinizden emin misiniz?"):
            quadrant = self.quadrants[quadrant_title]
            quadrant.remove_task(task)
            self.update_quadrants()
            self.save_tasks()

    def save_tasks(self):
        try:
            data = {}
            for title, quadrant in self.quadrants.items():
                data[title] = []
                for task in quadrant.tasks:
                    task_copy = task.copy()
                    task_copy["completed"] = task["var"].get()
                    del task_copy["var"]
                    data[title].append(task_copy)
            
            with open("tasks.json", "w", encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Görevler kaydedilirken bir hata oluştu: {e}")

    def load_tasks(self):
        try:
            if os.path.exists("tasks.json"):
                with open("tasks.json", "r", encoding='utf-8') as file:
                    data = json.load(file)
                    for title, tasks in data.items():
                        if title in self.quadrants:
                            for task_data in tasks:
                                task_data["var"] = tk.BooleanVar(value=task_data["completed"])
                                self.quadrants[title].tasks.append(task_data)
            self.check_recurring_tasks()
            self.update_quadrants()
        except Exception as e:
            print(f"Görevler yüklenirken bir hata oluştu: {e}")

    def check_recurring_tasks(self):
        current_date = datetime.now().date()
        for quadrant in self.quadrants.values():
            for task in quadrant.tasks:
                task_date = datetime.strptime(task['date'], "%m/%d/%y").date()
                if task_date < current_date:
                    if task['recurrence'] == "Günlük":
                        days_diff = (current_date - task_date).days
                        task['date'] = (task_date + timedelta(days=days_diff)).strftime("%m/%d/%y")
                    elif task['recurrence'] == "Haftalık":
                        weeks_diff = ((current_date - task_date).days + 6) // 7
                        task['date'] = (task_date + timedelta(weeks=weeks_diff)).strftime("%m/%d/%y")
                    elif task['recurrence'] == "Aylık":
                        months_diff = (current_date.year - task_date.year) * 12 + current_date.month - task_date.month
                        if current_date.day < task_date.day:
                            months_diff -= 1
                        new_date = task_date
                        for _ in range(months_diff):
                            if new_date.month == 12:
                                new_date = new_date.replace(year=new_date.year + 1, month=1)
                            else:
                                new_date = new_date.replace(month=new_date.month + 1)
                        task['date'] = new_date.strftime("%m/%d/%y")

    def filter_tasks(self, *args):
        filter_type = self.filter_var.get()
        current_date = datetime.now()

        for title, quadrant in self.quadrants.items():
            frame = self.quadrant_frames[title]
            for widget in frame.winfo_children():
                widget.destroy()

            tk.Label(frame, text=title, bg=quadrant.color).pack(pady=5)

            filtered_tasks = []
            for task in quadrant.tasks:
                task_date = datetime.strptime(task['date'], "%m/%d/%y")

                if filter_type == "Bugünkü Görevler":
                    if task_date.date() == current_date.date():
                        filtered_tasks.append(task)
                elif filter_type == "Bu Haftaki Görevler":
                    week_start = current_date - timedelta(days=current_date.weekday())
                    week_end = week_start + timedelta(days=6)
                    if week_start.date() <= task_date.date() <= week_end.date():
                        filtered_tasks.append(task)
                elif filter_type == "Bu Aylık Görevler":
                    if task_date.month == current_date.month and task_date.year == current_date.year:
                        filtered_tasks.append(task)
                elif filter_type == "Tamamlanmamış Görevler":
                    if not task['completed']:
                        filtered_tasks.append(task)
                elif filter_type == "Tamamlanmış Görevler":
                    if task['completed']:
                        filtered_tasks.append(task)
                else:  # "Tüm Görevler"
                    filtered_tasks.append(task)

            self._display_filtered_tasks(frame, filtered_tasks, quadrant.color, title)

    def _display_filtered_tasks(self, frame, tasks, bg_color, quadrant_title):
        for task in tasks:
            task_frame = tk.Frame(frame, bg=bg_color)
            task_frame.pack(fill='x')

            task_checkbox = tk.Checkbutton(
                task_frame, 
                text=f"{task['title']} - {task['date']}", 
                bg=bg_color,
                variable=task["var"],
                command=lambda t=task, q=quadrant_title: self.complete_task(t, q)
            )
            task_checkbox.pack(side='left', padx=5)

            progress_label = tk.Label(task_frame, text=self.get_progress_bar(task["progress"]), bg=bg_color)
            progress_label.pack(side='left', padx=5)

            tk.Button(task_frame, text="+25%", command=lambda t=task, q=quadrant_title: self.update_progress(t, 25, q)).pack(side='left', padx=2)
            tk.Button(task_frame, text="Sıfırla", command=lambda t=task, q=quadrant_title: self.reset_progress(t, q)).pack(side='left', padx=2)

            if task["completed"]:
                task_checkbox.config(font=("Arial", 10, "overstrike"))
            else:
                task_checkbox.config(font=("Arial", 10))

            tk.Button(task_frame, text="Notu Göster", command=lambda t=task: self.show_note(t)).pack(side='left', padx=5)
            tk.Button(task_frame, text="Sil", command=lambda t=task, q=quadrant_title: self.delete_task(t, q)).pack(side='right', padx=5)

    def update_progress(self, task, amount, quadrant_title):
        new_progress = min(task["progress"] + amount, 100)
        if new_progress != task["progress"]:
            task["progress"] = new_progress
            self.update_quadrants()
            self.save_tasks()

    def reset_progress(self, task, quadrant_title):
        task["progress"] = 0
        self.update_quadrants()
        self.save_tasks()

    def get_progress_bar(self, progress):
        total_blocks = 4
        filled_blocks = int(progress / 25)
        empty_blocks = total_blocks - filled_blocks
        return "🟦" * filled_blocks + "⬜️" * empty_blocks

if __name__ == "__main__":
    root = tk.Tk()
    app = CoveyMatrixApp(root)
    root.mainloop()