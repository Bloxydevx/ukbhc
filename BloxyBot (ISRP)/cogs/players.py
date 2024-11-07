import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp
from discord.ext import commands
import discord

class apicmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.APIKEY = os.getenv('APIKEY')




    @commands.command()
    async def players(self, ctx, callsign=None):
        loading_message = await ctx.send("Loading...")

        headers = {
            'Server-Key': self.APIKEY,
            'Content-Type': 'application/json'
        }

        url = 'https://api.policeroleplay.community/v1/server/players'

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
            except aiohttp.ClientResponseError as err:
                if response.status == 429:
                    await loading_message.edit(content="Too many requests. Retry this command later.")
                    return
                else:
                    await loading_message.edit(content="Failed to fetch data from the API.")
                    return

        player_count = len(data)
        server_staff = []
        players = []

        guild = ctx.guild
        discord_nicknames = {member.display_name for member in guild.members}

        async def process_player_info(player_info):
            player_name, player_id = player_info["Player"].split(":")
            roblox_username = player_name
            roblox_id = player_id
            team = player_info["Team"]
            permission = player_info["Permission"]
            player_callsign = player_info.get("Callsign")

            profile_url = f"https://www.roblox.com/users/{roblox_id}/profile"

            roblox_in_discord = any(roblox_username.lower() in nickname.lower() for nickname in discord_nicknames)

            if callsign and player_callsign:
                if callsign.lower() == player_callsign.lower():
                    if roblox_in_discord:
                        if "Normal" in permission:
                            players.append(f"[{roblox_username}]({profile_url}) - {team} (`{player_callsign}`)\n")
                        else:
                            server_staff.append(f"[{roblox_username}]({profile_url}) - {team} (`{player_callsign}`)\n")
                    else:
                        if "Normal" in permission:
                            players.append(f"[{roblox_username}]({profile_url}) - {team} (`{player_callsign}`) <:ServerShutdown:1217225089519583262>\n")
                        else:
                            server_staff.append(f"[{roblox_username}]({profile_url}) - {team} (`{player_callsign}`)\n")
            elif not callsign:
                if roblox_in_discord:
                    if "Normal" in permission:
                        players.append(f"[{roblox_username}]({profile_url}) - {team} (`{player_callsign}`)\n")
                    else:
                        server_staff.append(f"[{roblox_username}]({profile_url}) - {team} (`{player_callsign}`)\n")
                else:
                    if "Normal" in permission:
                        players.append(f"[{roblox_username}]({profile_url}) - {team} (`{player_callsign}`) <:ServerShutdown:1217225089519583262>\n")
                    else:
                        server_staff.append(f"[{roblox_username}]({profile_url}) - {team} (`{player_callsign}`)\n")

        await asyncio.gather(*[process_player_info(player_info) for player_info in data])

        embed = discord.Embed(title=f"In-game Players [{player_count}]", color=0x2b2d31)

        if server_staff:
            embed.description = "**Server Staff:**\n" + ''.join(server_staff)

        if players:
            if server_staff:
                embed.description += "\n**Players:**\n" + ''.join(players)
            else:
                embed.description = "**Players:**\n" + ''.join(players)

        await loading_message.edit(content="", embed=embed)
            
    @staticmethod
    async def get_roblox_id(username):
        api_url = f'https://api.newstargeted.com/roblox/users/v2/user.php?username={username}'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(api_url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data.get('userId')
            except Exception as e:
                print(f"Error fetching Roblox ID for {username}:", e)
                return None


async def setup(bot):
    await bot.add_cog(apicmds(bot))