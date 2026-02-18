# SoundCloud Downloader

A simple desktop application to download songs from SoundCloud.

## How to use

1. Go to the `dist` folder.
2. Run `SoundCloudDownloader.exe`.
3. Paste a SoundCloud URL.
4. Select a download folder.
5. Click "Download".

## Requirements

- **FFmpeg**: limit
  - **GOOD NEWS**: FFmpeg is now **bundled** with the application! You do not need to install it separately.
  - The application uses the embedded `ffmpeg.exe` and `ffprobe.exe` automatically.

## Troubleshooting

- If the download fails immediately, check if the URL is valid.
- If it converts but fails to save, check permissions or FFmpeg installation.
