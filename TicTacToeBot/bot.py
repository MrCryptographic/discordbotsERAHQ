import discord
import os
import json
from discord.ext import commands
from discord import app_commands

GAMES_DIR = "game_data"
os.makedirs(GAMES_DIR, exist_ok=True)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

def load_game(game_id):
    with open(f"{GAMES_DIR}/{game_id}.json") as f:
        return json.load(f)

def save_game(game_id, data):
    with open(f"{GAMES_DIR}/{game_id}.json", "w") as f:
        json.dump(data, f)

def render_board(board):
    symbols = [cell or "⬜" for cell in board]
    return f"{symbols[0]}{symbols[1]}{symbols[2]}\n{symbols[3]}{symbols[4]}{symbols[5]}\n{symbols[6]}{symbols[7]}{symbols[8]}"

@tree.command(name="start_ttt", description="Start a Tic Tac Toe game")
@app_commands.describe(opponent="The user you're challenging")
async def start(interaction: discord.Interaction, opponent: discord.User):
    game_id = f"{interaction.user.id}_{opponent.id}"
    board = [""] * 9
    game = {
        "game_id": game_id,
        "players": [interaction.user.id, opponent.id],
        "board": board,
        "turn": interaction.user.id,
        "winner": None
    }
    save_game(game_id, game)
    await interaction.response.send_message(
        f"Tic Tac Toe started between <@{interaction.user.id}> and <@{opponent.id}>\n" +
        f"Game ID: `{game_id}`\n" +
        render_board(board)
    )

@tree.command(name="move", description="Make a move in Tic Tac Toe")
@app_commands.describe(game_id="The game ID", position="0-8 position on the board")
async def move(interaction: discord.Interaction, game_id: str, position: int):
    if not os.path.exists(f"{GAMES_DIR}/{game_id}.json"):
        await interaction.response.send_message("Game not found.")
        return

    game = load_game(game_id)

    if game["winner"]:
        await interaction.response.send_message("This game has already ended.")
        return

    if interaction.user.id != game["turn"]:
        await interaction.response.send_message("Not your turn.")
        return

    if game["board"][position] != "":
        await interaction.response.send_message("That space is already taken.")
        return

    symbol = "❌" if interaction.user.id == game["players"][0] else "⭕"
    game["board"][position] = symbol

    # Check for win
    win_combos = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for combo in win_combos:
        a,b,c = combo
        if game["board"][a] == game["board"][b] == game["board"][c] != "":
            game["winner"] = interaction.user.id
            save_game(game_id, game)
            await interaction.response.send_message(f"{render_board(game['board'])}\n<@{interaction.user.id}> wins!")
            return

    # Check for draw
    if all(game["board"]):
        game["winner"] = "draw"
        save_game(game_id, game)
        await interaction.response.send_message(f"{render_board(game['board'])}\nIt's a draw!")
        return

    # Continue game
    game["turn"] = game["players"][1] if game["turn"] == game["players"][0] else game["players"][0]
    save_game(game_id, game)
    await interaction.response.send_message(f"{render_board(game['board'])}\nNext turn: <@{game['turn']}>")

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {bot.user}!")

bot.run("token")
