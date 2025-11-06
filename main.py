import os
import discord
from discord.ext import commands
import paho.mqtt.client as mqtt

# === Ambil variabel dari Railway ===
TOKEN = os.getenv("DISCORD_TOKEN")
MQTT_SERVER = os.getenv("MQTT_SERVER")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

# === Setup Discord ===
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# === Setup MQTT ===
client = mqtt.Client()
if MQTT_USER:
    client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_SERVER, MQTT_PORT, 60)
client.loop_start()

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} aktif!")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("🤖 Bot MQTT sudah online di Railway!")

@bot.command()
async def onlampu(ctx):
    client.publish("lampu/control", "ON")
    await ctx.reply("💡 Lampu dinyalakan!")

@bot.command()
async def offlampu(ctx):
    client.publish("lampu/control", "OFF")
    await ctx.reply("🌙 Lampu dimatikan!")

bot.run(TOKEN)
