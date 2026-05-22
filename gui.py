# gui.py
import tkinter as tk
from tkinter import ttk
import math
import queue

class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("J.A.R.V.I.S. Core Interface")
        self.root.geometry("480x680")
        self.root.configure(bg="#02060e")
        
        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 1. Outer Tech Accent Top Bar
        self.top_line = tk.Frame(root, height=2, bg="#00f0ff")
        self.top_line.pack(fill=tk.X, side=tk.TOP)
        
        # 2. HUD Technical Header Labels
        self.title_label = tk.Label(
            root, text="MAIN SYSTEM STATUS // SECURE", 
            font=("Lucida Console", 11, "bold"), fg="#00f0ff", bg="#02060e"
        )
        self.title_label.pack(pady=(20, 5))
        
        self.version_label = tk.Label(
            root, text="A.Y. SYSTEMS V3.0 // AVATAR ENGAGED", 
            font=("Lucida Console", 8), fg="#005577", bg="#02060e"
        )
        self.version_label.pack(pady=(0, 15))
        
        # 3. Fluid Centering Container for Vector Graphics Canvas
        self.canvas_container = tk.Frame(root, bg="#02060e")
        self.canvas_container.pack(fill=tk.X, expand=False)
        
        # 4. Central Vector Graphics Canvas (Character Array)
        self.canvas = tk.Canvas(self.canvas_container, width=320, height=260, bg="#02060e", highlightthickness=0)
        self.canvas.pack(pady=10, anchor="center")
        
        # Animation State Variables
        self.current_state = "idle"  # idle, listening, speaking
        self.anim_tick = 0
        
        # Safe data transfer queue channel
        self.log_queue = queue.Queue()
        
        # Generate character layout
        self.build_vector_character_avatar()
        
        # 5. Live Status Indicator Dashboard Label
        self.status_label = tk.Label(
            root, text="STATUS: ONLINE & STANDBY", 
            font=("Lucida Console", 12, "bold"), fg="#00a8ff", bg="#02060e"
        )
        self.status_label.pack(pady=15)
        
        # 6. Responsive Console Logging Container Frame
        self.log_container = tk.Frame(root, bg="#02060e")
        self.log_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 25))
        
        # 7. Scrolling Dialogue Console Box Widget
        self.dialog_box = tk.Text(
            self.log_container, font=("Consolas", 10),
            bg="#040a14", fg="#a2b7cd", highlightbackground="#002233", 
            highlightcolor="#00f0ff", highlightthickness=1, bd=0, padx=12, pady=12
        )
        self.dialog_box.pack(fill=tk.BOTH, expand=True)
        self.dialog_box.insert(tk.END, " >> AVATAR CORE SYNCHRONIZED WITH WINRT CORE...\n")
        self.dialog_box.config(state=tk.DISABLED)
        
        # Launch non-blocking animation updates and text loops
        self.refresh_avatar_animation()
        self.process_incoming_queue_logs()

    def build_vector_character_avatar(self):
        """Draws character line vectors"""
        self.canvas.create_oval(40, 10, 280, 250, outline="#001a2e", width=1, dash=(3, 3))
        self.canvas.create_line(160, 0, 160, 260, fill="#001122", width=1)
        
        face_coordinates = [120, 80, 200, 80, 210, 150, 160, 200, 110, 150]
        self.face_base = self.canvas.create_polygon(face_coordinates, outline="#00f0ff", fill="#051529", width=2)
        
        self.eye_left = self.canvas.create_line(140, 115, 160, 118, fill="#00f0ff", width=3)
        self.eye_right = self.canvas.create_line(180, 118, 200, 115, fill="#00f0ff", width=3)
        
        self.pupil_l = self.canvas.create_oval(146, 122, 154, 134, fill="#00ffcc", outline="")
        self.pupil_r = self.canvas.create_oval(186, 122, 194, 134, fill="#00ffcc", outline="")
        
        self.canvas.create_line(135, 142, 142, 146, fill="#ff0066", width=1)
        self.canvas.create_line(205, 142, 198, 146, fill="#ff0066", width=1)
        
        self.canvas.create_line(110, 75, 160, 50, fill="#00f0ff", width=2)
        self.canvas.create_line(160, 50, 210, 75, fill="#00f0ff", width=2)
        self.earpiece_l = self.canvas.create_rectangle(105, 90, 118, 135, fill="#00f0ff", outline="")
        self.earpiece_r = self.canvas.create_rectangle(202, 90, 215, 135, fill="#00f0ff", outline="")
        
        self.mouth = self.canvas.create_line(152, 165, 168, 165, fill="#00f0ff", width=2)

    def refresh_avatar_animation(self):
        """Handles smooth frame updates"""
        try:
            self.anim_tick += 1
            if self.anim_tick > 360: self.anim_tick = 0
            rad = math.radians(self.anim_tick * 5)
            
            if self.current_state == "listening":
                offset = math.sin(rad) * 3
                self.canvas.coords(self.pupil_l, 146, 122 + (offset/2), 154, 134 + (offset/2))
                self.canvas.coords(self.pupil_r, 186, 122 + (offset/2), 194, 134 + (offset/2))
                self.canvas.itemconfig(self.mouth, fill="#00ffcc")
                self.canvas.coords(self.mouth, 154, 165, 166, 165)
            elif self.current_state == "speaking":
                mouth_open = abs(math.sin(rad * 1.5)) * 10
                self.canvas.coords(self.mouth, 152, 165 - (mouth_open/2), 168, 165 + (mouth_open/2))
                headset_bob = math.cos(rad) * 1.5
                self.canvas.move(self.earpiece_l, 0, headset_bob)
                self.canvas.move(self.earpiece_r, 0, headset_bob)
            else:
                self.canvas.coords(self.mouth, 152, 165, 168, 165)
                if self.anim_tick % 100 < 8:
                    self.canvas.coords(self.eye_left, 140, 118, 160, 118)
                    self.canvas.coords(self.eye_right, 180, 118, 200, 118)
                    self.canvas.itemconfig(self.pupil_l, state=tk.HIDDEN)
                    self.canvas.itemconfig(self.pupil_r, state=tk.HIDDEN)
                else:
                    self.canvas.coords(self.eye_left, 140, 115, 160, 118)
                    self.canvas.coords(self.eye_right, 180, 118, 200, 115)
                    self.canvas.itemconfig(self.pupil_l, state=tk.NORMAL)
                    self.canvas.itemconfig(self.pupil_r, state=tk.NORMAL)
                    
            self.root.after(33, self.refresh_avatar_animation)
        except Exception:
            pass

    def update_status(self, text, state="idle"):
        self.current_state = state
        self.status_label.config(text=f"STATUS: {text.upper()}")
        if state == "listening":
            self.status_label.config(fg="#00ffcc")
            self.title_label.config(text="CAPTURE MODE ENGAGED // AUDIO INBOUND", fg="#00ffcc")
            self.canvas.itemconfig(self.face_base, outline="#00ffcc")
        elif state == "speaking":
            self.status_label.config(fg="#ff0066")
            self.title_label.config(text="NEURAL SYNCHRONIZER BROADCASTING // ONLINE", fg="#ff0066")
            self.canvas.itemconfig(self.face_base, outline="#ff0066")
        else:
            self.status_label.config(fg="#00a8ff")
            self.title_label.config(text="MAIN SYSTEM STATUS // SECURE", fg="#00f0ff")
            self.canvas.itemconfig(self.face_base, outline="#00f0ff")

    def append_log(self, sender, text):
        self.log_queue.put((sender, text))

    def process_incoming_queue_logs(self):
        try:
            while not self.log_queue.empty():
                sender, text = self.log_queue.get_nowait()
                self.dialog_box.config(state=tk.NORMAL)
                self.dialog_box.insert(tk.END, f" [{sender.upper()}]: {text}\n")
                self.dialog_box.see(tk.END)
                self.dialog_box.config(state=tk.DISABLED)
        except Exception:
            pass
        self.root.after(100, self.process_incoming_queue_logs)
