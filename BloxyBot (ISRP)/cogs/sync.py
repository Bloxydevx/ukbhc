import discord
from discord.ext import commands
from typing import Optional, Literal

class SyncCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx):
        try:
            synced = await self.bot.tree.sync()
            sync_commands = True
            await ctx.send(f"Synced!")
        except Exception as anyname:
            await ctx.send(f"Error occurred: {anyname}")

async def setup(bot):
    await bot.add_cog(SyncCog(bot))
