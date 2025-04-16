from flask import Flask, jsonify, request, send_from_directory
import json, os

app = Flask(__name__)
GAMES_DIR = "game_data"

@app.route("/game/<game_id>")
def get_game(game_id):
    try:
        with open(f"{GAMES_DIR}/{game_id}.json") as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return {"error": "Game not found"}, 404

@app.route("/move", methods=["POST"])
def make_move():
    data = request.json
    game_id = data["game_id"]
    position = data["position"]
    player_id = data["player_id"]

    with open(f"{GAMES_DIR}/{game_id}.json") as f:
        game = json.load(f)

    if game["winner"] or game["board"][position] != "" or game["turn"] != player_id:
        return {"error": "Invalid move"}, 400

    symbol = "❌" if player_id == game["players"][0] else "⭕"
    game["board"][position] = symbol

    win_combos = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in win_combos:
        if game["board"][a] == game["board"][b] == game["board"][c] != "":
            game["winner"] = player_id
            break
    else:
        if all(game["board"]):
            game["winner"] = "draw"
        else:
            game["turn"] = game["players"][1] if game["turn"] == game["players"][0] else game["players"][0]

    with open(f"{GAMES_DIR}/{game_id}.json", "w") as f:
        json.dump(game, f)

    return {"success": True, "game": game}

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
