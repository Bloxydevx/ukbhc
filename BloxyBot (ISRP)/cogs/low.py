import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button


class QuickJoinButton(Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.grey, label='Quick Join', url="https://policeroleplay.community/join/ISSRP")

class QuickJoinView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(QuickJoinButton()) 



class low(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="low", description="Announce low players.")
    @app_commands.guild_only()
    async def ssu(self, interaction: discord.Interaction):
        roleid = 1192187168957931647
        role = discord.utils.get(interaction.guild.roles, id=roleid)
        if role in interaction.user.roles:
            await interaction.response.send_message("<:ServerOnline:1217225035895275572> **Successfully** ran command.", ephemeral=True)
            channel = self.bot.get_channel(1192187169385762911)
            embed = discord.Embed(title="Low Players", description="Our in-game server has dropped in players, please join for an immersive experience in our top-notch roleplay.", color=0x2b2d31)
            embed.set_author(name=f"@{interaction.user}", icon_url=interaction.user.display_avatar.url)
            await channel.send("@here", embed=embed, view=QuickJoinView())
        else:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(low(bot))
