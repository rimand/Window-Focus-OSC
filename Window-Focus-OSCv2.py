# ฺBasic Select Program
#มีการกรองชื่อ Program และจัดลำดับเองได้

import tkinter as tk
import pygetwindow as gw
import os

def focus_window(window_title):
    """ฟังก์ชันโฟกัสไปยังหน้าต่างโปรแกรมที่เลือก"""
    window = next((win for win in gw.getWindowsWithTitle(window_title) if win.visible), None)
    if window:
        window.activate()
    else:
        print(f"ไม่พบหน้าต่าง {window_title}")

def log_program_names():
    """บันทึกรายชื่อโปรแกรมที่พบในระบบลงไฟล์ log.txt"""
    windows = gw.getWindowsWithTitle("")  # ดึงหน้าต่างทั้งหมด
    visible_windows = [win.title.strip() for win in windows if win.visible and win.title.strip()]
    
    # เขียนชื่อโปรแกรมลง log.txt
    with open("log.txt", "w", encoding="utf-8") as log_file:
        for title in visible_windows:
            log_file.write(title + "\n")
    print("บันทึกชื่อโปรแกรมใน log.txt เรียบร้อยแล้ว!")

def load_program_list():
    """โหลดรายการโปรแกรมจากไฟล์ list.txt"""
    if not os.path.exists("list.txt"):
        print("ไม่พบไฟล์ list.txt")
        return []
    with open("list.txt", "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

def adjust_window_size():
    """ปรับขนาดหน้าต่าง GUI ตามจำนวนปุ่มและความกว้างของชื่อโปรแกรม"""
    num_buttons = len(frame.winfo_children())
    button_height = 40  # ความสูงโดยประมาณของปุ่ม (พิกเซล)
    base_height = 100   # ความสูงพื้นฐาน (พิกเซล)
    offset_height = 50  # เผื่อพื้นที่ด้านล่าง (พิกเซล)
    new_height = min(800, max(base_height + num_buttons * button_height + offset_height, 200))  # จำกัดความสูงสูงสุด
    
    # คำนวณความกว้างตามชื่อโปรแกรมที่ยาวที่สุด
    longest_title = max((button.cget("text") for button in frame.winfo_children()), key=len, default="")
    char_width = 8  # ความกว้างโดยประมาณของตัวอักษร (พิกเซล)
    base_width = 300  # ความกว้างพื้นฐาน (พิกเซล)
    offset_width = 50  # เผื่อพื้นที่ด้านข้าง (พิกเซล)
    new_width = min(1200, max(base_width, len(longest_title) * char_width + offset_width))  # จำกัดความกว้างสูงสุด
    
    # ตั้งค่าขนาดหน้าต่าง
    root.geometry(f"{new_width}x{new_height}")

def create_buttons():
    """สร้างปุ่มสำหรับโปรแกรมที่ตรงกับชื่อใน list.txt"""
    program_list = load_program_list()  # โหลดรายการโปรแกรมจากไฟล์
    windows = gw.getWindowsWithTitle("")  # ดึงหน้าต่างทั้งหมด
    visible_windows = {win.title: win for win in windows if win.visible and win.title.strip()}

    for program_name in program_list:
        if program_name in visible_windows:
            # สร้างปุ่มเฉพาะโปรแกรมที่พบในหน้าต่างที่มองเห็นได้
            button = tk.Button(frame, text=program_name, command=lambda t=program_name: focus_window(t))
            button.pack(fill=tk.X, padx=10, pady=5)
        else:
            print(f"ไม่พบโปรแกรมในหน้าต่าง: {program_name}")
    
    # ปรับขนาดหน้าต่าง GUI
    adjust_window_size()

def refresh_buttons():
    """รีเฟรชปุ่มโปรแกรม"""
    for widget in frame.winfo_children():
        widget.destroy()
    create_buttons()

# สร้างหน้าต่าง GUI
root = tk.Tk()
root.title("เลือกโปรแกรม")
root.geometry("400x200")  # ค่าเริ่มต้นขนาดหน้าต่าง

# สร้างเฟรมสำหรับปุ่ม
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# บันทึกรายชื่อโปรแกรมลง log.txt
log_program_names()

# สร้างปุ่มสำหรับหน้าต่างโปรแกรม
create_buttons()

# สร้างปุ่ม Refresh
refresh_button = tk.Button(root, text="Refresh Programs", command=refresh_buttons, bg="lightblue")
refresh_button.pack(fill=tk.X, padx=10, pady=10)

# เริ่มต้นแอปพลิเคชัน
root.mainloop()
