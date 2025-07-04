# 🔐 Webcam Spyware Security System

This is a Python-based **GUI security system** built using `Tkinter`, designed to secure access to your webcam and log unauthorized access attempts. It includes a **password-protected login**, camera **enable/disable control**, **video recording on failed login**, and an interactive **log viewer** — all wrapped in a modern interface.

---

## 📌 Features

- 🎨 **Modern Tkinter GUI** with styled buttons and icons
- 🔐 **Password-Protected Access** to camera features
- 🎥 **Auto Video Recording** on failed login attempts
- 🔒 **Camera Locking Mechanism** to block access
- 📁 **Login Attempts Logging** with timestamp and status
- ✨ **Enable/Disable Camera** with a password prompt
- 🔄 **Change Password** securely in the app
- 🗂️ **View Login Logs** in a separate window
- 🖼️ Uses `Pillow` to load icons and images attractively

---

## 📂 Folder Structure

project/
│
├── hack.png # Display image on login screen
├── enable_icon.png # Icon for enable camera button
├── disable_icon.png # Icon for disable camera button
├── change_icon.png # Icon for change password button
├── log_icon.png # Icon for view logs button
├── passwords.txt # Stored passwords
├── login_attempts.txt # Login attempt logs
├── videos/ # Folder to store recorded videos
└── webcam_security.py # Main Python GUI application


---

## 🚀 Getting Started

### 1. Install Dependencies

Make sure you have Python 3 and the required libraries installed:

```bash
pip install pillow opencv-python
python webcam_security.py
📷 How It Works
On incorrect password entry:

A short video is recorded from the webcam

The attempt is logged with a timestamp

On successful login:

You gain access to:

Change password

Enable/Disable camera

View all login attempts

🔒 Security Note
Passwords are stored in plain text (passwords.txt). In production, use encryption for secure storage.

This app is a prototype and should be enhanced before deploying in sensitive environments.

🛠 Built With
Python 3

Tkinter (GUI)

Pillow (Image handling)

OpenCV (Webcam & video processing)

📄 License
This project is open-source and available under the MIT License.

🙋‍♂️ Author
Vinay Kumar
Final Year B.Tech Student – CSE (AI & ML)
GitHub Profile : https://github.com/vinaykumar-05
LinkedIn : https://www.linkedin.com/in/vinay-kakumani/
