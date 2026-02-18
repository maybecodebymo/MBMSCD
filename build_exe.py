import PyInstaller.__main__
import customtkinter
import os

# Get customtkinter path
ctk_path = os.path.dirname(customtkinter.__file__)

PyInstaller.__main__.run([
    'main.py',
    '--name=SoundCloudDownloader',
    '--onefile',
    '--noconsole',
    f'--add-data={ctk_path};customtkinter/',
    '--clean',
    '--noconfirm',
    '--icon=logo.ico',
    '--add-data=logo.png;.',
    '--add-data=logo.ico;.',
    '--add-data=logo2.png;.',

    '--add-data=fl.png;.',
    '--add-data=sc(1).png;.',
    # Add FFmpeg binaries (assuming they are in dist/ folder)
    '--add-data=dist/ffmpeg.exe;.',
    '--add-data=dist/ffprobe.exe;.',
])
