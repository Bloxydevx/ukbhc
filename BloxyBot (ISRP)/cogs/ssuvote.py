import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord import app_commands

class VotingButton(discord.ui.View):
    def __init__(self, max_votes: int):
        super().__init__(timeout=None)
        self.max_votes = max_votes  

    @discord.ui.button(label="Vote", disabled=False)  
    async def vote_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        global votes
        if len(votes) >= self.max_votes:  
            await interaction.response.send_message("Voting has ended!", ephemeral=True)
            return

        user = interaction.user
        user_id = user.id

        if (user_id, user.name) in votes:  
            votes.remove((user_id, user.name))  
            embed = discord.Embed(description=f'Your session vote has been removed.', color=0x2b2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            votes.append((user_id, user.name))  
            embed = discord.Embed(description=f'Your session vote has been added.', color=0x2b2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        if len(votes) >= self.max_votes: 
            button.disabled = True
            await interaction.message.edit(view=self) 
        
        self.value = f"Vote [{len(votes)}/{self.max_votes}]"
        button.label = self.value
        await interaction.message.edit(view=self)  

    @discord.ui.button(label="View Votes", style=discord.ButtonStyle.blurple)
    async def view_votes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if votes:  
            vote_list = "\n".join(f"<@{user_id}> ({user_id})" for user_id, username in votes)
            embed = discord.Embed(title="Session Votes", description=f"These are the list of people who have voted for the session. Note that you are able to remove your vote by clicking the vote button again.\n\n{vote_list}", color=0x2b2d31)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("No votes have been cast yet.", ephemeral=True)
    
    def update_vote_button_label(self):
        votes_count = len(self.children[0].custom_id)  # Access the number of votes from the first button's custom ID
        self.children[0].label = f"Vote ({votes_count})" 

class SessionVote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.SSUCHANNEL = 1192187169385762911

    @app_commands.command(name="ssuvote", description="Start a session vote.")
    @app_commands.guilds(discord.Object(id=1192187168907591701))
    async def vote_callback(self, interaction: discord.Interaction, max_votes: int):
        roleid = 1192187168957931647
        role = discord.utils.get(interaction.guild.roles, id=roleid)
        if role in interaction.user.roles:
            global votes
            from main import votes

            view = VotingButton(max_votes=max_votes)
            embed = discord.Embed(title="Session Vote", description=f"Management has decided to host a session vote. We are required to have {max_votes}+ votes in order to Start Up the server\n\nIf you vote yes, you are required to join. Failure to do so will result in moderation.", color=0x2b2d31)
            embed.set_author(name=f"@{interaction.user}", icon_url=interaction.user.display_avatar.url)
            ssuchannel = discord.utils.get(interaction.guild.channels, id=self.SSUCHANNEL) 
            await interaction.response.send_message("<:ServerOnline:1217225035895275572> **Successfully** ran command.", ephemeral=True)
            await ssuchannel.send("<@&1193380116030562334>", embed=embed, view=view)

        else:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SessionVote(bot))
