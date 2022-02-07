# BaseRequirements
import discord
from discord.ext import commands, tasks
import re
import asyncio

# Hide Token
import os

token = open("token", "r").readline()

# Discord Default Value
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = "!", intents=intents)

@bot.event
async def on_ready():
    print(bot.user.id)
    
@bot.event
async def on_member_join(member):
    await bot.get_channel(939857307297251349).send(f"{member.mention}\n\n"
                                                   f"종합게임동아리에 온 걸 환영해요!\n"
                                                   f"우선, 입부신청을 위해 신청서를 써줘야 해요.\n"
                                                   f"아래 양식에 맞춰 당신의 정보를 입력해주세요.\n\n"
                                                   f"양식 : 이름(닉네임) 생년(비공가능) 성별(비공가능)\n\n"
                                                   f"예시 : 김춘삼 1397 남자\n"
                                                   f"`※주의※ 이름, 생년, 성별은 서로 띄어쓰기를 해주어야 합니다.`\n"
                                                   f"`※주의※ 꼭 생년은 태어난 년도를 입력해야 합니다.`")

@bot.event
async def on_message(message):
    if message.author.bot:
        return None
    
    if str(message.channel) == "입부신청":
        try:
            name = message.content.split(" ")[0]
            age = message.content.split(" ")[1]
            sex = message.content.split(" ")[2]
            name = str(name)    # 맞는 형식인지 체크..
            try:
                age = int(age)
            except:
                age = "비공"
            sex = str(sex)
            
            p = re.compile('남|여|비공')     # 성별 찾기
            sex = p.match(sex)
            if sex.group() == "남":
                d_sex = "남성"
                sex = "남성"
            elif sex.group() == "여":
                d_sex = "여성"
                sex = "여성"
            else:
                d_sex = "비공"
                sex = "성별비공개"
            
            member = discord.utils.get(message.guild.roles, name="동아리원")
            
            if age == "비공":
                year = discord.utils.get(message.guild.roles, name="나이비공개")
                age = "비공개"
                await message.author.add_roles(year)
            else:
                try:
                    year = discord.utils.get(message.guild.roles, name=str(age)[2:4] + "년생")
                    await message.author.add_roles(year)
                    age = str(age)[2:4] + "년생"
                except:
                    await message.guild.create_role(name=str(age)[2:4] + "년생")
                    year = discord.utils.get(message.guild.roles, name=str(age)[2:4] + "년생")
                    await message.author.add_roles(year)
                    age = str(age)[2:4] + "년생"
            sex = discord.utils.get(message.guild.roles, name=sex)
            
            await message.author.edit(nick=name)
            await message.author.add_roles(member, reason="입부")
            await message.author.add_roles(sex)
            await message.delete()
            await message.channel.purge(limit=1)
            await bot.get_channel(939857159041192049).send(f"{message.author.mention}님이 종겜동에 가입했어요! 환영해주세요!")
            await bot.get_channel(939865596319924244).send(f"**[입부 신청서]**\n{message.author.display_name} / `{message.author.id}` / `{age}` / `{d_sex}`")
        except:
            await message.delete()
            erm = await message.channel.send(f"{message.author.mention} 뭔가 잘못된 양식이에요.")
            await asyncio.sleep(3)
            await erm.delete()
    else:
        await bot.process_commands(message)

@bot.command()
async def 테스트(ctx):
    await ctx.send("켜져있어.")

bot.run(token)