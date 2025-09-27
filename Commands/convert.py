import discord
from discord.ext import commands
from discord import app_commands
import os
import dotenv
import random

dotenv.load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")

CONVERT_OPTIONS = [
    ("To Celsius", "celsius"),
    ("To Fahrenheit", "fahrenheit"),
    ("To Binary", "binary"),
    ("To Hexadecimal", "hexadecimal"),
]

class ConvertSelect(discord.ui.View):
    """the dropdown view, makes the convert menu appear"""

    def __init__(self, value):
        super().__init__(timeout=30)
        options = [
            discord.SelectOption(label=label, value=val)
            for label, val in CONVERT_OPTIONS           #i love that python syntax it makes me feel smart and it looks cool (picks the options from the list of tuples above)
        ]
        self.add_item(ConvertDropdown(options, value))

class ConvertDropdown(discord.ui.Select):
    """ The select menu for convertions itself"""

    def __init__(self, options, value):
        super().__init__(placeholder="Choose a unit to convert to...", min_values=1, max_values=1, options=options)
        self.value_to_convert = value

    async def callback(self, interaction: discord.Interaction):
        """The selection's handler says what to do when an option is selected""" 

        choice : str = self.values[0]
        value  : int = self.value_to_convert
        color  : str = discord.Color(random.randint(0, 0xFFFFFF))
        value  : int
        result : float
        text   : str

        try:
            match choice: # switch case cus ooohhh fancy (and cleaner)

                case "celsius":                         # F to C
                    result = (value - 32) * 5 / 9
                    text = f"{value}°F = {result:.2f}°C"

                case "fahrenheit":                      # C to F
                    result = value * 9 / 5 + 32
                    text = f"{value}°C = {result:.2f}°F"

                case "binary":                          # int to binary (signed)
                    val_copy = value
                    bits = 8

                    # Find minimum bits needed (at least 8)
                    if val_copy < 0:
                        # Two's complement (we saw that in class)
                        val_copy_unsigned = (abs(val_copy) ^ ((1 << bits) - 1)) + 1
                        val_copy_unsigned &= (1 << bits) - 1
                        val_copy = val_copy_unsigned
                    else:
                        val_copy = val_copy
                    
                    # Build bytes
                    bytes_list = []
                    total = abs(value)
                    
                    # Calculate how many bytes needed (at least 1)
                    min_bytes = max(1, (total.bit_length() + 7) // 8)
                    val_copy = value if value >= 0 else (1 << (min_bytes * 8)) + value
                    
                    for _ in range(min_bytes):
                        byte = ""
                        for i in range(8):
                            byte = str(val_copy % 2) + byte
                            val_copy = val_copy // 2
                        
                        bytes_list.insert(0, byte)
                    
                    text = f"binary: {' | '.join(bytes_list)}"

                case "hexadecimal":                     # int to hex (signed)
                    total = abs(value)
                    min_bytes = max(1, (total.bit_length() + 7) // 8)
                    
                    if value < 0:
                        # Two's complement for negative numbers and yes i'm too lazy to make it fully by myself
                        hex_value = hex((1 << (min_bytes * 8)) + value)
                    else:
                        hex_value = hex(value) 
                    
                    # Format to always show full bytes
                    hex_str = hex_value[2:].zfill(min_bytes * 2)
                    text = f"hexadecimal: 0x{hex_str}"

        except Exception as e:              #for dummies that enters str and floats
            text = f"Convertion error: {e}"

        embed = discord.Embed(
            title="Conversion Result",
            description=f"**{text}**",
            color=color
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

class Convert(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="convert", description="Convert an integer value to another unit")
    @app_commands.describe(value="The value to convert (must be an integer)") 
    #@app_commands.guilds(discord.Object(id=GUILD_ID))
    async def convert(self, interaction: discord.Interaction, value: int):
        color = discord.Color(random.randint(0, 0xFFFFFF))
        embed = discord.Embed(
            title="Choose Conversion",
            description=f"Select the unit you want to convert __{value}__ to:",
            color=color
        )
        await interaction.response.send_message(embed=embed, view=ConvertSelect(value))

async def setup(bot):
    await bot.add_cog(Convert(bot))