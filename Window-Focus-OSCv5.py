# ฺBasic Select Program
#มีการกรองชื่อ Program และจัดลำดับเองได้
#มี OSC ควบคุม Program
#OSC Path : /program [value] ; value : ลำดับ Program เริ่มที่ 1->....
#เปลี่ยน port ได้
#แก้ปัญหาเมื่อไปกด Program อื่นเราทำงานไม่ได้


import tkinter as tk
from tkinter import messagebox
import pygetwindow as gw
import os
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import threading
from pywinauto import Application
from pywinauto.findwindows import find_window

osc_port = 7005
osc_server_thread = None
gui_window_title = "Window-Focus-OSCv5"  # ชื่อหน้าต่าง GUI ของตัวเอง

def log_program_names():
    """บันทึกรายชื่อโปรแกรมที่พบในระบบลงไฟล์ log.txt"""
    windows = gw.getWindowsWithTitle("")  # ดึงหน้าต่างทั้งหมด
    visible_windows = [win.title.strip() for win in windows if win.visible and win.title.strip()]
    
    # เขียนชื่อโปรแกรมลง log.txt
    with open("log.txt", "w", encoding="utf-8") as log_file:
        for title in visible_windows:
            log_file.write(title + "\n")
    print("บันทึกชื่อโปรแกรมใน log.txt เรียบร้อยแล้ว!")


def start_osc_server():
    global osc_server_thread
    dispatcher = Dispatcher()
    dispatcher.map("/program", handle_osc_program)

    server = BlockingOSCUDPServer(("0.0.0.0", osc_port), dispatcher)
    print(f"OSC Server started on port {osc_port}")
    server.serve_forever()


def restart_osc_server(new_port):
    global osc_server_thread, osc_port
    osc_port = new_port
    if osc_server_thread and osc_server_thread.is_alive():
        print("หยุด OSC Server เก่า...")
    osc_server_thread = threading.Thread(target=start_osc_server, daemon=True)
    osc_server_thread.start()
    print(f"OSC Server ถูกเปลี่ยนเป็นพอร์ต {osc_port}")


def handle_osc_program(address, *args):
    """ฟังก์ชันจัดการ OSC สำหรับ path /program"""
    program_list = load_program_list()
    if len(args) > 0:
        index = int(args[0]) - 1
        if 0 <= index < len(program_list):
            program_name = program_list[index]
            print(f"รับคำสั่ง OSC: โฟกัสโปรแกรมลำดับที่ {index + 1}: {program_name}")
            focus_window_with_pywinauto(program_name)
        else:
            print(f"ค่าลำดับไม่ถูกต้องจาก OSC: {args[0]}")

def refresh_and_focus(window_title):
    print(f"รีเฟรชสถานะหน้าต่างก่อนโฟกัส: {window_title}")
    refresh_buttons()
    focus_window(window_title)


def focus_window(window_title):
    """ฟังก์ชันตรวจสอบและบังคับโฟกัสไปยังหน้าต่างที่ต้องการ"""
    try:
        # รีเฟรชสถานะหน้าต่าง
        windows = gw.getWindowsWithTitle("")  # ดึงหน้าต่างทั้งหมด
        target_window = None

        # ค้นหาหน้าต่างที่ตรงกับชื่อ
        for win in windows:
            if win.title == window_title and win.visible:
                target_window = win
                break

        if not target_window:
            print(f"ไม่พบหน้าต่างที่ตรงกับชื่อ: {window_title}")
            return

        # จัดการสถานะหน้าต่าง
        if target_window.isMinimized:
            print(f"หน้าต่าง {window_title} ถูกย่อขนาด กำลังกู้คืน...")
            target_window.restore()

        # บังคับโฟกัสหน้าต่าง
        print(f"โฟกัสไปที่หน้าต่าง: {window_title}")
        target_window.activate()

    except gw.PyGetWindowException as e:
        print(f"ข้อผิดพลาดขณะจัดการหน้าต่าง: {e}")

def focus_window_with_pywinauto(window_title):
    """ใช้ pywinauto เพื่อโฟกัสหน้าต่าง"""
    try:
        # ค้นหา handle ของหน้าต่างที่ตรงกับชื่อ
        handle = find_window(title=window_title)
        if not handle:
            print(f"ไม่พบหน้าต่างที่ตรงกับชื่อ: {window_title}")
            return

        # เชื่อมต่อกับหน้าต่าง
        app = Application().connect(handle=handle)
        window = app.window(handle=handle)

        # นำหน้าต่างกลับมาด้านหน้า
        window.set_focus()
        print(f"โฟกัสหน้าต่างสำเร็จ: {window_title}")
    except Exception as e:
        print(f"ข้อผิดพลาดขณะโฟกัสหน้าต่างด้วย pywinauto: {e}")


def load_program_list():
    if not os.path.exists("list.txt"):
        print("ไม่พบไฟล์ list.txt")
        return []
    with open("list.txt", "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def refresh_buttons():
    for widget in frame.winfo_children():
        widget.destroy()
    create_buttons()


def create_buttons():
    program_list = load_program_list()
    windows = gw.getWindowsWithTitle("")
    visible_windows = {win.title: win for win in windows if win.visible and win.title.strip()}

    for program_name in program_list:
        if program_name in visible_windows:
            button = tk.Button(frame, text=program_name, command=lambda t=program_name: focus_window(t))
            button.pack(fill=tk.X, padx=10, pady=5)
        else:
            print(f"ไม่พบโปรแกรมในหน้าต่าง: {program_name}")


def change_osc_port():
    global osc_port
    try:
        new_port = int(port_entry.get())
        if new_port < 1024 or new_port > 65535:
            messagebox.showerror("พอร์ตไม่ถูกต้อง", "กรุณาใส่พอร์ตระหว่าง 1024-65535")
            return
        print(f"กำลังเปลี่ยนพอร์ต OSC เป็น {new_port}")
        restart_osc_server(new_port)
    except ValueError:
        messagebox.showerror("ข้อผิดพลาด", "กรุณาใส่หมายเลขพอร์ตที่ถูกต้อง")


# สร้างหน้าต่าง GUI
root = tk.Tk()
root.title(gui_window_title)
root.geometry("500x600")

# ช่องป้อนพอร์ต OSC
port_frame = tk.Frame(root)
port_frame.pack(anchor="ne", padx=10, pady=10)
port_label = tk.Label(port_frame, text="OSC Port:")
port_label.pack(side="left")
port_entry = tk.Entry(port_frame, width=6)
port_entry.insert(0, str(osc_port))
port_entry.pack(side="left")
port_button = tk.Button(port_frame, text="Change port", command=change_osc_port)
port_button.pack(side="left")

# เฟรมสำหรับปุ่มโปรแกรม
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# ปุ่ม Refresh (วางไว้ล่างสุด)
refresh_button = tk.Button(root, text="Refresh Programs", command=refresh_buttons, bg="lightblue")
refresh_button.pack(side="bottom", fill=tk.X, padx=10, pady=10)

# บันทึกรายชื่อโปรแกรมลง log.txt
log_program_names()

# สร้างปุ่มโปรแกรม
create_buttons()

# เริ่มต้น OSC Server
osc_server_thread = threading.Thread(target=start_osc_server, daemon=True)
osc_server_thread.start()

hint_label = tk.Label(root, text="/program [value] ; value is 1,2,3...", bg="white", fg="gray")
hint_label.pack(side="bottom", fill=tk.X, pady=5)

# เริ่มต้นแอปพลิเคชัน
root.mainloop()

