import discord
from discord.ext import commands
from discord import app_commands
import os
import dotenv
import numpy

dotenv.load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")

DICE_OPTIONS = [    # add more dice types as needed
    ("d100", 100),
    ("d20", 20),
    ("d6", 6),
    ("d4", 4)
]

class DiceSelect(discord.ui.View):
    """The view that holds the dropdown menu."""
    
    def __init__(self):
        super().__init__(timeout=30)
        options = [

            discord.SelectOption(label=name, description=f"Roll a {sides}-sided dice")
            for name, sides in DICE_OPTIONS
        ]
        self.add_item(DiceDropdown(options))

class DiceDropdown(discord.ui.Select):
    """The dropdown menu for selecting a dice to roll."""

    def __init__(self, options):
        super().__init__(placeholder="Choose a dice to roll...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        """The selection's handler says what to do when an option picked""" 

        dice_label = self.values[0]
        sides = next(s for n, s in DICE_OPTIONS if n == dice_label)
        result = numpy.random.randint(1, sides)

        color = discord.Color(numpy.random.randint(0, 0xFFFFFF))
        embed = discord.Embed(
            title=f"{interaction.user.display_name} rolled {result} on the {dice_label}",
            color=color
        )
        await interaction.response.send_message(embed=embed)

class DiceRoll(commands.Cog):
    """Cog for rolling dices."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Display available dice to roll")
    @app_commands.allowed_contexts(guilds=True, dms= True, private_channels=True)
    @app_commands.user_install()
    #@app_commands.guilds(discord.Object(id=GUILD_ID))
    async def roll(self, interaction: discord.Interaction):
        random_color = discord.Color(numpy.random.randint(0, 0xFFFFFF)) # Generate a random hex color  for the embed
        embed = discord.Embed(
            title="Available Dice",
            description="You can roll the following dice:",
            color=random_color
        )
        for name, sides in DICE_OPTIONS:
            embed.add_field(name=name, value=f"Rolls a {sides}-sided die", inline=False)
        embed.set_footer(text="Select a dice below to roll it!")

        await interaction.response.send_message(embed=embed, view=DiceSelect())

async def setup(bot):
    await bot.add_cog(DiceRoll(bot))