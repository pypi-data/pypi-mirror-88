This is discordRandomStuff it can be a startup for you discord bot or a fun thing for it.


Welcome example
```
Not in cogs

from discordRandomStuff.welcome import Welcome
from discord.ext import commands
prefix  = "t!"
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_member_join(self, member):
    Welcome(channel=735826080153337898) #Replace those numbers a channel id
    Welcome.start() #This will start it
    print("DRS welcome module is loaded") #If this shows up in your conosle logs, that means it is loaded


In cogs

from discordRandomStuff.welcome import Welcome
from discord.ext import commands
class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()  # Event module
    async def on_member_join(self, member):  # defining it
        Welcome(channel=735826080153337898) #Replace those numbers a channel id
        Welcome.start() #This will start it
        print("DRS welcome module is loaded") #If this shows up in your conosle logs, that means it is loaded
        
def setup(bot):
    bot.add_cog(Welcome(bot))


