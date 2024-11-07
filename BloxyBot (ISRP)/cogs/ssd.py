import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button



class ssd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="ssd", description="Server shutdown")
    @app_commands.guild_only()
    async def ssu(self, interaction: discord.Interaction):
        roleid = 1192187168957931647
        role = discord.utils.get(interaction.guild.roles, id=roleid)
        if role in interaction.user.roles:
            await interaction.response.send_message("<:ServerOnline:1217225035895275572> **Successfully** ran command.", ephemeral=True)
            channel = self.bot.get_channel(1192187169385762911)
            embed = discord.Embed(title="Server Shutdown", description="Our session has came to an end, we thank those who participated within our session and hope to see you again next time.", color=0x2b2d31)
            embed.set_author(name=f"@{interaction.user}", icon_url=interaction.user.display_avatar.url)
            await channel.send(embed=embed)
        else:
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ssd(bot))
