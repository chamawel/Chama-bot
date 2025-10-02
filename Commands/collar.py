import discord
from discord.ext import commands
from discord import app_commands
import os
import dotenv
import random

dotenv.load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")

class BarkBackButton(discord.ui.View):
    def __init__(self, sender: discord.User, target: discord.User):
        super().__init__(timeout=30)
        self.sender = sender
        self.target = target

    @discord.ui.button(label="Bark back", style=discord.ButtonStyle.primary)
    async def bark_back(self, interaction: discord.Interaction, button: discord.ui.Button):
        barks = ["woof", "arf", "waf", "bow-wow", "bark"]
        bark_str = " ".join(random.choices(barks, k=random.randint(3, 7))) + "!~"
        color = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(
            title=f"{self.target.display_name} barked back !",
            description=(
                f"{self.target.mention} : {bark_str}\n"
                f"you own me now {self.sender.mention} ! i'll be a good dog !"
            ),
            color=color
        )
        embed.set_author(
            name=self.target.display_name,
            icon_url=self.target.display_avatar.url
        )
        embed.set_thumbnail(url=self.sender.display_avatar.url)
        await interaction.response.send_message(embed=embed)

class Collar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="collar", description="Collar a user like a nice puppy!")
    @app_commands.describe(target="The user to collar")
    @app_commands.allowed_contexts(guilds=True, dms= True, private_channels=True)
    @app_commands.user_install()
    async def collar(self, interaction: discord.Interaction, target: discord.User):
        color = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(
            description=f"{interaction.user.mention} collared {target.mention} like a nice puppy !",
            color=color
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url
        )
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.set_image(url="attachment://collar.jpg")  # Add image to embed
        view = BarkBackButton(sender=interaction.user, target=target)
        file = discord.File("assets/imgs/secret_imgs/collar.jpg", filename="collar.jpg")
        await interaction.response.send_message(embed=embed, view=view, file=file)

async def setup(bot):
    await bot.add_cog(Collar(bot))