import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime, timedelta
from tkcalendar import Calendar
import os

# 데이터 파일 경로
DATA_FILE = 'data.json'

# 루틴 데이터 로드 함수
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"routines": [], "repeating_routines": []}

# 루틴 데이터 저장 함수
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 스타일 정의
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 10), padding=6)
style.configure("TLabel", font=("Helvetica", 12), background="lightblue")
style.configure("TEntry", font=("Helvetica", 10), padding=6)
style.configure("TCombobox", font=("Helvetica", 10), padding=6)

# 루틴 추가 창 클래스
class AddRoutineWindow(tk.Toplevel):
    def __init__(self, master, selected_date, refresh):
        super().__init__(master)
        self.title("루틴 추가")
        self.geometry("300x250")
        self.selected_date = selected_date
        self.refresh = refresh

        self.configure(bg="lightblue")

        # 시간 입력
        ttk.Label(self, text="시간 (HH:MM)").grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.time_entry = ttk.Entry(self)
        self.time_entry.grid(row=1, column=0, pady=5, padx=20)

        # 내용 입력
        ttk.Label(self, text="내용").grid(row=2, column=0, pady=10, padx=20, sticky="w")
        self.content_entry = ttk.Entry(self)
        self.content_entry.grid(row=3, column=0, pady=5, padx=20)

        # 빈도 선택
        ttk.Label(self, text="빈도").grid(row=4, column=0, pady=10, padx=20, sticky="w")
        self.frequency_var = tk.StringVar()
        self.frequency_var.set("once")
        self.frequency_combo = ttk.Combobox(self, textvariable=self.frequency_var, values=["once", "daily", "weekly", "monthly"], state='readonly')
        self.frequency_combo.grid(row=5, column=0, pady=5, padx=20)

        # 저장 버튼
        ttk.Button(self, text="저장", command=self.save_routine).grid(row=6, column=0, pady=20, padx=20)

    def save_routine(self):
        time = self.time_entry.get()
        content = self.content_entry.get()
        frequency = self.frequency_var.get()
        if not time or not content:
            messagebox.showerror("입력 오류", "모든 필드를 입력해주세요.")
            return
        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror("입력 오류", "시간 형식이 올바르지 않습니다.")
            return

        data = load_data()
        new_routine = {
            "time": time,
            "content": content,
            "frequency": frequency,
            "start_date": self.selected_date
        }
        if frequency == "once":
            new_routine["dates"] = [self.selected_date]
        data["routines"].append(new_routine)
        save_data(data)
        self.refresh()
        self.destroy()

