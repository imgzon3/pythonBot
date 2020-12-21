import os
import youtube_dl
import asyncio
from pythonBot.bot_info import *


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def endSong(guild, path):
    os.remove(path)


@bot.command(pass_context=True)
async def play(ctx, url):
    if not ctx.message.author.voice:
        await ctx.send('노래 재생을 위해서는 음성 채널에 입장해 주세요!')
        return

    else:
        channel = ctx.message.author.voice.channel

    voice_client = await channel.connect()

    guild = ctx.message.guild

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=True)
        path = str(file['title']) + "-" + str(file['id'] + ".mp3")

    voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

    await ctx.send(f'**Music: **{url}')

    while voice_client.is_playing():
        await asyncio.sleep(1)
    else:
        await voice_client.disconnect()
        print("Disconnected")