import yt_dlp
import os

class SoundCloudDownloader:
    def __init__(self, download_path, ffmpeg_path=None):
        self.download_path = download_path
        self.ffmpeg_path = ffmpeg_path

    def download(self, url, progress_hook=None):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'progress_hooks': [progress_hook] if progress_hook else [],
            'quiet': True,
            'no_warnings': True,
        }

        if self.ffmpeg_path:
            ydl_opts['ffmpeg_location'] = self.ffmpeg_path

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True, "Download complete!"
        except Exception as e:
            return False, str(e)
