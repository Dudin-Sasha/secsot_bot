curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.14
uv python pin 3.14
uv pip install -r requirements.txt
echo Download is ended. You can start bots by open `bot start.sh`. 
echo Click any key to exit...
pause >nul