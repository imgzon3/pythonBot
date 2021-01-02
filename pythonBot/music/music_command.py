from pythonBot.music.music_info import *
from pythonBot.music.youtube_api import search_youtube
import math


# 저장된 노래 지우는 함수
def endSong(guild, path):
    os.remove(path)


# 노래 리스트 저장
queue_list = []
status_list = [0]  # 재생중이면 1, 아니라면 0


# play 명령어 첫 시작 후 노래 등록 전에 play사용 시 오류 발생, 해결 필요
@bot.command(pass_context=True)
async def play(ctx, *, url=None):
    # 입력 값이 없을 경우
    if url is None:
        await ctx.send(':headphones:노래 제목 혹은 유튜브 url을 달아주세요!')
        return

    # 사용자가 음성 채널에 접속하지 않았을 경우
    if not ctx.message.author.voice:
        await ctx.send(':headphones:노래 재생을 위해서는 음성 채널에 입장해 주세요!')
        return

    else:
        channel = ctx.message.author.voice.channel

    # 단어 검색인 경우 api 활용 검색
    if 'https' not in url:
        url = search_youtube(url)
        # 검색 결과가 없는 경우
        if url == '':
            await ctx.send(':headphones:검색결과가 없습니다.')
            return

    # 현재 노래가 재생되고 있지 않다면, 음성채널 접속
    if status_list[0] == 0:
        voice_channel = await channel.connect()
        guild = ctx.message.guild
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    await ctx.send(':headphones:노래가 등록되었습니다. 잠시만 기다려 주세요.')

    # 유튜브 영상 다운, 음원 추출
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=True)
        path = str(file['title']) + "-" + str(file['id'] + ".mp3")

    # 플레이리스트에 저장
    song_time = str(math.floor(file['duration'] / 60)) + ":"
    if file['duration'] % 60 < 10:
        song_time = song_time + '0' + str(file['duration'] % 60)
    else:
        song_time = song_time + str(file['duration'] % 60)
    tmp_list = [path, file['title'], song_time]
    queue_list.append(tmp_list)
    print(queue_list)

    # 노래가 재생되고 있지 않은 상태면, 새로 노래 시작
    if status_list[0] == 0:
        # voice_channel.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
        # voice_channel.source = discord.PCMVolumeTransformer(voice_channel.source, 1)
        try:
            voice.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
            voice.source = discord.PCMVolumeTransformer(voice.source, 1)
        except FileNotFoundError as file_no:
            await ctx.send(':headphones:오류가 발생했습니다.')
            queue_list.pop()
            return

    if status_list[0] == 0:
        status_list.pop()
        status_list.append(1)

    # 노래 추가 결과 알림
    song_embed = discord.Embed(title=':headphones:노래가 추가되었습니다.', color=0xfcffab)
    song_embed.add_field(name='노래 제목:', inline=False, value=file['title'])
    if len(queue_list) is 1:
        queue_txt = '현재 재생 중'
    else:
        queue_txt = len(queue_list) - 1
    song_embed.add_field(name='순서', inline=False, value=queue_txt)
    song_embed.add_field(name='곡 길이:', inline=False, value=song_time)
    song_embed.add_field(name='링크', inline=False, value=url)
    await ctx.send(embed=song_embed)

    # 노래가 재생되고 있지 않다면 접속 종료, queue_list 남아있을 경우 계속
    while True:
        while voice.is_playing():
            await asyncio.sleep(1)
        else:
            if status_list[0] is 1:
                queue_list.pop(0)
                if len(queue_list) != 0:
                    # await ctx.send(':headphones: 이어서 ['+queue_list[0][2]+']'+queue_list[1]+'이(가) 재생됩니다.')
                    print(queue_list)
                    voice.play(discord.FFmpegPCMAudio(queue_list[0][0]),
                               after=lambda x: endSong(guild, queue_list[0][0]))
                    voice.source = discord.PCMVolumeTransformer(voice.source, 1)
                else:
                    status_list.pop()
                    status_list.append(0)
                    await ctx.voice_client.disconnect()
                    print("Disconnected")
                    break
            elif status_list[0] is 0:
                print('Disconnected by other')
                break


