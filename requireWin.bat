powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv python install 3.14
uv python pin 3.14
uv pip install -r requirements.txt
echo Download is ended. You can start bots by open `bot start.bat`. 
echo Click any key to exit...
pause >nul