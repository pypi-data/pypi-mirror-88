import discord
from discord.ext import commands
import asyncio

class Channel(Exception):
    "Channel is not provided"

class Welcome(object):
    def __init__(self, **kwargs):
        if "channel" not in kwargs:
            raise Channel("You must provide a channel id.")
        else:
            self.channel = kwargs["channel"]
    async def start(self):
        @commands.Cog.listener()
        async def on_member_join(self, member):
            if self.channel is None:
                raise Channel("Please use discordRandomStuff.Welcome(channel=channel_id) to setup Welcome.")
            else:
                channel = discord.utils.get(member.guild.channels, id=self.channel)
                embed = discord.Embed(title=f'A new Member as joined!')
                embed.add_field(name="User", value=str(member))
                embed.add_field(name="Joined at", value=member.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"))
                embed.add_field(name="Created at", value=member.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"))
                embed.set_thumbnail(url=member.avatar_url_as(format='png'))
                await channel.send(embed=embed)
        
        
        

        
        
 
    