@bot.command(pass_context=True)
async def p(ctx, *, url=None):
    # 입력 값이 없을 경우
    if url is None:
        await ctx.send(':headphones:노래 제목 혹은 유튜브 url을 달아주세요!')
        return

    # 사용자가 음성 채널에 접속하지 않았을 경우
    if not ctx.message.author.voice:
        await ctx.send(':headphones:노래 재생을 위해서는 음성 채널에 입장해 주세요!')
        return

    else:
        channel = ctx.message.author.voice.channel

    # 단어 검색인 경우 api 활용 검색
    if 'https' not in url:
        url = search_youtube(url)
        # 검색 결과가 없는 경우
        if url == '':
            await ctx.send(':headphones:검색결과가 없습니다.')
            return

    # 현재 노래가 재생되고 있지 않다면, 음성채널 접속
    if status_list[0] == 0:
        voice_channel = await channel.connect()
        guild = ctx.message.guild
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    await ctx.send(':headphones:노래가 등록되었습니다. 잠시만 기다려 주세요.')

    # 유튜브 영상 다운, 음원 추출
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=True)
        path = str(file['title']) + "-" + str(file['id'] + ".mp3")

    # 플레이리스트에 저장
    song_time = str(math.floor(file['duration'] / 60)) + ":"
    if file['duration'] % 60 < 10:
        song_time = song_time + '0' + str(file['duration'] % 60)
    else:
        song_time = song_time + str(file['duration'] % 60)
    tmp_list = [path, file['title'], song_time]
    queue_list.append(tmp_list)
    print(queue_list)

    # 노래가 재생되고 있지 않은 상태면, 새로 노래 시작
    if status_list[0] == 0:
        # voice_channel.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
        # voice_channel.source = discord.PCMVolumeTransformer(voice_channel.source, 1)
        try:
            voice.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
            voice.source = discord.PCMVolumeTransformer(voice.source, 1)
        except FileNotFoundError as file_no:
            await ctx.send(':headphones:오류가 발생했습니다.')
            queue_list.pop()
            return

    if status_list[0] == 0:
        status_list.pop()
        status_list.append(1)

    # 노래 추가 결과 알림
    song_embed = discord.Embed(title=':headphones:노래가 추가되었습니다.', color=0xfcffab)
    song_embed.add_field(name='노래 제목:', inline=False, value=file['title'])
    if len(queue_list) is 1:
        queue_txt = '현재 재생 중'
    else:
        queue_txt = len(queue_list) - 1
    song_embed.add_field(name='순서', inline=False, value=queue_txt)
    song_embed.add_field(name='곡 길이:', inline=False, value=song_time)
    song_embed.add_field(name='링크', inline=False, value=url)
    await ctx.send(embed=song_embed)

    # 노래가 재생되고 있지 않다면 접속 종료, queue_list 남아있을 경우 계속
    while True:
        while voice.is_playing():
            await asyncio.sleep(1)
        else:
            if status_list[0] is 1:
                queue_list.pop(0)
                if len(queue_list) != 0:
                    # await ctx.send(':headphones: 이어서 ['+queue_list[0][2]+']'+queue_list[1]+'이(가) 재생됩니다.')
                    print(queue_list)
                    voice.play(discord.FFmpegPCMAudio(queue_list[0][0]),
                               after=lambda x: endSong(guild, queue_list[0][0]))
                    voice.source = discord.PCMVolumeTransformer(voice.source, 1)
                else:
                    status_list.pop()
                    status_list.append(0)
                    await ctx.voice_client.disconnect()
                    print("Disconnected")
                    break
            elif status_list[0] is 0:
                print('Disconnected by other')
                break


@bot.command(pass_context=True)
async def skip(ctx):
    # 사용자가 음성 채널에 접속하지 않았을 경우
    if not ctx.message.author.voice:
        await ctx.send(':headphones:음성 채널에 입장해 주세요!')
        return

    # 노래 재생 중인 상태가 아닌 경우
    elif len(queue_list) is 0:
        await ctx.send(':headphones:노래가 재생되고 있지 않습니다.')
        return

    # 노래 재생 중인 경우
    elif len(queue_list) > 0:
        # 다음 노래가 있을 경우
        if len(queue_list) > 1:
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            voice.stop()
            await ctx.send(':headphones:다음 노래로 스킵합니다.')
            print('skip')
            return
        # 다음 노래가 없을 경우
        else:
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            status_list.pop()
            status_list.append(0)
            queue_list.clear()
            voice.stop()
            await ctx.voice_client.disconnect()
            await ctx.send(':headphones:다음 노래가 없어 봇이 종료됩니다.')
            print("Disconnected")
            return


@bot.command(pass_context=True)
async def 넘기기(ctx):
    # 사용자가 음성 채널에 접속하지 않았을 경우
    if not ctx.message.author.voice:
        await ctx.send(':headphones:음성 채널에 입장해 주세요!')
        return

    # 노래 재생 중인 상태가 아닌 경우
    elif len(queue_list) is 0:
        await ctx.send(':headphones:노래가 재생되고 있지 않습니다.')
        return

    # 노래 재생 중인 경우
    elif len(queue_list) > 0:
        # 다음 노래가 있을 경우
        if len(queue_list) > 1:
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            voice.stop()
            await ctx.send(':headphones:다음 노래로 스킵합니다.')
            print('skip')
            return
        # 다음 노래가 없을 경우
        else:
            voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
            status_list.pop()
            status_list.append(0)
            queue_list.clear()
            voice.stop()
            await ctx.voice_client.disconnect()
            await ctx.send(':headphones:다음 노래가 없어 봇이 종료됩니다.')
            print("Disconnected")
            return


