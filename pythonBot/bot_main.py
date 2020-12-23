from pythonBot.bot_music import *
from pythonBot.bot_vote import *
from pythonBot.bot_weather import *


@bot.event  # 봇 로그인 상태 전환, 상태 메세지
async def on_ready():
    print('다음으로 로그인합니다: ', bot.user.name)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='//help로 도움말'))


@bot.command()  # 도움말
async def help(ctx):
    help_txt = discord.Embed(title=':headphones:장인이 봇 도움말', description='봇 도움말 목록입니다!', color=0xfcffab)
    help_txt.add_field(name='노래 명령어', inline=False,
                       value='//play [제목/url] - 노래를 재생합니다.  ("//p, //재생"명령어로도 가능)\n\n'
                             '//queue - 현재 대기열을 보여줍니다.  ("//대기열, //list"명령어로도 가능)\n\n'
                             '//remove [위치/all/전부] - 대기열에서 특정 순서의 노래를 제거하거나, 전부 제거합니다  '
                             '("//delete, //삭제"명령어로도 가능)\n\n'
                             '//skip - 현재 재생중인 노래를 건너뜁니다.  ("//넘기기"명령어로도 가능)\n\n'
                             '//pause - 현재 재생중인 노래를 일시중지합니다. 일시중지 상태인 경우 다시 재생합니다.  '
                             '("//일시정지"명령어로도 가능)\n\n'
                             '//volume [0-1000] - 볼륨의 크기를 조절합니다.  ("//볼륨"명령어로도 가능)\n\n'
                             '//stop - 현재 대기열을 포함한 모든 노래를 종료합니다.  ("//정지"명령어로도 가능)\n\n'
                             '//now - 현재 재생하고 있는 노래를 보여줍니다.  ("//current, //현재"명령어로도 가능)\n\n'
                             '//random - 노래 대기열의 순서를 랜덤화 합니다.  ("//랜덤"명령어로도 가능)')
    help_txt.add_field(name='날씨 명령어', inline=False,
                       value='업데이트 예정')
    help_txt.add_field(name='투표 명령어', inline=False,
                       value='업데이트 예정')

    await ctx.send(embed=help_txt)


@bot.command()  # 도움말
async def 도움(ctx):
    help_txt = discord.Embed(title=':headphones:장인이 봇 도움말', description='봇 도움말 목록입니다!', color=0xfcffab)
    help_txt.add_field(name='노래 명령어', inline=False,
                       value='//play [제목/url] - 노래를 재생합니다.  ("//p, //재생"명령어로도 가능)\n\n'
                             '//queue - 현재 대기열을 보여줍니다.  ("//대기열, //list"명령어로도 가능)\n\n'
                             '//remove [위치/all/전부] - 대기열에서 특정 순서의 노래를 제거하거나, 전부 제거합니다  '
                             '("//delete, //삭제"명령어로도 가능)\n\n'
                             '//skip - 현재 재생중인 노래를 건너뜁니다.  ("//넘기기"명령어로도 가능)\n\n'
                             '//pause - 현재 재생중인 노래를 일시중지합니다. 일시중지 상태인 경우 다시 재생합니다.  '
                             '("//일시정지"명령어로도 가능)\n\n'
                             '//volume [0-1000] - 볼륨의 크기를 조절합니다.  ("//볼륨"명령어로도 가능)\n\n'
                             '//stop - 현재 대기열을 포함한 모든 노래를 종료합니다.  ("//정지"명령어로도 가능)\n\n'
                             '//now - 현재 재생하고 있는 노래를 보여줍니다.  ("//current, //현재"명령어로도 가능)\n\n'
                             '//random - 노래 대기열의 순서를 랜덤화 합니다.  ("//랜덤"명령어로도 가능)')
    help_txt.add_field(name='날씨 명령어', inline=False,
                       value='업데이트 예정')
    help_txt.add_field(name='투표 명령어', inline=False,
                       value='업데이트 예정')

    await ctx.send(embed=help_txt)

bot.run(token)
