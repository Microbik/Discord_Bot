import discord
from discord.ext import commands

class HelpCog(commands.Cog):

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title='Stardust Help', description='Use help [command] for extented information.', color=0x7289da)
        em.add_field(name='Commands', value='hello; info; mine; upgrade; ascend; rankup; transit; redeem; annigilate; leaderboard; rating; rolerankcreate; rolerankdelete; shop; buy; shopadd; shopdelete \n \nprefix; d; clear; calc; adsel; adsend; bugreport \n \nplaylist; playlists; playlistcreate; playlistdelete; playlistselect; playlistadd')
        await ctx.send(embed=em)

    @help.command()
    async def hello(self, ctx):
        em = discord.Embed(title='Hello', description='A simple explanation of bot functions')
        await ctx.send(embed=em)

    @help.command()
    async def info(self, ctx):
        em = discord.Embed(title='Info', description='Your resourses and money are there. Use buttons or other commands below to navigate through your inventory.')
        await ctx.send(embed=em)

    @help.command()
    async def mine(self, ctx):
        em = discord.Embed(title='Mine', description="Type for mine some stardust. Each drill has it's own cooldown on this command. Each drill level has its own diapasone of random min-max numbers")
        await ctx.send(embed=em)

    @help.command()
    async def upgrade(self, ctx):
        em = discord.Embed(title='Upgrade', description="Upgrade your drill level. If you ascend, your level will not go on next drill.")
        await ctx.send(embed=em)

    @help.command()
    async def ascend(self, ctx):
        em = discord.Embed(title='Upgrade', description="Ascend your drill to a new one. level will be reset to 1.")
        await ctx.send(embed=em)

    @help.command()
    async def transit(self, ctx):
        em = discord.Embed(title='Transit', description="Give your money to someone (transit [@user] [amount])")
        await ctx.send(embed=em)

    @help.command()
    async def d(self, ctx):
        em = discord.Embed(title='Dice', description="d [number] for random from 1 to [number]")
        await ctx.send(embed=em)

    @help.command()
    async def clear(self, ctx):
        em = discord.Embed(title='Clear', description="clear [number] to clear chat")
        await ctx.send(embed=em)

    @help.command()
    async def annigilate(self, ctx):
        em = discord.Embed(title='ANNIGILATION', description="deletes your stardust progress from this server")
        await ctx.send(embed=em)

    @help.command()
    async def calc(self, ctx):
        em = discord.Embed(title='Calculator', description="calculate [number] [+ or - or * or /] [number]")
        await ctx.send(embed=em)

    @help.command()
    async def prefix(self, ctx):
        em = discord.Embed(title='Prefix', description="sets your server prefix (prefix (symbol)) ")
        await ctx.send(embed=em)

    @help.command()
    async def adsel(self, ctx):
        em = discord.Embed(title='Advert channel selection', description="Select an advert/announce channel (adsel [channel_id or #channel]")
        await ctx.send(embed=em)

    @help.command()
    async def adsend(self, ctx):
        em = discord.Embed(title='Advert send', description="Send an announce to the advert channel (adsend [1 word for title] [other words for message]")
        await ctx.send(embed=em)

    @help.command()
    async def bugreport(self, ctx):
        em = discord.Embed(title='Bug report', description="Send to a bot author message (bugreport [message]). It can contain info about bug. DO NOT spam this command. Only bug info or suggestion about bot functions can be provided. You will be banned from this command if you will not follow this rules. Bot (author) also may answer on your bug report.")
        await ctx.send(embed=em)

    @help.command()
    async def leaderboard(self, ctx):
        em = discord.Embed(title='Leaderboard', description="Shows top 10 richest users on this server.")
        await ctx.send(embed=em)

    @help.command()
    async def rankup(self, ctx):
        em = discord.Embed(title='Rank up', description="Upgrade your rank. Every 5 levels you will get a new role, if admin creates them via rolerankcreate command.")
        await ctx.send(embed=em)

    @help.command()
    async def rolerankcreate(self, ctx):
        em = discord.Embed(title='Create a bot roles', description="Create roles, that gives to user every 5 level. If roles is exists, they will be pinged in info. On this command also roles will be given. To delete roles, please use rolerankdelete command. Roles will be given to the users, which roles a lower, than a bot role.")
        await ctx.send(embed=em)

    @help.command()
    async def rolerankdelete(self, ctx):
        em = discord.Embed(title='Deletes all bot roles', description='Deletes custom bot roles if they exists.')
        await ctx.send(embed=em)

    @help.command()
    async def playlist(self, ctx):
        em = discord.Embed(title='Playlist', description='Get your playlist to copy (playlist [name]).')
        await ctx.send(embed=em)

    @help.command()
    async def playlists(self, ctx):
        em = discord.Embed(title='Playlist', description='See which playlists do you have.')
        await ctx.send(embed=em)

    @help.command()
    async def playlistcreate(self, ctx):
        em = discord.Embed(title='Playlist create', description='Create your playlist (playlistcreate [name]). You can\'t have playlists with the same names.')
        await ctx.send(embed=em)

    @help.command()
    async def playlistdelete(self, ctx):
        em = discord.Embed(title='Playlist delete', description='Deletes playlist (playlistdelete [name]).')
        await ctx.send(embed=em)

    @help.command()
    async def playlistselect(self, ctx):
        em = discord.Embed(title='Playlist selection', description='Select playlist to add a song. Only one playlist can be selected at the same time (playlistselect [name]).')
        await ctx.send(embed=em)

    @help.command()
    async def playlistadd(self, ctx):
        em = discord.Embed(title='Playlist add', description='Adds a song to a currently selected playlist (playlistadd [any text]).')
        await ctx.send(embed=em)

    @help.command()
    async def redeem(self, ctx):
        em = discord.Embed(title='Redeem', description='Redeem a wild code! (redeem [code in low reg.]).')
        await ctx.send(embed=em)

    @help.command()
    async def shop(self, ctx):
        em = discord.Embed(title='Shop', description='Displays a server shop.')
        await ctx.send(embed=em)

    @help.command()
    async def buy(self, ctx):
        em = discord.Embed(title='Buy', description='Buy an item (buy [item]).')
        await ctx.send(embed=em)

    @help.command()
    async def shopadd(self, ctx):
        em = discord.Embed(title='Shop add item', description='Adds an item to the shop (shopadd [cost] [name]). Bot will message to the user, who add this item if someone bought it! Make sure bot can msg you!')
        await ctx.send(embed=em)

    @help.command()
    async def shopdelete(self, ctx):
        em = discord.Embed(title='Shop delete item', description='Deletes an item in the shop (shopdelete [name]).')
        await ctx.send(embed=em)

    @help.command()
    async def rating(self, ctx):
        em = discord.Embed(title='Your rating', description='Your personal rating on this server.')
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(HelpCog(bot))
    print('Help is loaded')