import asyncio
import discord
from discord import Intents
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent
from TikTokLive.client.errors import UserOfflineError

# ===== CONFIG =====
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TIKTOK_USERNAME = "saaapizzy"
CHANNEL_ID = 1475007140954378401  # DÁN CHANNEL ID VÀO ĐÂY
MENTION_TEXT = "@everyone"
# ==================

intents = discord.Intents.default()
intents.message_content = True  # BẮT BUỘC
client = discord.Client(intents=intents)

tiktok = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

live_sent = False


@client.event
async def on_ready():
    print(f"Bot đã đăng nhập: {client.user}")
    client.loop.create_task(check_live_loop())


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == "!testlive":
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(
                f"{MENTION_TEXT} https://www.tiktok.com/@{TIKTOK_USERNAME}/live"
            )


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

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(
            f"{MENTION_TEXT} https://www.tiktok.com/@{TIKTOK_USERNAME}/live"
        )

    live_sent = True


client.run(DISCORD_TOKEN)