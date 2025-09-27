import discord
from discord.ext import commands
from discord import app_commands
import os
import dotenv

dotenv.load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="hello", description="send hello")
    #@app_commands.guilds(discord.Object(id=GUILD_ID))
    async def say_hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("hello")

async def setup(bot):
    await bot.add_cog(Hello(bot))