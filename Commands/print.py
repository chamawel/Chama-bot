import discord
from discord.ext import commands
from discord import app_commands
import os
import dotenv

dotenv.load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")

class Print(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="print", description="copies the text you give")
    @app_commands.describe(value="the text to copy")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def say_hello(self, interaction: discord.Interaction, value: str):
        await interaction.response.send_message(value)

async def setup(bot):
    await bot.add_cog(Print(bot))