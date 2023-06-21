from rcon.source import Client
import discord
from discord import app_commands, ui
from discord.ext import tasks
import subprocess
import asyncio

RCON_PASSWORD = ""

BOT_TOKEN = ""
GUILD_ID = 123456789012345678
OWNER_ID = 901234567890123456

MINECRAFT_SERVICE_NAME = "mcserver.service"
LATEST_LOG_FILE = "/path/to/your/mcserver/logs/latest.log"


def run_command(inp):
    with Client('127.0.0.1', 25575, passwd=RCON_PASSWORD) as client:
        return client.run(inp)

intents = discord.Intents.default()

bot = discord.Client(intents=intents)

tree = app_commands.CommandTree(bot)


@tree.command(name="run", description="Run a command on the Minecraft server", guild=discord.Object(id=GUILD_ID))
async def run(ctx, command: str):
    if ctx.user.id == OWNER_ID:
        await ctx.response.send_message(f"```\n{run_command(command)}```")
    else:
        await ctx.response.send_message("Access denied", ephemeral=True, delete_after=5)

@tree.command(name="start", description="Start the Minecraft server", guild=discord.Object(id=GUILD_ID))
async def start(ctx):
    process = subprocess.Popen(["systemctl", "start", MINECRAFT_SERVICE_NAME])
    while process.poll() is None:
        await asyncio.sleep(0.1)
    await ctx.response.send_message("Server started.", ephemeral=True, delete_after=5)

@tree.command(name="stop", description="Stop the Minecraft server", guild=discord.Object(id=GUILD_ID))
async def stop(ctx):
    if ctx.user.id == OWNER_ID:
        process = subprocess.Popen(["systemctl", "stop", MINECRAFT_SERVICE_NAME])
        while process.poll() is None:
            await asyncio.sleep(0.1)
        await ctx.response.send_message("Server stopped.", ephemeral=True, delete_after=5)
    else:
        await ctx.response.send_message("Access denied", ephemeral=True, delete_after=5)


@tree.command(name="restart", description="Restart the Minecraft server", guild=discord.Object(id=GUILD_ID))
async def restart(ctx):
    if ctx.user.id == OWNER_ID:
        process = subprocess.Popen(["systemctl", "restart", MINECRAFT_SERVICE_NAME])
        while process.poll() is None:
            await asyncio.sleep(0.1)
        await ctx.response.send_message("Server stopped.", ephemeral=True, delete_after=5)
    else:
        await ctx.response.send_message("Access denied", ephemeral=True, delete_after=5)



async def get_logs(interaction, offset, og, callback=False):
    if interaction.user.id != og:
        await interaction.response.send_message("Call `/logs` to use it yourself.", ephemeral=True, delete_after=5)
        return

    async def left_callback(interaction):
        await get_logs(interaction, offset+1, og, callback=True)
    async def right_callback(interaction):
        await get_logs(interaction, offset+-1, og, callback=True)
    
    with open(LATEST_LOG_FILE, "r") as fobj:
        text = fobj.read()
    text = text.split("\n")[:-1]
    current_text = '\n'.join(text[-10 - (offset*10):-(offset*10) if offset else None])

    left_button = ui.Button(label="<", disabled=(len(text) - 1) // 10 <=offset)
    left_button.callback = left_callback
    right_button = ui.Button(label=">", disabled=offset<=0)
    right_button.callback = right_callback

    log_buttons = ui.View()
    log_buttons.add_item(left_button)
    log_buttons.add_item(right_button)
    
    if callback:
        await interaction.response.edit_message(content=f"```{current_text}```", view=log_buttons)
    else:
        await interaction.response.send_message(f"```{current_text}```", view=log_buttons)


@tree.command(name="logs", description="Get logs of the Minecraft server", guild=discord.Object(id=GUILD_ID))
async def logs_command(interaction, offset: int = 0):
    if interaction.user.guild_permissions.administrator:
        await get_logs(interaction, offset, interaction.user.id)
    else:
        await interaction.response.send_message("Access denied", ephemeral=True, delete_after=5)



@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")


bot.run(BOT_TOKEN)
