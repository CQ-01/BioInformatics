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

# 루틴 추가 창 클래스
class AddRoutineWindow(tk.Toplevel):
    def __init__(self, master, selected_date, refresh):
        super().__init__(master)
        self.title("루틴 추가")
        self.geometry("300x250")
        self.selected_date = selected_date
        self.refresh = refresh

        # 시간 입력
        tk.Label(self, text="시간 (HH:MM)").pack(pady=5)
        self.time_entry = tk.Entry(self)
        self.time_entry.pack(pady=5)

        # 내용 입력
        tk.Label(self, text="내용").pack(pady=5)
        self.content_entry = tk.Entry(self)
        self.content_entry.pack(pady=5)

        # 빈도 선택
        tk.Label(self, text="빈도").pack(pady=5)
        self.frequency_var = tk.StringVar()
        self.frequency_var.set("once")
        ttk.Combobox(self, textvariable=self.frequency_var, values=["once", "daily", "weekly", "monthly"], state='readonly').pack(pady=5)

        # 저장 버튼
        tk.Button(self, text="저장", command=self.save_routine).pack(pady=20)

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

        tk.Button(self, text="수정", command=self.modify_routine).pack(side=tk.LEFT, padx=20, pady=10)
        tk.Button(self, text="삭제", command=self.delete_routine).pack(side=tk.RIGHT, padx=20, pady=10)

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

        # 시간 입력
        tk.Label(self, text="시간 (HH:MM)").pack(pady=5)
        self.time_entry = tk.Entry(self)
        self.time_entry.insert(0, routine["time"])
        self.time_entry.pack(pady=5)

        # 내용 입력
        tk.Label(self, text="내용").pack(pady=5)
        self.content_entry = tk.Entry(self)
        self.content_entry.insert(0, routine["content"])
        self.content_entry.pack(pady=5)

        # 빈도 선택
        tk.Label(self, text="빈도").pack(pady=5)
        self.frequency_var = tk.StringVar()
        self.frequency_var.set(routine["frequency"])
        ttk.Combobox(self, textvariable=self.frequency_var, values=["once", "daily", "weekly", "monthly"], state='readonly').pack(pady=5)

        # 저장 버튼
        tk.Button(self, text="저장", command=self.save_changes).pack(pady=20)

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
        self.root.configure(bg='white')

        # 현재 날짜 표시
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.selected_date = self.current_date
        self.date_label = tk.Label(root, text=self.current_date, font=("Helvetica", 18, "bold"), bg="white")
        self.date_label.pack(pady=20)

        # 날짜 선택
        self.calendar = Calendar(root, firstweekday='sunday', mindate=datetime(2020,1,1), maxdate=datetime(2030,12,31))
        self.calendar.pack(pady=20)
        self.calendar.bind("<<CalendarSelected>>", self.on_date_select)

        # 루틴 리스트
        self.routine_frame = tk.Frame(root, bg="white")
        self.routine_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        self.refresh_routines()

        # 버튼 프레임
        btn_frame = tk.Frame(root, bg="white")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="루틴 추가", command=self.open_add_routine, bg ="whitesmoke", relief="raised").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="반복 루틴 관리", command=self.open_manage_repeating, bg="whitesmoke", relief="raised").pack(side=tk.LEFT, padx=10)

    def on_date_select(self, event):
        self.selected_date = self.calendar.selection_get().strftime("%Y-%m-%d")
        self.date_label.config(text=self.selected_date)
        self.refresh_routines()

    def open_add_routine(self):
        AddRoutineWindow(self.root, self.selected_date, self.refresh_routines)

    def open_manage_repeating(self):
        ManageRepeatingRoutinesWindow(self.root, self.refresh_routines)

    def refresh_routines(self):
        for widget in self.routine_frame.winfo_children():
            widget.destroy()
            
        data = load_data()
        routines_today = []
        
        for routine in data["routines"]:
            if routine["frequency"] == "once":
                if routine["dates"] and self.selected_date in routine["dates"]:
                    routines_today.append(routine)
            else:
                start_date = datetime.strptime(routine["start_date"], "%Y-%m-%d")
                current = datetime.strptime(self.selected_date, "%Y-%m-%d")
                if current < start_date:
                    continue
                if routine["frequency"] == "daily":
                    routines_today.append(routine)
                elif routine["frequency"] == "weekly":
                    delta = current - start_date
                    if delta.days % 7 == 0:
                        routines_today.append(routine)
                elif routine["frequency"] == "monthly":
                    if start_date.day == current.day:
                        routines_today.append(routine)

        # 시간 순으로 정렬 (HH:MM 형식의 문자열을 datetime으로 변환하여 정렬)
        routines_today.sort(key=lambda r: datetime.strptime(r["time"], "%H:%M"))

        for idx, routine in enumerate(routines_today):
            frame = tk.Frame(self.routine_frame)
            frame.pack(fill=tk.X, pady=2)
            
            # once 빈도 루틴 강조 표시 (배경색 변경)
            if routine["frequency"] == "once":
                frame.config(bg="yellow")  # 강조할 색을 원하는 색으로 설정
            
            var = tk.IntVar()
            chk = tk.Checkbutton(frame, variable=var)
            chk.pack(side=tk.RIGHT, padx=5)
            
            # 강조 색이 적용된 라벨
            label = tk.Label(frame, text=f"{routine['time']} - {routine['content']}")
            label.pack(side=tk.LEFT, padx=5)
            
            # 수정 버튼
            tk.Button(frame, text="수정", command=lambda r=routine: self.modify_routine(r)).pack(side=tk.RIGHT, padx=5)
            
            # 삭제 버튼
            tk.Button(frame, text="삭제", command=lambda r=routine: self.delete_routine(r)).pack(side=tk.RIGHT, padx=5)


    def modify_routine(self, routine):
        data = load_data()
        idx = data["routines"].index(routine)
        
        # 루틴이 "once"일 경우에는 수정 가능
        if routine["frequency"] == "once":
            ModifyRoutineWindow(self.root, idx, routine, self.refresh_routines, self.refresh_routines)
            return

        # "daily", "weekly", "monthly" 루틴은 당일만 수정 가능
        today = datetime.strptime(self.selected_date, "%Y-%m-%d")
        start_date = datetime.strptime(routine["start_date"], "%Y-%m-%d")
        
        if routine["frequency"] == "daily" and today >= start_date:
            ModifyRoutineWindow(self.root, idx, routine, self.refresh_routines, self.refresh_routines)
        elif routine["frequency"] == "weekly":
            delta = today - start_date
            if delta.days % 7 == 0:  # 오늘이 주기적으로 반복되는 주기인 경우
                ModifyRoutineWindow(self.root, idx, routine, self.refresh_routines, self.refresh_routines)
        elif routine["frequency"] == "monthly":
            if today.day == start_date.day:  # 오늘이 월별 반복 주기인 경우
                ModifyRoutineWindow(self.root, idx, routine, self.refresh_routines, self.refresh_routines)
        else:
            messagebox.showinfo("수정 불가", "이 루틴은 오늘 수정할 수 없습니다.")

    def delete_routine(self, routine):
        data = load_data()
        idx = data["routines"].index(routine)
        
        # 루틴이 "once"일 경우에는 삭제 가능
        if routine["frequency"] == "once":
            data["routines"].remove(routine)
            save_data(data)
            self.refresh_routines()
            return

        # "daily", "weekly", "monthly" 루틴은 당일만 삭제 가능
        today = datetime.strptime(self.selected_date, "%Y-%m-%d")
        start_date = datetime.strptime(routine["start_date"], "%Y-%m-%d")

        if routine["frequency"] == "daily" and today >= start_date:
            data["routines"].remove(routine)
            save_data(data)
            self.refresh_routines()
        elif routine["frequency"] == "weekly":
            delta = today - start_date
            if delta.days % 7 == 0:  # 오늘이 주기적으로 반복되는 주기인 경우
                data["routines"].remove(routine)
                save_data(data)
                self.refresh_routines()
        elif routine["frequency"] == "monthly":
            if today.day == start_date.day:  # 오늘이 월별 반복 주기인 경우
                data["routines"].remove(routine)
                save_data(data)
                self.refresh_routines()
        else:
            messagebox.showinfo("삭제 불가", "이 루틴은 오늘 삭제할 수 없습니다.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RoutineApp(root)
    root.mainloop()
