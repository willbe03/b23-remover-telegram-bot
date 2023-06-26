# Requirements
```
conda create --name tgbot
conda install -c conda-forge python-telegram-bot
conda install requests
```

# Usage
Replace `BOT_TOKEN` with your token from @bot_father

# Docker
```
docker build -t b23remover .
```
```
docker run -d --name b23remover --restart=always -e BOT_TOKEN=xxxxxxxx b23remover
```
