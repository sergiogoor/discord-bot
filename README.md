# 🎵 Discord Music Bot

A simple Discord bot that plays music from YouTube, using `yt-dlp` to download audio and `discord.py` to manage playback.

## 🚀 Features
- ✅ **Search and play music** from YouTube
- 📥 **Download and store** audio files for playback
- 🔄 **Queue system** to manage multiple songs
- ⏭ **Skip songs** with a simple command
- 🎵 **Auto-disconnect** when the queue is empty

## 📌 Requirements
Before running the bot, ensure you have the following installed:

- **Python 3.8+**
- **FFmpeg** (must be in the project folder)
- **yt-dlp** (YouTube downloader)
- **discord.py** (Discord bot framework)

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/discord-music-bot.git
   cd discord-music-bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your bot token:
   ```
   DISCORD_TOKEN=your-bot-token-here
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

## 🎮 Commands
| Command      | Description |
|-------------|-------------|
| `!play <song name or URL>` | Search and play a song |
| `!s` | Skip the current song |

## 🔧 Configuration
Ensure you have `ffmpeg.exe` and `yt-dlp.exe` in the project directory for the bot to function correctly.

## 📜 License
This project is licensed under the **MIT License**. Feel free to modify and improve it!

---
### 🌟 Enjoy your music! 🎶

