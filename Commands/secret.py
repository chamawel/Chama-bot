import discord
from discord.ext import commands
from discord import app_commands
import os
import dotenv

dotenv.load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")
SECRET_PASSWORD = os.getenv("SECRET_PASSWORD")

class Secret(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="secret", description="Enter the password and a size to get a secret pattern")
    @app_commands.describe(password="The secret password", size="The size for the pattern")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def secret(self, interaction: discord.Interaction, password: str, size: int):
        if password != SECRET_PASSWORD:
            await interaction.response.send_message("Incorrect password.", ephemeral=True)
            return

        x = f"{' ' * size}"         
        result = f"({x}.{x})({x}.{x})"
        await interaction.response.send_message(result) # sends PEAK to the channel

async def setup(bot):
    await bot.add_cog(Secret(bot))