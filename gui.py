import customtkinter as ctk
import threading
from tkinter import filedialog
from downloader import SoundCloudDownloader
import os
import time
import sys
import random

ctk.set_appearance_mode("Light") 
ctk.set_default_color_theme("dark-blue") 

class ProgressButton(ctk.CTkFrame):
    def __init__(self, master, width=200, height=50, 
                 text="BUTTON", font=None,
                 fg_color="#333333", hover_color="#555555", 
                 progress_color="#4ECDC4", 
                 text_color="white", text_color_loading="black",
                 text_color_hover="black",
                 command=None, **kwargs):
        
        super().__init__(master, width=width, height=height, fg_color=fg_color, **kwargs)
        
        self.command = command
        self.height = height
        self.width = width
        self.text_color_idle = text_color
        self.text_color_loading = text_color_loading
        self.text_color_hover = text_color_hover
        self.fg_color_idle = fg_color
        self.hover_color = hover_color
        self.progress_color = progress_color
        
        self.grid_propagate(False) 
        
        self.progress_bar = ctk.CTkFrame(self, width=0, height=height, 
                                         fg_color=progress_color, corner_radius=kwargs.get('corner_radius', 0))
        self.progress_bar.place(x=0, y=0)
        
        self.label = ctk.CTkLabel(self, text=text, font=font, text_color=text_color, fg_color="transparent")
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.bind("<Button-1>", self.on_click)
        self.label.bind("<Button-1>", self.on_click)
        self.progress_bar.bind("<Button-1>", self.on_click)
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.label.bind("<Enter>", self.on_enter)
        self.label.bind("<Leave>", self.on_leave)
        
        self.state = "normal"
        self.current_progress = 0
        self.target_progress = 0
    
    def on_click(self, event=None):
        if self.state == "normal" and self.command:
            self.command()
            
    def on_enter(self, event=None):
        if self.state == "normal":
            self.configure(fg_color=self.hover_color)
            self.label.configure(text_color=self.text_color_hover)
            
    def on_leave(self, event=None):
        if self.state == "normal":
            self.configure(fg_color=self.fg_color_idle)
            self.label.configure(text_color=self.text_color_idle)

    def configure_button(self, text=None, fg_color=None, state=None, text_color=None):
        if text: self.label.configure(text=text)
        if fg_color: 
            super().configure(fg_color=fg_color)
            self.fg_color_idle = fg_color
        if state: self.state = state
        if text_color: 
            self.label.configure(text_color=text_color)
            self.text_color_idle = text_color 

    def set_progress(self, percentage):
        self.target_progress = max(0.0, min(1.0, percentage))
        self.animate_progress()

    def animate_progress(self):
        step = 0.01
        if abs(self.current_progress - self.target_progress) < step:
            self.current_progress = self.target_progress
        else:
            if self.current_progress < self.target_progress:
                self.current_progress += step
            else:
                self.current_progress -= step
            self.after(10, self.animate_progress)

        new_width = self.winfo_width() * self.current_progress
        self.progress_bar.configure(width=new_width)
        self.label.lift()

    def reset_progress(self):
        self.current_progress = 0
        self.target_progress = 0
        self.progress_bar.configure(width=0)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x600") 
        self.minsize(450, 400)  # Allow smaller windows
        self.title("Maybebeatsbymo's downloader")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header - fixed
        self.grid_rowconfigure(1, weight=1)  # Content - expands
        self.grid_rowconfigure(2, weight=0)  # Download button - fixed
        self.grid_rowconfigure(3, weight=0)  # Warning - fixed

        self.font_title = ("Impact", 36)
        self.font_body = ("Courier New", 14, "bold")
        self.font_label = ("Impact", 24)
        self.font_button = ("Courier New", 18, "bold")
        
        self.color_bg = "#FFD93D" 
        self.color_header_bg = "#FF6B6B" 
        self.color_content_bg = "#4ECDC4" 
        self.color_input_bg = "#F7F1E3" 
        self.color_btn_idle = "#1A1A1A" 
        self.color_btn_hover = "#FFFFFF" 
        self.color_accent_active = "#C4E538" 
        self.color_accent_done = "#FF9FF3" 
        self.color_border = "#000000"
        self.border_width = 4 
        self.corner_radius = 0

        self.configure(fg_color=self.color_bg)

        self.ffmpeg_path = self.check_ffmpeg()
        self.create_widgets()
        self.add_chaos_stickers()

    def check_ffmpeg(self):
        # 1. Check for bundled ffmpeg
        bundled_ffmpeg = self.resource_path("ffmpeg.exe")
        if os.path.exists(bundled_ffmpeg):
            return os.path.dirname(bundled_ffmpeg)
            
        # 2. Check system PATH
        import shutil
        if shutil.which("ffmpeg"):
            return None # detected in path, yt-dlp will find it

        # 3. Not found
        self.label_warning = ctk.CTkLabel(
            self, 
            text="[ WARNING: FFMPEG NOT FOUND ]", 
            text_color="red",
            fg_color="white",
            font=("Courier New", 12, "bold")
        )
        self.label_warning.grid(row=3, column=0, pady=5, sticky="ew")
        return None

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def create_widgets(self):
        # 1. Title / Logo Frame (Hot Pink)
        self.frame_header = ctk.CTkFrame(
            self, 
            fg_color=self.color_header_bg, 
            corner_radius=0,
            border_width=self.border_width,
            border_color=self.color_border
        )
        self.frame_header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        # Load Logo Image
        try:
            from PIL import Image
            img_path = self.resource_path("logo2.png")
            logo_img = ctk.CTkImage(light_image=Image.open(img_path), 
                                    dark_image=Image.open(img_path), 
                                    size=(300, 150)) 
            self.label_logo = ctk.CTkLabel(self.frame_header, text="", image=logo_img)
            self.label_logo.pack(pady=15)
            
            icon_path = self.resource_path("logo.ico")
            if os.path.exists(icon_path):
                 self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error loading logo: {e}")
            self.label_title = ctk.CTkLabel(
                self.frame_header, 
                text="MAYBEBEATSBYMO'S\nDOWNLOADER", 
                font=self.font_title, 
                text_color="black",
                justify="left"
            )
            self.label_title.pack(side="left", padx=10)

        # 2. Main Content Area (Cyan)
        self.frame_content = ctk.CTkFrame(
            self, 
            fg_color=self.color_content_bg, 
            border_width=self.border_width, 
            border_color=self.color_border, 
            corner_radius=self.corner_radius
        )
        self.frame_content.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.frame_content.grid_columnconfigure(0, weight=1)

        # URL Input
        self.label_url = ctk.CTkLabel(
            self.frame_content, 
            text="SOUNDCLOUD LINK:", 
            font=self.font_label,
            text_color="black",
            fg_color="transparent" 
        )
        self.label_url.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5)) 

        self.entry_url = ctk.CTkEntry(
            self.frame_content, 
            font=self.font_body,
            placeholder_text="https://soundcloud.com/...",
            fg_color=self.color_input_bg,
            text_color="black",
            border_width=self.border_width,
            border_color=self.color_border,
            corner_radius=self.corner_radius,
            height=45
        )
        self.entry_url.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 15))

        # Path Input
        self.label_path = ctk.CTkLabel(
            self.frame_content, 
            text="DESTINATION:", 
            font=self.font_label,
            text_color="black",
            fg_color="transparent"
        )
        self.label_path.grid(row=2, column=0, sticky="w", padx=20, pady=(0, 5))

        self.frame_path_inner = ctk.CTkFrame(self.frame_content, fg_color="transparent")
        self.frame_path_inner.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.frame_path_inner.grid_columnconfigure(0, weight=1)

        self.entry_path = ctk.CTkEntry(
            self.frame_path_inner, 
            font=self.font_body,
            fg_color=self.color_input_bg,
            text_color="black",
            border_width=self.border_width,
            border_color=self.color_border,
            corner_radius=self.corner_radius,
            height=45
        )
        self.entry_path.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entry_path.insert(0, os.getcwd())

        self.btn_browse = ctk.CTkButton(
            self.frame_path_inner, 
            text="BROWSE",
            font=self.font_body,
            fg_color="black",
            text_color="white",
            hover_color="#333333",
            border_width=0,
            corner_radius=self.corner_radius,
            width=120,
            height=45,
            command=self.browse_folder
        )
        self.btn_browse.grid(row=0, column=1)

        # 3. Action Area - Download Button (in its own row on the main window grid)
        self.btn_download = ProgressButton(
            self, 
            text="INITIATE DOWNLOAD", 
            font=("Impact", 24),
            fg_color=self.color_btn_idle,
            hover_color=self.color_btn_hover,
            progress_color=self.color_accent_active,
            text_color="white",
            text_color_loading="black",
            text_color_hover="black",
            corner_radius=self.corner_radius,
            border_width=self.border_width,
            border_color="white",
            height=70,
            command=self.start_download_thread
        )
        self.btn_download.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))

    def add_chaos_stickers(self):
        """ Place image-only decorations on the HEADER frame (sides of logo) """
        from PIL import Image
        
        self.sticker_refs = []
        
        # Place sc(1).png on the LEFT side of the logo, large
        try:
            sc_path = self.resource_path("sc(1).png")
            sc_img = Image.open(sc_path)
            sc_ctk = ctk.CTkImage(light_image=sc_img, dark_image=sc_img, size=(100, 100))
            self.sticker_refs.append(sc_ctk)
            sc_label = ctk.CTkLabel(self.frame_header, text="", image=sc_ctk, fg_color="transparent")
            sc_label.place(relx=0.03, rely=0.5, anchor="w")
        except Exception as e:
            print(f"Could not load sc(1).png: {e}")
        
        # Place fl.png on the RIGHT side of the logo, large
        try:
            fl_path = self.resource_path("fl.png")
            fl_img = Image.open(fl_path)
            fl_ctk = ctk.CTkImage(light_image=fl_img, dark_image=fl_img, size=(100, 100))
            self.sticker_refs.append(fl_ctk)
            fl_label = ctk.CTkLabel(self.frame_header, text="", image=fl_ctk, fg_color="transparent")
            fl_label.place(relx=0.97, rely=0.5, anchor="e")
        except Exception as e:
            print(f"Could not load fl.png: {e}")



    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, folder_selected)

    def start_download_thread(self):
        url = self.entry_url.get()
        path = self.entry_path.get()
        
        if not url:
            self.animate_button_error("NO URL PROVIDED")
            return
        
        if not path:
             self.animate_button_error("NO PATH SELECTED")
             return

        self.btn_download.configure_button(state="disabled", text="CONNECTING...", text_color="black", fg_color=self.color_btn_idle) 
        self.btn_download.set_progress(0.0)
        
        thread = threading.Thread(target=self.download_task, args=(url, path))
        thread.start()

    def download_task(self, url, path):
        downloader = SoundCloudDownloader(path, ffmpeg_path=self.ffmpeg_path)
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                try:
                    p_str = d.get('_percent_str', '0%').replace('%','')
                    p_val = float(p_str) / 100.0
                    self.after(0, lambda: self.btn_download.set_progress(p_val))
                    self.after(0, lambda: self.btn_download.configure_button(text=f"DOWNLOADING {p_str}%", text_color="black"))
                except:
                    pass
            elif d['status'] == 'finished':
                self.after(0, lambda: self.btn_download.configure_button(text="CONVERTING...", text_color="black"))

        success, message = downloader.download(url, progress_hook=progress_hook)
        self.after(0, lambda: self.finish_download(success, message))

    def finish_download(self, success, message):
        if success:
            self.btn_download.set_progress(1.0)
            self.btn_download.configure_button(
                state="normal", 
                fg_color=self.color_accent_done, 
                text="DONE! CLICK TO OPEN FOLDER",
                text_color="black",
            )
            self.btn_download.command = lambda: self.open_folder(self.entry_path.get())
            self.after(5000, self.reset_button)
        else:
            self.btn_download.set_progress(0)
            self.animate_button_error("FAILED")
            print(message) 

    def animate_button_error(self, error_text):
        self.btn_download.configure_button(text=error_text, fg_color="red", text_color="white")
        self.after(2000, self.reset_button)

    def reset_button(self):
        self.btn_download.configure_button(
            state="normal",
            text="INITIATE DOWNLOAD",
            fg_color=self.color_btn_idle,
            text_color="white"
        )
        self.btn_download.reset_progress()
        self.btn_download.command = self.start_download_thread

    def open_folder(self, path):
        try:
            os.startfile(path)
        except Exception:
            pass
        self.reset_button()

if __name__ == "__main__":
    app = App()
    app.mainloop()
