import asyncio
import logging
import sys
import time
import aiohttp
import requests
sys.dont_write_bytecode = True
import os
import discord
from cogwatch import watch
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
APIKEY = os.getenv('APIKEY')

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

votes = []

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="-", owner_ids=[938899833866059788, ], intents=intents)


    @watch(path='cogs', preload=True, default_logger=True)
    async def on_ready(self):
        print("Bot is online.")
        await bot.load_extension('jishaku')
        await bot.tree.sync(guild=discord.Object(id=1192187168907591701))
        await bot.loop.create_task(auto_update())
  
        
bot = Bot()
bot.remove_command("help")

start_time = time.time()

@bot.command(name='ping')
async def ping(ctx):
        fetching = await ctx.reply("Fetching latency...", mention_author=True)
        uptime = round(time.time() - start_time)
        uptime_timestamp = f"<t:{int(start_time)}:R>"
        embed=discord.Embed(title="Pong!", description=f"> **Uptime:** {uptime_timestamp} \n> **Latency:** {round(bot.latency * 1000)}ms", color=0x2b2d31)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1028686053218980001/1128758659074228224/New_Project_3.png?ex=6620186b&is=660da36b&hm=89e7693c6af8ef095e08c18b28ca7b21c6666413f25781f1f283e1498ec6c3f9&")
        await fetching.edit(content=None, embed=embed) 


@bot.event
async def on_member_join(member):
    if member.guild.id == 1038623685138980954:
        channel = bot.get_channel(1200877367858561124)
        if channel:
            await channel.send(f"👋 | **Welcome** {member.mention} **to** **Illinois State Roleplay**! **We now have a total of** {member.guild.member_count} **members!**")


@bot.command(name="say")
@commands.is_owner()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)


async def auto_update():
    while True:
        try:
            guild_id = 1192187168907591701  
            role_id = 1192187168945340498   
            channel_id = 1192187169385762911  
            message_id = 1234672077634539540 

            guild = bot.get_guild(guild_id)
            if guild:
                role = guild.get_role(role_id)
                if role:
                    members_with_role = sum(1 for member in guild.members if role in member.roles)

                    channel = bot.get_channel(channel_id)
                    if channel:
                        message = await channel.fetch_message(message_id)
                        if message:
                            await update_message(message, members_with_role)
        except Exception as e:
            print(f"An error occurred: {e}")

        await asyncio.sleep(20) 


async def update_message(message, members_with_role):
    headers = {
        'Content-Type': 'application/json',
        'Server-Key': APIKEY  
    }
    api_url = 'https://api.policeroleplay.community/v1/server'
    
    retry_count = 0
    max_retries = 5
    backoff_delay = 1  

    while retry_count < max_retries:
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  
            data = response.json()
            current_players = data.get('CurrentPlayers')
            if current_players is None:
                return 
            

            queue_count = await get_queue_count()
            if queue_count is None:
                print("Failed to fetch queue count.")
                return
            

            break
        except requests.HTTPError as http_err:
            if response.status_code == 429:  
                backoff_delay *= 2  
                await asyncio.sleep(backoff_delay)
                retry_count += 1
                continue

    if retry_count == max_retries:
        return 

    
    embed = discord.Embed(description=f"**Server Status**\n Welcome to the server status, here you can see our live player count real time that updates every 20 seconds.\n\n**Playercount:** {current_players}/40\n\n**Staff Online:** {members_with_role}\n\n**Queue Count:** {queue_count}\n\n*Last updated:* <t:{int(time.time())}:R>\n", color=0x2b2d31)

    await message.edit(content=None, embed=embed)


async def get_queue_count():
    headers = {
        'Content-Type': 'application/json',
        'Server-Key': APIKEY  
    }
    api_url = 'https://api.policeroleplay.community/v1/server/queue'
    
    retry_count = 0
    max_retries = 5
    backoff_delay = 1  

    while retry_count < max_retries:
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()  
            data = response.json()
            
            if isinstance(data, list):
                queue_count = len(data)
                return queue_count
            else:
                return 0

        except requests.HTTPError as http_err:
            if response.status_code == 429:  
                backoff_delay *= 2  
                await asyncio.sleep(backoff_delay)  
                retry_count += 1
                continue

        except Exception as e:
            return 0  
        
    if retry_count == max_retries:
        return 0  


if __name__ == '__main__':
    bot.run(TOKEN)