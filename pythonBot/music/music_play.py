from pythonBot.music.music_info import *
from pythonBot.music.youtube_api import search_youtube
import math


def endSong(guild, path):
    os.remove(path)


@bot.command(pass_context=True)
async def play(ctx, *, url=None):
    if url is None:
        await ctx.send('노래 제목 혹은 유튜브 url을 달아주세요!')
        return

    if not ctx.message.author.voice:
        await ctx.send('노래 재생을 위해서는 음성 채널에 입장해 주세요!')
        return

    else:
        channel = ctx.message.author.voice.channel
    voice_client = await channel.connect()

    guild = ctx.message.guild

    if 'https' not in url:
        url = search_youtube(url)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=True)
        path = str(file['title']) + "-" + str(file['id'] + ".mp3")
    voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
    voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)

    song_embed = discord.Embed(title=':headphones:노래가 추가되었습니다.', color=0xfcffab)
    song_embed.add_field(name='노래 제목:', inline=False, value=file['title'])
    song_embed.add_field(name='곡 길이:', inline=False, value=str(math.floor(file['duration']/60))+":"+str(file['duration']%60))
    song_embed.add_field(name='링크', inline=False, value=url)

    await ctx.send(embed=song_embed)

    while voice_client.is_playing():
        await asyncio.sleep(1)
    else:
        await voice_client.disconnect()
        print("Disconnected")