@bot.command(pass_context=True)
async def stop(ctx):
    # 사용자가 음성 채널에 접속하지 않았을 경우
    if not ctx.message.author.voice:
        await ctx.send(':headphones:음성 채널에 입장해 주세요!')
        return

    # 노래 재생 중인 상태가 아닌 경우
    elif len(queue_list) is 0:
        await ctx.send(':headphones:노래가 재생되고 있지 않습니다.')
        return

    # 노래 재생 중인 경우
    else:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if len(queue_list) != 1:
            for i in range(1, len(queue_list)):
                # 대기열의 노래 삭제
                endSong(queue_list[i][0])
        queue_list.clear()
        status_list.pop()
        status_list.append(0)
        voice.stop()
        await ctx.voice_client.disconnect()
        print("Disconnected")
        await ctx.send(':headphones:플레이리스트 제거 후 봇이 종료됩니다.')


@bot.command(pass_context=True)
async def 정지(ctx):
    # 사용자가 음성 채널에 접속하지 않았을 경우
    if not ctx.message.author.voice:
        await ctx.send(':headphones:음성 채널에 입장해 주세요!')
        return

    # 노래 재생 중인 상태가 아닌 경우
    elif len(queue_list) is 0:
        await ctx.send(':headphones:노래가 재생되고 있지 않습니다.')
        return

    # 노래 재생 중인 경우
    else:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if len(queue_list) != 1:
            for i in range(1, len(queue_list)):
                # 대기열의 노래 삭제
                endSong(queue_list[i][0])
        queue_list.clear()
        status_list.pop()
        status_list.append(0)
        voice.stop()
        await ctx.voice_client.disconnect()
        print("Disconnected")
        await ctx.send(':headphones:플레이리스트 제거 후 봇이 종료됩니다.')


@bot.command(pass_context=True)
async def queue(ctx):
    # 노래 재생 중인 상태가 아닌 경우
    if len(queue_list) is 0:
        await ctx.send(':headphones:현재 재생중인 노래가 없습니다!')

    # 노래 재생 중인 경우
    else:
        queue_txt = discord.Embed(title=':headphones:재생목록', color=0xfcffab)
        queue_txt.add_field(name='현재 재생 중', inline=False, value='[' + queue_list[0][2] + '] ' + queue_list[0][1])

        # 대기 목록이 없는 경우
        if len(queue_list) is 1:
            queue_txt.add_field(name='대기 목록', inline=False, value='대기 목록이 없습니다!')

        # 대기 목록이 있는 경우
        elif len(queue_list) > 1:
            queue_tmp = ''
            for i in range(1, len(queue_list)):
                queue_tmp = queue_tmp + str(i) + '. [' + queue_list[i][2] + '] ' + str(queue_list[i][1]) + '\n'
            queue_txt.add_field(name='대기 목록', inline=False, value=queue_tmp)
        await ctx.send(embed=queue_txt)


@bot.command(pass_context=True)
async def 대기열(ctx):
    # 노래 재생 중인 상태가 아닌 경우
    if len(queue_list) is 0:
        await ctx.send(':headphones:현재 재생중인 노래가 없습니다!')

    # 노래 재생 중인 경우
    else:
        queue_txt = discord.Embed(title=':headphones:재생목록', color=0xfcffab)
        queue_txt.add_field(name='현재 재생 중', inline=False, value='[' + queue_list[0][2] + '] ' + queue_list[0][1])

        # 대기 목록이 없는 경우
        if len(queue_list) is 1:
            queue_txt.add_field(name='대기 목록', inline=False, value='대기 목록이 없습니다!')

        # 대기 목록이 있는 경우
        elif len(queue_list) > 1:
            queue_tmp = ''
            for i in range(1, len(queue_list)):
                queue_tmp = queue_tmp + str(i) + '. [' + queue_list[i][2] + '] ' + str(queue_list[i][1]) + '\n'
            queue_txt.add_field(name='대기 목록', inline=False, value=queue_tmp)
        await ctx.send(embed=queue_txt)


@bot.command(pass_context=True)
async def now(ctx):
    # 사용자가 음성 채널에 접속하지 않았을 경우
    if not ctx.message.author.voice:
        await ctx.send(':headphones:음성 채널에 입장해 주세요!')
        return

    # 노래 재생 중인 상태가 아닌 경우
    elif len(queue_list) is 0:
        await ctx.send(':headphones:현재 재생중인 노래가 없습니다!')
        return

    # 노래 재생 중인 경우
    else:
        now_txt = discord.Embed(title=':headphones:현재 재생중인 노래', color=0xfcffab)
        now_txt.add_field(name='노래 제목:', inline=False, value=queue_list[0][1])
        now_txt.add_field(name='곡 길이:', inline=False, value=queue_list[0][2])
        await ctx.send(embed=now_txt)


