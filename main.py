from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = discord.Object(id=os.getenv("GUILD_ID"))

class Client(commands.Bot):
    
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
        try:
            GUILD = discord.Object(id=os.getenv("GUILD_ID"))
            synced = await self.tree.sync(guild=GUILD)
            print(f"Synced {len(synced)} commands to guild {GUILD.id}")
        except Exception as e:
            print(f"Error syncing commands: {e}")
            
    
    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.lower().endswith("quoi"):
            await message.reply("feur")    



intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix="!",intents=intents)

async def main():
    for fn in os.listdir("./Commands"):
        if fn.endswith(".py") and not fn.startswith("__"):
            await client.load_extension(f"Commands.{fn[:-3]}")
    await client.start(BOT_TOKEN)

asyncio.run(main())