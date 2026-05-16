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
    await bot.load_extension('cogs.admin')
    await bot.tree.sync()
    print('Commands synced!')
    
    # Set bot status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="bcine.app"))
    
    # Post support embed when bot comes online
    support_cog = bot.get_cog('Support')
    if support_cog:
        await support_cog.post_support_embed()

if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    bot.run(TOKEN)