@bot.command(pass_context=True)
async def 현재(ctx):
    # 사용자가 음성 채널에 접속하지 않았을 경우
    if not ctx.message.author.voice:
        await ctx.send(':headphones:음성 채널에 입장해 주세요!')
        return

    # 노래 재생 중인 상태가 아닌 경우
    elif len(queue_list) is 0:
        await ctx.send(':headphones:현재 재생중인 노래가 없습니다!')
        return

    # 노래 재생 중인 경우
    else:
        now_txt = discord.Embed(title=':headphones:현재 재생중인 노래', color=0xfcffab)
        now_txt.add_field(name='노래 제목:', inline=False, value=queue_list[0][1])
        now_txt.add_field(name='곡 길이:', inline=False, value=queue_list[0][2])
        await ctx.send(embed=now_txt)


@bot.command(pass_context=True)
async def remove(ctx, *, index=None):
    # 노래 재생 중인 상태가 아닌 경우
    if len(queue_list) is 0:
        await ctx.send(':headphones:현재 재생중인 노래가 없습니다!')
        return

    # 대기 목록이 없을 경우
    elif len(queue_list) is 1:
        await ctx.send(':headphones:현재 대기 목록이 없습니다!')
        return

    # 대기 목록이 있는 경우
    else:
        # all 입력 시
        if index is 'all':
            for i in range(1, len(queue_list)):
                # 대기열의 노래 삭제
                endSong(queue_list[i][0])
                queue_list.pop(1)
            await ctx.send(':headphones:모든 대기 목록을 삭제했습니다.')
            return

        # 전부 입력 시
        elif index is '전부':
            for i in range(1, len(queue_list)):
                # 대기열의 노래 삭제
                endSong(queue_list[i][0])
                queue_list.pop(1)
            await ctx.send(':headphones:모든 대기 목록을 삭제했습니다.')
            return

        # 삭제할 숫자 입력 시
        elif 1 <= index <= len(queue_list):
            await ctx.send(':headphones:'+str(index)+'번 째 노래 '+queue_list[index][1]+'을 삭제합니다.')
            endSong(queue_list[index][0])
            queue_list.pop(index)
            return

        # 재생목록 이외의 숫자 입력 시
        elif index < 1 or index > len(queue_list):
            await ctx.send(':headphones:현재 대기중인 곡은 '+str(len(queue_list)-1)+'개 입니다.')

        # 다른 것, null일 시
        else:
            await ctx.send(':headphones:지우실 대기 목록을 선택해주세요!\n'
                           'remove [전부/all/위치]로 지정할 수 있습니다.\n'
                           '현재 대기중인 곡: '+str(len(queue_list)-1)+'개')
            return


@bot.command(pass_context=True)
async def 삭제(ctx, *, index=None):
    # 노래 재생 중인 상태가 아닌 경우
    if len(queue_list) is 0:
        await ctx.send(':headphones:현재 재생중인 노래가 없습니다!')
        return

    # 대기 목록이 없을 경우
    elif len(queue_list) is 1:
        await ctx.send(':headphones:현재 대기 목록이 없습니다!')
        return

    # 대기 목록이 있는 경우
    else:
        # all 입력 시
        if index is 'all':
            for i in range(1, len(queue_list)):
                # 대기열의 노래 삭제
                endSong(queue_list[i][0])
                queue_list.pop(1)
            await ctx.send(':headphones:모든 대기 목록을 삭제했습니다.')
            return

        # 전부 입력 시
        elif index is '전부':
            for i in range(1, len(queue_list)):
                # 대기열의 노래 삭제
                endSong(queue_list[i][0])
                queue_list.pop(1)
            await ctx.send(':headphones:모든 대기 목록을 삭제했습니다.')
            return

        # 삭제할 숫자 입력 시
        elif 1 <= index <= len(queue_list):
            await ctx.send(':headphones:'+str(index)+'번 째 노래 '+queue_list[index][1]+'을 삭제합니다.')
            endSong(queue_list[index][0])
            queue_list.pop(index)
            return

        # 재생목록 이외의 숫자 입력 시
        elif index < 1 or index > len(queue_list):
            await ctx.send(':headphones:현재 대기중인 곡은 '+str(len(queue_list)-1)+'개 입니다.')

        # 다른 것, null일 시
        else:
            await ctx.send(':headphones:지우실 대기 목록을 선택해주세요!\n'
                           'remove [전부/all/위치]로 지정할 수 있습니다.\n'
                           '현재 대기중인 곡: '+str(len(queue_list)-1)+'개')
            return

