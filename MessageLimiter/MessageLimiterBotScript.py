import discord
from discord.ext import commands, tasks

TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = 123456789012345678  # Replace with your channel ID
MESSAGE_LIMIT = 1  # Configurable message limit per person

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await clean_channel()

async def clean_channel():
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("Channel not found!")
        return
    
    user_messages = {}
    async for message in channel.history(limit=None, oldest_first=True):
        if message.author.bot:
            continue
        if message.author.id not in user_messages:
            user_messages[message.author.id] = [message]
        else:
            user_messages[message.author.id].append(message)
            if len(user_messages[message.author.id]) > MESSAGE_LIMIT:
                await message.delete()

@client.event
async def on_message(message):
    if message.author.bot or message.channel.id != CHANNEL_ID:
        return
    
    channel = message.channel
    user_messages = []
    async for msg in channel.history(limit=100):  # Checks last 100 messages
        if msg.author == message.author:
            user_messages.append(msg)
    
    if len(user_messages) > MESSAGE_LIMIT:
        await message.delete()
        await message.channel.send(f"{message.author.mention}, the message limit is {MESSAGE_LIMIT} per person!", delete_after=5)
        return
    
    await client.process_commands(message)

client.run(TOKEN)
