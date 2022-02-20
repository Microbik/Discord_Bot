import discord
from discord.ext import commands
import sqlite3
import random
import asyncio

def pref(bot, ctx):
    db = sqlite3.connect('guildspec.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT prefix FROM guildspec WHERE guild_id = {ctx.guild.id}')
    result = cursor.fetchone()
    x = str(result[0])
    return x

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

class HelpCog(commands.Cog):

    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    # SPECIAL COMMANDS NOT IDLE

    @commands.command(pass_context=True)
    async def d(self, ctx, number):
        number = int(number)
        d = random.randint(1, number)
        if number == 20 and d == 20:
            await ctx.send(d)
            await ctx.send('NOICE!')
        else:
            await ctx.send(d)

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    @cooldown(1, per_sec=60, type=commands.BucketType.user)
    async def clear(self, ctx, number):
        number = int(number)
        moreoma = ctx.author.id
        message = await ctx.send("Are you sure you want to delete " + str(number) + " messages?")

        emojis = ['✅', '❌']

        for emoji in (emojis):
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user.id == moreoma and str(reaction.emoji) in emojis

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10, check=check)
        except asyncio.TimeoutError:
            await ctx.send("timeout")
        else:
            if reaction.emoji == '✅':
                if number <= 100:
                    await ctx.channel.purge(limit=number + 2, check=lambda msg: not msg.pinned)
                elif number > 100:
                    await ctx.send('No more than 100 messages to delete allowed!')
            elif reaction.emoji == '❌':
                await ctx.send("Cancelled")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    @cooldown(1, per_sec=15, type=commands.BucketType.user)
    async def prefix(self, ctx, l=None):
        if l is None:
            db = sqlite3.connect('guildspec.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT prefix FROM guildspec WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            x = str(result[0])
            await ctx.send(f'Server prefix is {x}. Type {pref(self, ctx)}prefix [symbol] to change prefix')
        else:

            l = str(l)
            db = sqlite3.connect('guildspec.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT guild_id FROM guildspec WHERE guild_id = {ctx.guild.id}")
            if cursor.fetchone() == None:
                cursor.execute(f"INSERT INTO guildspec VALUES (?,?,?)", (ctx.guild.id, 'l', 0))
                db.commit()
            else:
                cursor.execute(f"SELECT prefix FROM guildspec WHERE guild_id = {ctx.guild.id}")
                result = cursor.fetchone()
                n = str(result[0])
                cursor.execute(f"UPDATE guildspec SET prefix = '{l}' WHERE guild_id = {ctx.guild.id}")
                db.commit()
                await ctx.send(f'Successfully changed prefix from {n} to {l}')

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    @cooldown(1, per_sec=100, type=commands.BucketType.user)
    async def adsel(self, ctx, number):
        number = str(number)
        for char in number:
            if char in " <#>":
                number = number.replace(char, '')

        number = int(number)
        db = sqlite3.connect('guildspec.sqlite')
        cursor = db.cursor()
        cursor.execute(f'UPDATE guildspec SET channel_id = {number} WHERE guild_id = {ctx.guild.id}')
        db.commit()
        channel = self.bot.get_channel(number)
        message = await channel.send('Channel selected')
        await asyncio.sleep(15)
        await message.delete()

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    @cooldown(1, per_sec=30, type=commands.BucketType.user)
    async def adsend(self, ctx, title, *, message):
        title = str(title)
        message = str(message)
        db = sqlite3.connect('guildspec.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id FROM guildspec WHERE guild_id = {ctx.guild.id}')
        result = cursor.fetchone()
        cha = int(result[0])
        if cha == 0 or None:
            await ctx.send(f'Channel was not selected. Type {pref(self, ctx)}adsel [channel_id or #channel]')
        else:
            channel = self.bot.get_channel(cha)
            em = discord.Embed(title=title, description=message, color=0x3498db)
            await channel.send(embed=em)

    @commands.command(pass_context=True)
    async def calc(self, ctx, first, par, second):
        first = int(first)
        par = str(par)
        second = int(second)
        if par == '+':
            await ctx.send(first + second)
        elif par == '-':
            await ctx.send(first - second)
        elif par == '*':
            await ctx.send(first * second)
        elif par == '/':
            try:
                await ctx.send(first / second)
            except ValueError:
                await ctx.send('ERROR, can\'t divide by zero!')
        else:
            await ctx.send('Error. Wrong parameter.')

    @commands.group(pass_context=True)
    @cooldown(1, per_sec=600, type=commands.BucketType.user)
    async def bugreport(self, ctx, *, message=None):
        if message is None:
            message = await ctx.send('No message provided.')
            await asyncio.sleep(10)
            await message.delete()
        else:

            db = sqlite3.connect('usersbug.sqlite')
            cursor = db.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usersbug(
                user_id INT,
                banned INT
                )
                ''')

            cursor.execute(f'SELECT user_id FROM usersbug WHERE user_id = {ctx.author.id}')
            if cursor.fetchone() is None:
                cursor.execute(f'INSERT INTO usersbug VALUES (?,?)', (ctx.author.id, 0))
                db.commit()

            cursor.execute(f'SELECT banned FROM usersbug WHERE user_id = {ctx.author.id}')
            result = cursor.fetchone()
            x = int(result[0])
            abobus = ctx.author.name
            abobusid = ctx.author.id
            if x == 0:
                user = self.bot.get_user(555767665986109450)
                em = discord.Embed(title=f"{abobus} ({abobusid}) writed:", description=f'{message}')
                await user.send(embed=em)
                await ctx.send('Sended a bug report message.')

            elif x == 1:
                await ctx.send('You are banned for creating a false bug report. Please, do not spam this command')

    #author commands

    @commands.group(pass_context=True)
    async def globalannounce(self, ctx, title, *, message):
        if ctx.author.id == 555767665986109450:
            db = sqlite3.connect('guildspec.sqlite')
            cursor = db.cursor()
            cursor.execute('SELECT channel_id FROM guildspec')
            for result in cursor.fetchall():
                x = int(result[0])
                channel = self.bot.get_channel(x)
                em = discord.Embed(title=f'{title}', description=f'{message}', color=0x7289da)
                await channel.send(embed=em)
        else:
            await ctx.send('ACCESS DENIED')

    @commands.group(pass_context=True)
    async def bugban(self, ctx, huyilo):
        huyilo = int(huyilo)
        if ctx.author.id == 555767665986109450:
            db = sqlite3.connect('usersbug.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT user_id, banned FROM usersbug WHERE user_id = {huyilo}')
            result = cursor.fetchone()
            if result is None:
                await ctx.send('ERROR 404: user not found')
            elif result[1] == 0:
                db = sqlite3.connect('usersbug.sqlite')
                cursor = db.cursor()
                cursor.execute(f'UPDATE usersbug SET banned = 1 WHERE user_id = {huyilo}')
                db.commit()
                await ctx.send('User banned')
            elif result[1] == 1:
                db = sqlite3.connect('usersbug.sqlite')
                cursor = db.cursor()
                cursor.execute(f'UPDATE usersbug SET banned = 0 WHERE user_id = {huyilo}')
                db.commit()
                await ctx.send('User unbanned')
        else:
            await ctx.send('ACCESS DENIED')

    @commands.group(pass_context=True)
    async def buganswer(self, ctx, huyilo, *, msg):
        huyilo = int(huyilo)
        if ctx.author.id == 555767665986109450:
            user = self.bot.get_user(huyilo)
            em = discord.Embed(title='Answer to your message', description=f'{msg}')
            try:
                await user.send(embed=em)
                await ctx.send('Message is delivered.')
            except Exception:
                await ctx.send('Error. Message is not delivered.')
        else:
            await ctx.send('ACCESS DENIED')

    # playlist commands

    @commands.group(pass_context=True)
    @cooldown(1, per_sec=200, type=commands.BucketType.user)
    async def playlistcreate(self, ctx, *, name):
        db = sqlite3.connect('playlists.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM playlists WHERE user_id = {ctx.author.id} and name = "{name}"')
        result = cursor.fetchone()
        if result is None:
            cursor.execute('INSERT INTO playlists VALUES (?,?,?,?)', (ctx.author.id, name, '', 0))
            db.commit()
            await ctx.send(f'Playlist \"{name}\" created.')
        else:
            await ctx.send(f'Playlist \"{name}\" already exist.')

    @commands.group(pass_context=True)
    @cooldown(1, per_sec=100, type=commands.BucketType.user)
    async def playlistdelete(self, ctx, *, name):
        db = sqlite3.connect('playlists.sqlite')
        cursor = db.cursor()
        cursor.execute(f'DELETE FROM playlists WHERE name = "{name}" and user_id = {ctx.author.id}')
        db.commit()
        await ctx.send(f'Your existing playlist with name: \"{name}\" has been deleted.')

    @commands.group(pass_context=True)
    @cooldown(1, per_sec=20, type=commands.BucketType.user)
    async def playlistselect(self, ctx, *, name):
        db = sqlite3.connect('playlists.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT selected FROM playlists WHERE user_id = {ctx.author.id} and name = "{name}"')
        result = cursor.fetchone()
        if result is None:
            await ctx.send(f'Failed to find playlist with name: "{name}".')
        elif result[0] == 1:
            await ctx.send('Already selected this playlist.')
        elif result[0] == 0:
            cursor.execute(f'UPDATE playlists SET selected = 0 WHERE user_id = {ctx.author.id}')
            db.commit()
            cursor.execute(
                f'UPDATE playlists SET selected = 1 WHERE user_id = {ctx.author.id} and name = "{name}"')
            db.commit()
            await ctx.send(f'Selected playlist "{name}".')

    @commands.group(pass_context=True)
    @cooldown(1, per_sec=10, type=commands.BucketType.user)
    async def playlistadd(self, ctx, *, song):
        song = str(song)
        db = sqlite3.connect('playlists.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT name FROM playlists WHERE user_id = {ctx.author.id} and selected = 1')
        result = cursor.fetchone()
        if result is None:
            await ctx.send('No playlists has been selected.')
        else:
            name = result[0]
            cursor.execute(f'SELECT songs FROM playlists WHERE user_id = {ctx.author.id} and selected = 1')
            result0 = cursor.fetchone()
            songs = str(result0[0])
            newlist = songs + song + "|"
            cursor.execute(
                f'UPDATE playlists SET songs = "{newlist}" WHERE user_id = {ctx.author.id} and selected = 1')
            db.commit()
            await ctx.send(f'Added a song "{song}" to a "{name}" playlist.')

    @commands.group(pass_context=True)
    @cooldown(1, per_sec=10, type=commands.BucketType.user)
    async def playlist(self, ctx, *, name):
        db = sqlite3.connect('playlists.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT songs FROM playlists WHERE user_id = {ctx.author.id} and name = "{name}"')
        result = cursor.fetchone()
        if result is None:
            await ctx.send('This playlist does not exist')
        else:
            songs = str(result[0])
            em = discord.Embed(title=f"Playlist '{name}'", description=songs.replace("|", "\n"))
            await ctx.send(embed=em)

    @commands.group(pass_context=True)
    @cooldown(1, per_sec=10, type=commands.BucketType.user)
    async def playlists(self, ctx):
        member = ctx.author
        db = sqlite3.connect('playlists.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT name FROM playlists WHERE user_id = {ctx.author.id}')
        list = cursor.fetchall()
        result = ''
        for i in list:
            result = result + str(i[0]) + "\n"
        if result == '':
            await ctx.send('You haven\'t got any playlist yet.')
        else:
            em = discord.Embed(title=f'Playlists of {member.name}', description=result)
            await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(HelpCog(bot))
    print('Not stardust commands is loaded')