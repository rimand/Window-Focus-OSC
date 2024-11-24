# ฺBasic Select Program

import tkinter as tk
import pygetwindow as gw

def focus_window(window_title):
    """ฟังก์ชันโฟกัสไปยังหน้าต่างโปรแกรมที่เลือก"""
    window = next((win for win in gw.getWindowsWithTitle(window_title) if win.visible), None)
    if window:
        window.activate()
    else:
        print(f"ไม่พบหน้าต่าง {window_title}")

def refresh_buttons():
    """ฟังก์ชันล้างปุ่มเก่าและสร้างปุ่มใหม่"""
    # ล้างปุ่มเก่าออก ยกเว้นปุ่ม Refresh
    for widget in frame.winfo_children():
        widget.destroy()
    create_buttons()

def create_buttons():
    """ฟังก์ชันสร้างปุ่มสำหรับโปรแกรมที่มีหน้าต่างมองเห็นได้"""
    windows = gw.getWindowsWithTitle("")  # ดึงหน้าต่างทั้งหมด
    visible_windows = [win for win in windows if win.visible and win.title.strip()]
    unique_windows = list({win.title: win for win in visible_windows}.values())  # กรองชื่อหน้าต่างที่ซ้ำกัน
    
    filtered_windows = [win for win in unique_windows if not any(
        keyword in win.title.lower() for keyword in ["mail", "calculator", "settings", "photos", "microsoft"]
    )]

    for win in filtered_windows:
        title = win.title
        window_type = f"Class: {win._hWnd}"  # ใช้ `win._hWnd` หรือปรับตามข้อมูลอื่นหากต้องการ
        button_text = f"{title} ({window_type})"
        
        # สร้างปุ่มสำหรับโปรแกรมแต่ละตัว
        button = tk.Button(frame, text=button_text, command=lambda t=title: focus_window(t))
        button.pack(fill=tk.X, padx=10, pady=5)

# สร้างหน้าต่าง GUI
root = tk.Tk()
root.title("เลือกโปรแกรม")
root.geometry("600x800")  # ขยายขนาดหน้าต่างสำหรับข้อมูลเพิ่มเติม

# สร้างเฟรมสำหรับปุ่ม
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# สร้างปุ่มสำหรับหน้าต่างโปรแกรม
create_buttons()

# สร้างปุ่ม Refresh (สร้างเพียงครั้งเดียว)
refresh_button = tk.Button(root, text="Refresh Programs", command=refresh_buttons, bg="lightblue")
refresh_button.pack(fill=tk.X, padx=10, pady=10)

# เริ่มต้นแอปพลิเคชัน
root.mainloop()
