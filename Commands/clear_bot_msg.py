import discord
from discord.ext import commands
from discord import app_commands
import os
import dotenv

dotenv.load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")
ALLOWED_ROLE_ID = int(os.getenv("ALLOWED_ROLE_ID", 0)) 
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", 0))  

class ClearBotMsg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="clear_bot_msg", description="Clear the bot's messages")
    @app_commands.describe(amount="Number of bot messages to delete")
    @app_commands.allowed_contexts(guilds=True, dms= True, private_channels=True)
    @app_commands.user_install()
    #@app_commands.guilds(discord.Object(id=GUILD_ID))
    async def clear_bot_msg(self, interaction: discord.Interaction, amount: int):
        # Check for allowed user
        if interaction.user.id == ALLOWED_USER_ID:
            allowed = True
        # Check for allowed role
        elif ALLOWED_ROLE_ID and any(role.id == ALLOWED_ROLE_ID for role in getattr(interaction.user, "roles", [])):
            allowed = True
        else:
            allowed = False

        if not allowed:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        deleted = 0
        async for msg in interaction.channel.history(limit=100):
            if msg.author == interaction.client.user:
                await msg.delete()
                deleted += 1
                if deleted >= amount:
                    break
        await interaction.followup.send(f"Deleted {deleted} bot message(s).", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ClearBotMsg(bot))