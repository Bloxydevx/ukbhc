import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from main import votes

class QuickJoinButton(Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.grey, label='Quick Join', url="https://policeroleplay.community/join/ISSRP")

class QuickJoinView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(QuickJoinButton()) 

class ssu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ssu", description="Server Start Up")
    @app_commands.guild_only()
    async def ssu(self, interaction: discord.Interaction):
        mention_list = "No voters"  # Default value
        if votes: 
            mention_list = " ".join(f"<@{user_id}>" for user_id, _ in votes)
            
        roleid = 1192187168957931647
        role = discord.utils.get(interaction.guild.roles, id=roleid)
        if role in interaction.user.roles:
            await interaction.response.send_message("<:ServerOnline:1217225035895275572> **Successfully** ran command.", ephemeral=True)
            channel = self.bot.get_channel(1192187169385762911)
            embed = discord.Embed(title="Server Start Up", description="We have hosted a server start up. Join for an immersive experience in our top-notch roleplay.\n\n> **Server Name:** Illinois State Roleplay I Strict I Realistic\n> **Server Code:** ISSRP\n> **Server Owner:** OnlyIfItsMilk", color=0x2b2d31)
            embed.set_author(name=f"@{interaction.user}", icon_url=interaction.user.display_avatar.url)
            await channel.send(f"<@&1193380116030562334> | {mention_list}", embed=embed, view=QuickJoinView())
            votes.clear()
        else:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ssu(bot))
