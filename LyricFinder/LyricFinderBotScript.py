import discord
from discord.ext import commands
import lyricsgenius
import asyncio

# Tokens (Replace these with actual values)
DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"
GENIUS_TOKEN = "YOUR_GENIUS_TOKEN_HERE"
LOG_CHANNEL_ID = LOG_CHANNEL_ID_HERE  # Replace with your log channel ID

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Required to process commands

# Initialize bot with command prefix
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize Genius API
genius = lyricsgenius.Genius(GENIUS_TOKEN)

@bot.event
async def on_ready():
    """Executed when bot starts."""
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f"✅ **{bot.user.name} is now online!**\n"
                           f"Use `!lyrics <song>` to find lyrics!")

@bot.command()
async def lyrics(ctx, *, song_name):
    """Fetch lyrics from Genius"""
    async with ctx.typing():  # Shows "typing..." indicator in Discord
        await asyncio.sleep(1)  # Simulate loading time
        song = genius.search_song(song_name)

    if song:
        lyrics = song.lyrics[:1900]  # Limit to fit Discord message
        await ctx.send(f"**{song.title}** by {song.artist}:\n```{lyrics}```")
    else:
        await ctx.send("Lyrics not found.")

async def shutdown():
    """Gracefully shuts down the bot and sends a message to the log channel"""
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send("❌ **Bot is shutting down...**\n"
                           "⚠️ `!lyrics` will not work until the bot is restarted.")
    await bot.close()

async def wait_for_exit():
    """Runs a loop that waits for 'exit' input in the terminal"""
    loop = asyncio.get_event_loop()
    while True:
        command = await loop.run_in_executor(None, input, "Type 'exit' to stop the bot: ")
        if command.lower() == "exit":
            print("Shutting down bot...")
            await shutdown()
            break

async def main():
    """Run bot and exit listener in parallel"""
    await asyncio.gather(bot.start(DISCORD_TOKEN), wait_for_exit())

# Run bot using asyncio to allow terminal input
asyncio.run(main())
