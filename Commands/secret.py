import discord
from discord.ext import commands
from discord import app_commands
import os
import dotenv
import numpy

dotenv.load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")
SECRET_PASSWORD = os.getenv("SECRET_PASSWORD")


class Secret(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="secret", description="Enter the password and a size to get a secret pattern")
    @app_commands.describe(password="The secret password", size="The size for the pattern")
    @app_commands.allowed_contexts(guilds=True, dms= True, private_channels=True)
    @app_commands.user_install()
    #@app_commands.guilds(discord.Object(id=GUILD_ID))
    async def secret(self, interaction: discord.Interaction, password: str, size: int):
        if password != SECRET_PASSWORD:
            await interaction.response.send_message("Incorrect password.", ephemeral=True)
            return

        # 10% chance of happening output
        if numpy.random.uniform() < 0.25:  # 25% chance
            img_dir = "assets/imgs/secret_imgs"
            try:
                files = [
                    f for f in os.listdir(img_dir)
                    if os.path.isfile(os.path.join(img_dir, f)) and f != "collar.jpg"
                ]  # Exclude "collar.jpg"
            except FileNotFoundError:
                files = []
            if files:
                chosen_file = numpy.random.choice(files)
                img_path = os.path.join(img_dir, chosen_file)
                with open(img_path, "rb") as img_file:
                    await interaction.response.send_message(file=discord.File(img_file, chosen_file))
                return
        
        # normal output
        x = f"{' ' * size}"         
        result = f"({x}.{x})({x}.{x})"
        await interaction.response.send_message(result)

async def setup(bot):
    await bot.add_cog(Secret(bot))