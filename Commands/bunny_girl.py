import discord
from discord.ext import commands
from discord import app_commands
import os
import dotenv
import numpy

dotenv.load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")

IMG_DIR = "assets/imgs/bunny_girls"  # Directory where bunny girl images are stored

class BunnyGirl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bunny_girl", description="sends a random img of a bunny girl")
    @app_commands.allowed_contexts(guilds=True, dms= True, private_channels=True)
    @app_commands.user_install()
    #@app_commands.guilds(discord.Object(id=GUILD_ID))
    
    async def bunnyGirl(self, interaction: discord.Interaction):
        try:
            files = [f for f in os.listdir(IMG_DIR) if os.path.isfile(os.path.join(IMG_DIR, f))]
        except FileNotFoundError:
            await interaction.response.send_message("Image folder not found!", ephemeral=True)
            return

        if not files:
            await interaction.response.send_message("No images found!", ephemeral=True)
            return

        chosen_file = numpy.random.choice(files)
        img_path = os.path.join(IMG_DIR, chosen_file)

        with open(img_path, 'rb') as img_file:
            await interaction.response.send_message(file=discord.File(img_file, chosen_file))

async def setup(bot):
    await bot.add_cog(BunnyGirl(bot))