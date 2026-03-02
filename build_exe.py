import PyInstaller.__main__
import customtkinter
import os
import sys

# Get customtkinter path
ctk_path = os.path.dirname(customtkinter.__file__)

# Use appropriate path separator for --add-data based on OS
sep = ';' if sys.platform == 'win32' else ':'

args = [
    'main.py',
    '--name=SoundCloudDownloader',
    '--onefile',
    '--noconsole',
    f'--add-data={ctk_path}{sep}customtkinter/',
    '--clean',
    '--noconfirm',
    f'--add-data=logo.png{sep}.',
    f'--add-data=logo2.png{sep}.',
    f'--add-data=fl.png{sep}.',
    f'--add-data=sc(1).png{sep}.',
]

if sys.platform == 'win32':
    args.extend([
        '--icon=logo.ico',
        f'--add-data=logo.ico{sep}.',
    ])
    if os.path.exists('dist/ffmpeg.exe'):
        args.append(f'--add-data=dist/ffmpeg.exe{sep}.')
    if os.path.exists('dist/ffprobe.exe'):
        args.append(f'--add-data=dist/ffprobe.exe{sep}.')

PyInstaller.__main__.run(args)
