import discord
from discord.ext import commands
import os
import asyncio
from TikTokLive import TikTokLiveClient

TOKEN = os.getenv("TOKEN")

# ====== CONFIG ======
WELCOME_CHANNEL_ID = 1475105492614254592
RULE_CHANNEL_ID = 1475105584624701543
ANNOUNCE_CHANNEL_ID = 1475046093921189964
MEMBER_ROLE_ID = 1475043789465714819

LIVE_CHANNEL_ID = 1475007140954378401
TIKTOK_USERNAME = "saaapizzy"
# ====================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ====== MEMBER JOIN EVENT ======
@bot.event
async def on_member_join(member):
    print("🔥 MEMBER JOINED:", member.name)

    role = member.guild.get_role(MEMBER_ROLE_ID)
    if role:
        await member.add_roles(role)
        print("✅ Đã gán role Member")

    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        message = (
            f"👋 Chào mừng {member.mention} đến với server!\n\n"
            f"📖 Vui lòng đọc luật tại: <#{RULE_CHANNEL_ID}>\n"
            f"📢 Xem thông báo mới nhất tại: <#{ANNOUNCE_CHANNEL_ID}>"
        )
        await channel.send(message)
        print("✅ Đã gửi tin chào")

# ====== TEST COMMAND ======
@bot.command()
@commands.has_permissions(administrator=True)
async def testlive(ctx):
    await ctx.send("🚀 Test thông báo LIVE thành công!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

# ====== TIKTOK LIVE SYSTEM ======
tiktok_client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)
is_live = False


async def check_live_status():
    global is_live

    while True:
        try:
            live_status = await tiktok_client.is_live()

            if live_status:
                if not is_live:
                    print("🔴 LIVE detected!")

                    channel = bot.get_channel(LIVE_CHANNEL_ID)
                    if channel:
                        live_url = f"https://www.tiktok.com/@{TIKTOK_USERNAME}/live"

                        embed = discord.Embed(
                            title="🔴 Em Sa ĐÃ LÊN SÓNG!",
                            description="🔥 Stream đã bắt đầu trên TikTok!",
                            color=discord.Color.red()
                        )

                        embed.add_field(
                            name="🎥 Xem trực tiếp:",
                            value=live_url,
                            inline=False
                        )

                        embed.set_footer(text="Vào xem và thả tim cho em với ❤️")

                        # Gửi embed + ping
                        await channel.send("@everyone", embed=embed)

                        # Gửi link riêng để Discord tự nhúng thumbnail
                        await channel.send(live_url)

                    is_live = True
            else:
                if is_live:
                    print("⚫ Live ended")
                is_live = False

        except Exception as e:
            print("❌ Lỗi check live:", e)

        await asyncio.sleep(60)  # 1 phút check 1 lần


# ====== READY EVENT ======
@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập với tên {bot.user}")
    asyncio.create_task(check_live_status())


bot.run(TOKEN)