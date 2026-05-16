import discord
from discord.ext import commands
from discord import app_commands
import uuid

class TicketView(discord.ui.View):
    def __init__(self, bot, ticket_id, author_id, channel_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.ticket_id = ticket_id
        self.author_id = author_id
        self.channel_id = channel_id
        self.claimed_by = None
        self.is_claimed = False

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.green, custom_id=f"claim_button")
    async def claim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        support_role_id = 1465374880865456261
        support_role = interaction.guild.get_role(support_role_id)
        
        if support_role not in interaction.user.roles:
            await interaction.response.send_message("You don't have permission to claim this ticket.", ephemeral=True)
            return
        
        if self.is_claimed:
            await interaction.response.send_message("This ticket is already claimed.", ephemeral=True)
            return
        
        self.is_claimed = True
        self.claimed_by = interaction.user.id
        
        # Update button appearance
        button.label = "Unclaim"
        button.style = discord.ButtonStyle.gray
        button.custom_id = f"unclaim_button_{self.claimed_by}"
        
        # Update the message with new button
        await interaction.response.defer()
        message = await interaction.channel.fetch_message(interaction.message.id)
        await message.edit(view=self)
        
        # Send confirmation message
        embed = discord.Embed(
            title="Ticket Claimed",
            description=f"{interaction.user.mention} has claimed this ticket.",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Unclaim", style=discord.ButtonStyle.gray, custom_id=f"unclaim_button", disabled=True)
    async def unclaim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        support_role_id = 1465374880865456261
        support_role = interaction.guild.get_role(support_role_id)
        
        if support_role not in interaction.user.roles:
            await interaction.response.send_message("You don't have permission to unclaim this ticket.", ephemeral=True)
            return
        
        if not self.is_claimed or self.claimed_by != interaction.user.id:
            await interaction.response.send_message("Only the person who claimed this ticket can unclaim it.", ephemeral=True)
            return
        
        self.is_claimed = False
        self.claimed_by = None
        
        # Update button appearance back to claim
        button.label = "Claim"
        button.style = discord.ButtonStyle.green
        button.custom_id = "claim_button"
        button.disabled = False
        
        # Find and update the claim button
        for item in self.children:
            if isinstance(item, discord.ui.Button) and item.label == "Claim":
                item.disabled = False
                item.style = discord.ButtonStyle.green
        
        await interaction.response.defer()
        message = await interaction.channel.fetch_message(interaction.message.id)
        await message.edit(view=self)
        
        embed = discord.Embed(
            title="Ticket Unclaimed",
            description=f"{interaction.user.mention} has unclaimed this ticket.",
            color=discord.Color.orange()
        )
        await interaction.followup.send(embed=embed)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, custom_id="close_button")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        support_role_id = 1465374880865456261
        support_role = interaction.guild.get_role(support_role_id)
        
        if support_role not in interaction.user.roles:
            await interaction.response.send_message("You don't have permission to close this ticket.", ephemeral=True)
            return
        
        # Create confirmation view
        confirm_view = ConfirmCloseView(interaction.channel)
        
        embed = discord.Embed(
            title="Close Ticket?",
            description="Are you sure you want to close this ticket? This will delete the channel.",
            color=discord.Color.red()
        )
        
        await interaction.response.send_message(embed=embed, view=confirm_view)


class ConfirmCloseView(discord.ui.View):
    def __init__(self, channel):
        super().__init__(timeout=60)
        self.channel = channel

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.red, custom_id="confirm_close")
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.channel.delete()

    @discord.ui.button(label="No", style=discord.ButtonStyle.gray, custom_id="confirm_no_close")
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        # Delete the confirmation message
        await interaction.message.delete()


class SupportDropdown(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = [
            discord.SelectOption(label="General", value="general", description="Create a general support ticket"),
            discord.SelectOption(label="Support or Bug/Suggestion", value="support_bug", description="Create a support, bug or suggestion ticket")
        ]
        super().__init__(placeholder="Select ticket type...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_type = self.values[0]
        
        if selected_type == "general":
            category_id = 1504828516347412512
        else:  # support_bug
            category_id = 1505026545100525660
        
        category = interaction.guild.get_channel(category_id)
        if not category:
            await interaction.response.send_message("Category not found. Please check the configuration.", ephemeral=True)
            return
        
        # Create ticket channel
        ticket_id = str(uuid.uuid4())[:8]
        channel_name = f"ticket-{ticket_id}"
        
        try:
            ticket_channel = await category.create_text_channel(
                channel_name,
                topic=f"Support ticket - Type: {selected_type} - User: {interaction.user.mention}"
            )
            
            # Create ticket embed
            embed = discord.Embed(
                title=f"Support Ticket #{ticket_id}",
                description=f"Created by: {interaction.user.mention}\nType: {selected_type.replace('_', ' ').title()}",
                color=discord.Color.blue()
            )
            embed.add_field(name="Status", value="Open", inline=False)
            
            # Send embed with buttons
            view = TicketView(self.bot, ticket_id, interaction.user.id, ticket_channel.id)
            await ticket_channel.send(embed=embed, view=view)
            
            await interaction.response.send_message(f"Ticket created! {ticket_channel.mention}", ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(f"Error creating ticket: {str(e)}", ephemeral=True)


class SupportDropdownView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(SupportDropdown(bot))


class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def post_support_embed(self):
        """Post the support system embed to the designated channel"""
        target_channel_id = 1504781109681193001
        
        channel = self.bot.get_channel(target_channel_id)
        if not channel:
            print(f"Support channel {target_channel_id} not found.")
            return
        
        embed = discord.Embed(
            title="Support System",
            description="Select the type of support ticket you need below.",
            color=discord.Color.blurple()
        )
        embed.add_field(
            name="How to use",
            value="1. Select a ticket type from the dropdown\n2. A support channel will be created for you\n3. Wait for support staff to assist you",
            inline=False
        )
        
        view = SupportDropdownView(self.bot)
        
        try:
            await channel.send(embed=embed, view=view)
            print("Support system embed posted successfully!")
        except Exception as e:
            print(f"Error posting support system: {str(e)}")

    @app_commands.command(name="support", description="Post the support system embed")
    @app_commands.checks.has_permissions(administrator=True)
    async def support(self, interaction: discord.Interaction):
        await self.post_support_embed()
        await interaction.response.send_message("Support system posted!", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Support(bot))
