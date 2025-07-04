import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import cv2
import os
import threading
import numpy as np

PASSWORD_FILE = "passwords.txt"
LOG_FILE = "login_attempts.txt"
IMAGE_PATH = "hack.png"
VIDEO_SAVE_PATH = "videos/"

class ModernButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#3498db", fg="white", font=("Arial", 14, "bold"), relief=tk.FLAT)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.configure(padx=10, pady=5)

    def on_enter(self, event):
        self.configure(bg="#2980b9")

    def on_leave(self, event):
        self.configure(bg="#3498db")

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Webcam Spyware Security")
        self.root.geometry("700x600")
        self.root.configure(bg="#ecf0f1")

        self.locked_cap = None  # Camera lock reference

        # Load button icons
        self.enable_icon = ImageTk.PhotoImage(Image.open("enable_icon.png").resize((20, 20)))
        self.disable_icon = ImageTk.PhotoImage(Image.open("disable_icon.png").resize((20, 20)))
        self.change_icon = ImageTk.PhotoImage(Image.open("change_icon.png").resize((20, 20)))
        self.log_icon = ImageTk.PhotoImage(Image.open("log_icon.png").resize((20, 20)))

        self.header_frame = tk.Frame(self.root, bg="#3498db", pady=10)
        self.header_frame.pack(fill=tk.X)

        self.title_label = tk.Label(self.header_frame, text="Camera Security System", font=("Arial", 18, "bold"),
                                    fg="white", bg="#3498db")
        self.title_label.pack(pady=10)

        self.login_frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        self.login_frame.pack(pady=20)

        self.image = self.load_image(IMAGE_PATH, (300, 150))
        self.image_label = tk.Label(self.login_frame, image=self.image, bg="#ecf0f1")
        self.image_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.lbl_password = tk.Label(self.login_frame, text="Password:", font=("Arial", 14, "bold"), fg="black", bg="#ecf0f1")
        self.lbl_password.grid(row=1, column=0, padx=10, pady=10)

        self.entry_password = tk.Entry(self.login_frame, show="*", font=("Arial", 14), fg="black", borderwidth=2, relief="solid")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.btn_login = ModernButton(self.login_frame, text="Login", command=self.login)
        self.btn_login.grid(row=1, column=2, padx=10, pady=10)

        self.btn_change_password = ModernButton(
            self.root, text="Change Password", image=self.change_icon, compound="left",
            command=self.change_password, state=tk.DISABLED)
        self.btn_change_password.pack(pady=10)

        self.btn_enable_camera_app = ModernButton(
            self.root, text="Enable Camera", image=self.enable_icon, compound="left",
            command=self.verify_password_and_enable_camera, state=tk.DISABLED)
        self.btn_enable_camera_app.pack(pady=10)

        self.btn_disable_camera = ModernButton(
            self.root, text="Disable Camera", image=self.disable_icon, compound="left",
            command=self.verify_password_and_disable_camera, state=tk.DISABLED)
        self.btn_disable_camera.pack(pady=10)

        self.btn_log_details = ModernButton(
            self.root, text="Log Details", image=self.log_icon, compound="left",
            command=self.view_log_details, state=tk.DISABLED)
        self.btn_log_details.pack(pady=10)

        self.load_passwords()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        if not os.path.exists(VIDEO_SAVE_PATH):
            os.makedirs(VIDEO_SAVE_PATH)

    def load_image(self, path, size):
        try:
            image = Image.open(path)
            image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")
            return None

    def load_passwords(self):
        try:
            with open(PASSWORD_FILE, "r") as f:
                self.passwords = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            self.passwords = []

    def save_passwords(self):
        with open(PASSWORD_FILE, "w") as f:
            for password in self.passwords:
                f.write(password + "\n")

    def log_attempt(self, action, success):
        attempt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Success" if success else "Failure"
        log_entry = f"{attempt_time} - {action} - {status}\n"
        with open(LOG_FILE, "a") as log_file:
            log_file.write(log_entry)

    def login(self):
        entered_password = self.entry_password.get()
        if entered_password in self.passwords:
            messagebox.showinfo("Success", "Login successful!")
            self.login_frame.pack_forget()
            self.btn_change_password.config(state=tk.NORMAL)
            self.btn_enable_camera_app.config(state=tk.NORMAL)
            self.btn_disable_camera.config(state=tk.NORMAL)
            self.btn_log_details.config(state=tk.NORMAL)
            self.log_attempt("Login", success=True)
        else:
            messagebox.showerror("Error", "Incorrect password!")
            self.log_attempt("Login", success=False)
            threading.Thread(target=self.record_video).start()

    def change_password(self):
        current_password = simpledialog.askstring("Change Password", "Enter current password:", show="*")
        if current_password in self.passwords:
            new_password = simpledialog.askstring("Change Password", "Enter new password:", show="*")
            if new_password:
                self.passwords = [new_password]
                self.save_passwords()
                messagebox.showinfo("Success", "Password changed successfully!")
        else:
            messagebox.showerror("Error", "Current password is incorrect!")

    def verify_password(self):
        entered_password = simpledialog.askstring("Password Required", "Enter password to continue:", show="*")
        if entered_password in self.passwords:
            return True
        else:
            messagebox.showerror("Error", "Incorrect password!")
            return False

    def verify_password_and_enable_camera(self):
        if self.verify_password():
            self.enable_camera_app()
            self.log_attempt("Enable Camera", success=True)
        else:
            self.log_attempt("Enable Camera", success=False)

    def verify_password_and_disable_camera(self):
        if self.verify_password():
            self.disable_camera()
            self.log_attempt("Disable Camera", success=True)
        else:
            self.log_attempt("Disable Camera", success=False)

    def enable_camera_app(self):
        try:
            if self.locked_cap and self.locked_cap.isOpened():
                self.locked_cap.release()
                self.locked_cap = None
            messagebox.showinfo("Camera", "Camera access is now enabled.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enable camera: {e}")

    def disable_camera(self):
        permission = messagebox.askyesno("Disable Camera", "Do you want to lock the camera?")
        if not permission:
            return
        threading.Thread(target=self.hold_camera_background, daemon=True).start()

    def hold_camera_background(self):
        try:
            if self.locked_cap and self.locked_cap.isOpened():
                return
            self.locked_cap = cv2.VideoCapture(0)
            if not self.locked_cap.isOpened():
                print("Camera is already locked or unavailable.")
                return
            while True:
                ret, frame = self.locked_cap.read()
                if not ret:
                    break
                cv2.waitKey(100)
        except Exception as e:
            print("Error while locking camera:", e)

    def record_video(self):
        try:
            cap = cv2.VideoCapture(0)
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            video_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".avi"
            video_path = os.path.join(VIDEO_SAVE_PATH, video_filename)
            out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
            for _ in range(20):
                ret, frame = cap.read()
                if ret:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    out.write(frame)
                else:
                    break
            cap.release()
            out.release()
        except Exception as e:
            print(f"Failed to record video: {e}")

    def view_log_details(self):
        try:
            with open(LOG_FILE, "r") as log_file:
                log_content = log_file.read()
        except FileNotFoundError:
            log_content = "No login attempts recorded yet."
        log_window = tk.Toplevel(self.root)
        log_window.title("Login Attempt Log")
        log_window.geometry("400x300")
        log_window.configure(bg="#ecf0f1")
        log_text = tk.Text(log_window, wrap=tk.WORD, font=("Arial", 12), bg="#ecf0f1", fg="black", borderwidth=2, relief="solid")
        log_text.insert(tk.END, log_content)
        log_text.config(state=tk.DISABLED)
        log_text.pack(expand=True, fill=tk.BOTH)

    def on_closing(self):
        try:
            if self.locked_cap and self.locked_cap.isOpened():
                self.locked_cap.release()
        except:
            pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
