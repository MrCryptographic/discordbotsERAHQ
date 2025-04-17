# Auth scopes for bot

In Discord Developer Portal, go to installation:

![image](https://github.com/user-attachments/assets/ca61f1fd-bc90-4dd1-ac04-5b020cc485b1)


`application.commands` and `bot`

![image](https://github.com/user-attachments/assets/ffdc44df-8b50-4a91-a075-7123efac832d)


# Permissions for bot

`Send Messages`, `Read Message History`, `Use Slash Commands` and `View Channels`

![image](https://github.com/user-attachments/assets/f5f4b78a-a9f4-487c-894d-a2b44f8e9cb6)


# You need to make the following folder structure in order for this to work
```php
tictactoe/
│
├── game_data/
│   └── abc123.json        # Stores each game by ID (created automatically)
│
├── bot.py                 # Your Discord bot
├── web_server.py          # Backend for web
├── static/                # Web assets (HTML/JS)
│   └── index.html
```
