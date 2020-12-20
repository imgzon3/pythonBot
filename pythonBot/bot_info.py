import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='//')  # 명령어 접두사는 ;으로 지정
bot.remove_command('help')  # 기본 명령어 help 미리 제거

# 토큰 값 가져오기
f = open("../../../privateStuff/bot_token.txt", 'r')

lines = f.readlines()
token = lines[0]

f.close()
