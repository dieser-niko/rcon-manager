# rcon-manager
A collection of scripts for managing my minecraft server.

I'm using RCON in order to control the server without the need for a secondary tool/dashboard to get access to the console.

The RCON port is not open to the public, so even though the connection is unencrypted, it shouldn't matter because the script is on the same machine as the minecraft server.

# rconbot
A simple discord bot with simple controls to the server.
The bot can only be accessed on a specified discord guild.

| Command | Description | Example | can be accessed by |
| ------- | --- | --- | --- |
| `/start` | starts the server | `/start` | everyone |
| `/stop` | stops the server | `/stop` | owner |
| `/restart` | restarts the server | `/restart` | owner |
| `/run <command>` | runs the command and returns the console output (some exceptions) | `/run say hi` | owner |
| `/logs [offset]` | shows the last 10 log entries. includes buttons to scroll back | `/logs 2` | admins |

## Setup

- Create a discord bot (I'm not going to explain that here)
- Clone the repo
- Create a virtual environment with `python3 -m venv venv`
- Activate the environment with `source ./venv/bin/activate`
- Install requirements with `pip install -r requirements.txt`
- Edit /rconbot/main.py
- You can change all variables written in upper case letters
- Make sure that RCON is activated in the server.properties
- start the bot with the bash file included or use the service file (make sure to run as root)


# backup
TODO