# 반복 루틴 관리 창 클래스
class ManageRepeatingRoutinesWindow(tk.Toplevel):
    def __init__(self, master, refresh_main):
        super().__init__(master)
        self.title("반복 루틴 관리")
        self.geometry("400x300")
        self.refresh_main = refresh_main

        self.tree = ttk.Treeview(self, columns=("Time", "Content", "Frequency"), show='headings')
        self.tree.heading("Time", text="시간")
        self.tree.heading("Content", text="내용")
        self.tree.heading("Frequency", text="빈도")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.load_repeating_routines()

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="수정", command=self.modify_routine).pack(side=tk.LEFT, padx=20)
        ttk.Button(button_frame, text="삭제", command=self.delete_routine).pack(side=tk.RIGHT, padx=20)

    def load_repeating_routines(self):
        data = load_data()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, routine in enumerate(data["routines"]):
            if routine["frequency"] != "once":
                self.tree.insert("", "end", iid=idx, values=(routine["time"], routine["content"], routine["frequency"]))

    def modify_routine(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("선택 오류", "수정할 루틴을 선택해주세요.")
            return
        idx = int(selected)
        routine = load_data()["routines"][idx]
        ModifyRoutineWindow(self, idx, routine, self.load_repeating_routines, self.refresh_main)

    def delete_routine(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("선택 오류", "삭제할 루틴을 선택해주세요.")
            return
        idx = int(selected)
        data = load_data()
        del data["routines"][idx]
        save_data(data)
        self.load_repeating_routines()
        self.refresh_main()

# 루틴 수정 창 클래스
class ModifyRoutineWindow(tk.Toplevel):
    def __init__(self, master, idx, routine, refresh_list, refresh_main):
        super().__init__(master)
        self.title("루틴 수정")
        self.geometry("300x250")
        self.idx = idx
        self.routine = routine
        self.refresh_list = refresh_list
        self.refresh_main = refresh_main

        self.configure(bg="lightblue")

        # 시간 입력
        ttk.Label(self, text="시간 (HH:MM)").grid(row=0, column=0, pady=10, padx=20, sticky="w")
        self.time_entry = ttk.Entry(self)
        self.time_entry.insert(0, routine["time"])
        self.time_entry.grid(row=1, column=0, pady=5, padx=20)

        # 내용 입력
        ttk.Label(self, text="내용").grid(row=2, column=0, pady=10, padx=20, sticky="w")
        self.content_entry = ttk.Entry(self)
        self.content_entry.insert(0, routine["content"])
        self.content_entry.grid(row=3, column=0, pady=5, padx=20)

        # 빈도 선택
        ttk.Label(self, text="빈도").grid(row=4, column=0, pady=10, padx=20, sticky="w")
        self.frequency_var = tk.StringVar()
        self.frequency_var.set(routine["frequency"])
        self.frequency_combo = ttk.Combobox(self, textvariable=self.frequency_var, values=["once", "daily", "weekly", "monthly"], state='readonly')
        self.frequency_combo.grid(row=5, column=0, pady=5, padx=20)

        # 저장 버튼
        ttk.Button(self, text="저장", command=self.save_changes).grid(row=6, column=0, pady=20, padx=20)

    def save_changes(self):
        time = self.time_entry.get()
        content = self.content_entry.get()
        frequency = self.frequency_var.get()
        if not time or not content:
            messagebox.showerror("입력 오류", "모든 필드를 입력해주세요.")
            return
        try:
            datetime.strptime(time, "%H:%M")
        except ValueError:
            messagebox.showerror("입력 오류", "시간 형식이 올바르지 않습니다.")
            return

        data = load_data()
        data["routines"][self.idx]["time"] = time
        data["routines"][self.idx]["content"] = content
        data["routines"][self.idx]["frequency"] = frequency
        save_data(data)
        self.refresh_list()
        self.refresh_main()
        self.destroy()

# 메인 애플리케이션 클래스
class RoutineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("루틴 관리 프로그램")
        self.root.geometry("800x780")
        self.root.configure(bg='lightblue')

        # 현재 날짜 표시
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.selected_date = self.current_date

        # 캘린더 위젯
        self.calendar = Calendar(self.root, selectmode="day", year=int(self.selected_date[:4]), month=int(self.selected_date[5:7]), day=int(self.selected_date[8:10]))
        self.calendar.pack(pady=20)

        # 루틴 목록 표시
        self.routine_listbox = tk.Listbox(self.root, height=15, width=50, font=("Helvetica", 10))
        self.routine_listbox.pack(pady=10)

        # 버튼 프레임
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="루틴 추가", command=self.add_routine).pack(side=tk.LEFT, padx=20)
        ttk.Button(button_frame, text="반복 루틴 관리", command=self.manage_repeating_routines).pack(side=tk.LEFT, padx=20)

        # 데이터 로드 후 루틴 표시
        self.load_routines()

    def load_routines(self):
        self.routine_listbox.delete(0, tk.END)
        data = load_data()
        for routine in data["routines"]:
            if routine["start_date"] == self.selected_date:
                self.routine_listbox.insert(tk.END, f"{routine['time']} - {routine['content']} ({routine['frequency']})")

    def add_routine(self):
        AddRoutineWindow(self.root, self.selected_date, self.load_routines)

    def manage_repeating_routines(self):
        ManageRepeatingRoutinesWindow(self.root, self.load_routines)

if __name__ == "__main__":
    root = tk.Tk()
    app = RoutineApp(root)
    root.mainloop()
