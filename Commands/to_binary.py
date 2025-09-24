import discord
from discord.ext import commands
from discord import app_commands
import os
import dotenv

dotenv.load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")

class To_binary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="to_binary", description="converts an interger to binary")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def to_binary(self, interaction: discord.Interaction, number : int):
        binary = ""
        while number > 0:
            for i in range(8):
                binary += str(number % 2) + ""
                number = number // 2
            binary += " | "
            
        await interaction.response.send_message(f"binary: {binary}")


async def setup(bot):
    await bot.add_cog(To_binary(bot))