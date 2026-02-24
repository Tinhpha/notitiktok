import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")  # Railway dùng biến môi trường

intents = discord.Intents.default()
intents.message_content = True  # BẮT BUỘC
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập với tên {bot.user}")


# Lệnh testlive - chỉ admin dùng được
@bot.command()
@commands.has_permissions(administrator=True)
async def testlive(ctx):
    await ctx.send("🚀 Test thông báo LIVE thành công!")


# Nếu thiếu cái này thì command sẽ không chạy
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)


bot.run(TOKEN)