import discord
from discord.ext import commands
from dotenv import load_dotenv
import subprocess
from youtubesearchpython import VideosSearch
import os
import asyncio
import re

queue = []
playing = False

def clean_name(name):
    return re.sub(r'[<>:"/\\|?*]', '', name)

def get_title(url):
    command = [
        "yt-dlp.exe",
        "--get-title",
        url
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Title obtained: {result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing yt-dlp: {e}")
        return None

def search_video(query):
    print(f"Searching video for: {query}")
    search = VideosSearch(query, limit=1)
    results = search.result()
    if 'result' in results and results['result']:
        video = results['result'][0]
        return video['title'], video['link']
        print(f"Video found: {video['title']} ({video['link']})")
    else:
        print("No results found for the search.")
    return None, None

def download_youtube(url, title):
    title = clean_name(title)
    download_folder = "music"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    file_path = os.path.join(download_folder, f"{title}.opus")
    if not os.path.exists(file_path):
        command = [
            "yt-dlp.exe",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-quality", "0",
            "--ffmpeg-location", os.path.join(os.getcwd(), "ffmpeg.exe"),
            "-o", os.path.join(download_folder, f"{title}"),
            url
        ]
        try:
            subprocess.run(command, check=True)
            print(f"Download completed: {os.path.join(download_folder, f"{title}.opus")}")
        except subprocess.CalledProcessError as e:
            print(f"Download error: {e}")

    return file_path

async def play_music(ctx, file):
    global queue, voice_channel, playing
    FFMPEG_PATH = os.path.join(os.getcwd(), "ffmpeg.exe")
    print(FFMPEG_PATH)
    count = 0

    while True:
        if not ctx.voice_client:
            if ctx.author.voice:
                embed = discord.Embed(
                    title="✅ Connected to Voice Channel",
                    description=f"Successfully connected to **{ctx.author.voice.channel.name}**!",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
                voice_channel = await ctx.author.voice.channel.connect()
            else:
                embed = discord.Embed(
                    title="❌ Voice Channel Error",
                    description="You must be in a voice channel to use this command.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
        else:
            voice_channel = ctx.voice_client

        if queue:
            file = queue[0]
            count = 0
            try:
                song_title = os.path.basename(file).replace(".opus", "")
                embed = discord.Embed(
                    title="🎵 Now Playing",
                    description=f"**{song_title}**",
                    color=discord.Color.blue()
                )
                embed.set_footer(text="Enjoy the music!")
                await ctx.send(embed=embed)

                voice_channel.play(discord.FFmpegOpusAudio(file, executable=FFMPEG_PATH))
                while voice_channel.is_playing():
                    await asyncio.sleep(1)
                queue.pop(0)

            except Exception as e:
                embed = discord.Embed(
                    title="❌ Playback Error",
                    description=f"```{e}```",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                await voice_channel.disconnect()
        else:
            await asyncio.sleep(1)
            count += 1
            print(count)
            if count > 300:
                playing = False
                embed = discord.Embed(
                    title="🎉 Playlist Finished",
                    description="Long live the republic!",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)
                await voice_channel.disconnect()
                break

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"✅ Bot ready as {bot.user}")

@bot.command(name="s")
async def skip(ctx):
    global voice_channel
    embed = discord.Embed(
        title="⏭ Song Skipped",
        description="Preparing next track...",
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)
    voice_channel.stop()

@bot.command(name="play")
async def play(ctx, *, input: str):
    global playing, queue
    if "https" in input:
        url = input
        title = get_title(url)
    else:
        title, url = search_video(input)

    if url and title:
        file = download_youtube(url, title)
        queue.append(file)

        embed = discord.Embed(
            title="📥 Song Added",
            description=f"[{title}]({url})",
            color=discord.Color.green()
        )
        embed.add_field(name="Queue Position", value=f"#{len(queue)}")
        await ctx.send(embed=embed)

        if not playing:
            playing = True
            await play_music(ctx, file)
    else:
        embed = discord.Embed(
            title="🔍 No Results Found",
            description="Try another search term.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

bot.run(TOKEN)
