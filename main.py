import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

# ====== CONFIG ======
WELCOME_CHANNEL_ID = 1475105492614254592
RULE_CHANNEL_ID = 1475105584624701543
ANNOUNCE_CHANNEL_ID = 1475046093921189964
MEMBER_ROLE_ID = 1475043789465714819
# ====================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # BẮT BUỘC

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập với tên {bot.user}")
    print("Members intent:", bot.intents.members)


# ====== MEMBER JOIN EVENT ======
@bot.event
async def on_member_join(member):
    print("🔥 MEMBER JOINED:", member.name)

    # Gán role Member
    role = member.guild.get_role(MEMBER_ROLE_ID)
    if role:
        await member.add_roles(role)
        print("✅ Đã gán role Member")

    # Gửi tin nhắn chào
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        message = (
            f"👋 Chào mừng {member.mention} đến với server!\n\n"
            "✈️ Chúng tôi rất vui mừng chào đón bạn gia nhập cộng đồng của chúng tôi!\n\n"
            f"📖 Vui lòng đọc luật tại: <#{RULE_CHANNEL_ID}>\n"
            f"📢 Xem thông báo mới nhất tại: <#{ANNOUNCE_CHANNEL_ID}>"
        )
        await channel.send(message)
        print("✅ Đã gửi tin chào")


# ====== TEST LIVE ======
@bot.command()
@commands.has_permissions(administrator=True)
async def testlive(ctx):
    await ctx.send("🚀 Test thông báo LIVE thành công!")


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)


bot.run(TOKEN)