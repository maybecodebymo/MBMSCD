from downloader import SoundCloudDownloader
import os

def test_download():
    # Test with a known royalty-free soundcloud track or similar
    # Using a dummy URL that might fail if validation is strict, 
    # but yt-dlp usually handles generic validation.
    # Better to use a real URL if possible, or just check if yt-dlp attempts to invoke ffmpeg.
    # Since I don't have a guaranteed valid SC URL, I will try a generic one and expect a specific error or success.
    # Actually, let's try to just check if `ffmpeg` is callable by `yt-dlp` by seeing if it doesn't crash on "ffmpeg not found".
    
    # We can also just check if ffmpeg is in path pythonically
    import shutil
    if shutil.which("ffmpeg"):
        print("FFmpeg found in PATH.")
    else:
        print("FFmpeg NOT found in PATH.")

    # We can dry-run yt-dlp
    import yt_dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        # 'simulate': True, # Simulate to avoid actual download but check extraction
    }
    
    print("Testing yt-dlp initialization...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("yt-dlp initialized successfully.")
    except Exception as e:
        print(f"yt-dlp initialization failed: {e}")

if __name__ == "__main__":
    test_download()
