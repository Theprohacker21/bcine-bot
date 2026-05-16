import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.load_extension('cogs.support')
    await bot.tree.sync()
    print('Commands synced!')

if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
