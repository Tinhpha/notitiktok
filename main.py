import asyncio
import discord
from discord import Intents
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent
from TikTokLive.client.errors import UserOfflineError
from flask import Flask
from threading import Thread
import os
import time
from collections import defaultdict

# ===== CONFIG =====
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TIKTOK_USERNAME = "saaapizzy"

LIVE_CHANNEL_ID = 1475007140954378401
WELCOME_CHANNEL_ID = 1475105492614254592
RULE_CHANNEL_ID = 1475105584624701543
ANNOUNCE_CHANNEL_ID = 1475046093921189964
MEMBER_ROLE_ID = 1475043789465714819

MENTION_TEXT = "@everyone"
# ==================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
tiktok = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

live_sent = False
user_messages = defaultdict(list)

# ===== READY =====
@client.event
async def on_ready():
    print(f"Bot đã đăng nhập: {client.user}")
    client.loop.create_task(check_live_loop())


# ===== LIVE CHECK =====
async def check_live_loop():
    global live_sent

    while True:
        try:
            await tiktok.connect()
        except UserOfflineError:
            live_sent = False
            await asyncio.sleep(30)
        except Exception as e:
            print("Lỗi:", e)
            await asyncio.sleep(30)


@tiktok.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    global live_sent

    if live_sent:
        return

    channel = client.get_channel(LIVE_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🔴 ĐANG LIVE TRÊN TIKTOK!",
            description=f"https://www.tiktok.com/@{TIKTOK_USERNAME}/live",
            color=0xff0050
        )
        embed.set_footer(text="Vào xem ngay đi anh em 🚀")
        await channel.send(content=MENTION_TEXT, embed=embed)

    live_sent = True


# ===== WELCOME + AUTO ROLE =====
@client.event
async def on_member_join(member):
    channel = client.get_channel(WELCOME_CHANNEL_ID)

    # Auto role
    role = member.guild.get_role(MEMBER_ROLE_ID)
    if role:
        await member.add_roles(role)

    # Welcome embed
    if channel:
        embed = discord.Embed(
            title="🎉 Chào mừng bạn đến với server!",
            description=(
                f"{member.mention}\n\n"
                "Chúng tôi rất vui mừng chào đón bạn gia nhập cộng đồng của chúng tôi! ✈️\n\n"
                f"📖 Vui lòng đọc kỹ <#{RULE_CHANNEL_ID}>\n"
                f"📢 Đừng quên xem <#{ANNOUNCE_CHANNEL_ID}> để cập nhật thông tin mới nhất."
            ),
            color=0x00b0f4
        )
        embed.set_thumbnail(
            url=member.avatar.url if member.avatar else member.default_avatar.url
        )
        await channel.send(embed=embed)


# ===== ANTI SPAM =====
@client.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    current_time = time.time()

    user_messages[user_id].append(current_time)
    user_messages[user_id] = [
        t for t in user_messages[user_id] if current_time - t <= 5
    ]

    if len(user_messages[user_id]) >= 5:
        embed = discord.Embed(
            title="⚠️ Spam detected!",
            description=f"{message.author.mention} Bình tĩnh bro 🧠",
            color=0xffcc00
        )
        await message.channel.send(embed=embed)
        user_messages[user_id] = []


# ===== KEEP ALIVE WEB =====
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run_web).start()

client.run(DISCORD_TOKEN)