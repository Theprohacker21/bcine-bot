import discord
from discord.ext import commands
from discord import app_commands
import sys
import os


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="refresh", description="Refresh the bot's cogs")
    @app_commands.checks.has_permissions(administrator=True)
    async def refresh(self, interaction: discord.Interaction):
        """Reload all bot cogs"""
        try:
            await interaction.response.defer(ephemeral=True)
            
            # Reload support cog
            await self.bot.reload_extension('cogs.support')
            
            # Sync commands
            await self.bot.tree.sync()
            
            embed = discord.Embed(
                title="Bot Refreshed",
                description="All cogs have been reloaded and commands synced.",
                color=discord.Color.green()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            print("Bot cogs refreshed successfully!")
            
        except Exception as e:
            embed = discord.Embed(
                title="Refresh Failed",
                description=f"Error: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            print(f"Error refreshing bot: {str(e)}")

    @app_commands.command(name="restart", description="Restart the bot")
    @app_commands.checks.has_permissions(administrator=True)
    async def restart(self, interaction: discord.Interaction):
        """Restart the bot"""
        try:
            await interaction.response.defer(ephemeral=True)
            
            embed = discord.Embed(
                title="Bot Restarting",
                description="The bot is restarting. Please wait...",
                color=discord.Color.orange()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            
            print("Bot is restarting...")
            await self.bot.close()
            
        except Exception as e:
            embed = discord.Embed(
                title="Restart Failed",
                description=f"Error: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            print(f"Error restarting bot: {str(e)}")


async def setup(bot):
    await bot.add_cog(Admin(bot))
