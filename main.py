import discord
from discord.ext import commands
from info import settings
import sqlite3
import sys
import traceback
import random
import asyncio
import math
from discord_components import DiscordComponents

version = 'Beta 0.9.1.1 (Closed beta)'

def pref(bot, ctx):
    db = sqlite3.connect('guildspec.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT prefix FROM guildspec WHERE guild_id = {ctx.guild.id}')
    result = cursor.fetchone()
    x = str(result[0])
    return x

bot = commands.Bot(command_prefix = pref, intents=discord.Intents.all())
bot.remove_command('help')

def cooldown(rate, per_sec=0, per_min=0, per_hour=0, type=commands.BucketType.default):
    return commands.cooldown(rate, per_sec + 60 * per_min + 3600 * per_hour, type)

drills = {
1: 'Rusty Drill',
2: 'Iron Drill',
3: 'Tungsten Drill',
4: 'Steel Drill',
5: 'Dark Steel Drill',
6: 'Crystal Drill',
7: 'Red Quartz Drill',
8: 'Diamond Drill',
9: 'Adamantine Drill',
10: 'Titan Drill'
}

drillpic = {
1: 'https://i.imgur.com/0BHZPai.png',
2: 'https://i.imgur.com/OAZNBKT.png',
3: 'https://i.imgur.com/DOsxf3k.png',
4: 'https://i.imgur.com/ts7a9M7.png',
5: 'https://i.imgur.com/XvFfdLR.png',
6: 'https://i.imgur.com/qFosfe2.png',
7: 'https://i.imgur.com/es6uXyq.png',
8: 'https://i.imgur.com/T13DLef.png',
9: 'https://i.imgur.com/gBg1tOp.png',
10: 'https://i.imgur.com/fpjNcKC.png'
}

roles = {
1: ['[1-5] Copper ranks', 0xEB522C],
2: ['[6-10] Iron ranks', 0x55403B],
3: ['[11-15] Tungsten ranks', 0x026B0D],
4: ['[16-20] Silver ranks', 0x96A297],
5: ['[21-25] Golden ranks', 0xFFD700],
6: ['[26-30] Platinum ranks', 0xE5E4E2],
7: ['[31-35] Diamond ranks', 0x0DF2DE],
8: ['[36-40] Titanium ranks', 0xB5DBD8],
9: ['[41-45] Orichalcum ranks', 0x9AE63E],
10: ['[46-50] Adamantine ranks', 0xE54D3B]
}

def ratemoney(ctx):
    number = 1
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT user_id, starcount FROM stardust WHERE guild_id = {ctx.guild.id} ORDER BY starcount DESC')
    tupleList = cursor.fetchall()
    for element in tupleList:
        dibil = element[0]
        if dibil != ctx.author.id:
            number += 1
            continue
        else:
            return number

def raterank(ctx):
    number = 1
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT user_id, level FROM stardust WHERE guild_id = {ctx.guild.id} ORDER BY level DESC')
    tupleList = cursor.fetchall()
    for element in tupleList:
        dibil = element[0]
        if dibil != ctx.author.id:
            number += 1
            continue
        else:
            return number

def frs(ctx):
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT pickaxe FROM stardust WHERE user_id ={ctx.author.id} and guild_id = {ctx.author.guild.id}")
    level = cursor.fetchone()
    l = int(level[0])
    cursor.execute(f"SELECT drillname FROM stardust WHERE user_id ={ctx.author.id} and guild_id = {ctx.author.guild.id} ")
    result = cursor.fetchone()
    pick = int(result[0])
    db = sqlite3.connect('pickaxelevel.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT min FROM pickaxelevel WHERE level = {l} and name = {pick}")
    result = cursor.fetchone()
    frs = int(result[0])
    return frs

def lst(ctx):
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT pickaxe FROM stardust WHERE user_id ={ctx.author.id} and guild_id = {ctx.author.guild.id}")
    level = cursor.fetchone()
    l = int(level[0])
    cursor.execute(f"SELECT drillname FROM stardust WHERE user_id ={ctx.author.id} and guild_id = {ctx.author.guild.id} ")
    result = cursor.fetchone()
    pick = int(result[0])
    db = sqlite3.connect('pickaxelevel.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT max FROM pickaxelevel WHERE level = {l} and name = {pick}")
    result = cursor.fetchone()
    lst = int(result[0])
    return lst

def cd(ctx):
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT pickaxe FROM stardust WHERE user_id ={ctx.author.id} and guild_id = {ctx.author.guild.id}")
    level = cursor.fetchone()
    l = int(level[0])
    cursor.execute(f"SELECT drillname FROM stardust WHERE user_id ={ctx.author.id} and guild_id = {ctx.author.guild.id} ")
    result = cursor.fetchone()
    pick = int(result[0])
    db = sqlite3.connect('pickaxelevel.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT cooldown FROM pickaxelevel WHERE level = {l} and name = {pick}")
    result = cursor.fetchone()
    cd = int(result[0])
    return cd

@bot.event
async def on_ready():
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stardust(
        guild_id INT,
        user_id INT,
        starcount INT,
        pickaxe INT,
        drillname INT,
        x INT,
        level INT,
        exp INT,
        y INT
        )
        ''')

    for guild in bot.guilds:
        for member in guild.members:
            if not member.bot:
                cursor.execute(f"SELECT user_id, guild_id FROM stardust where user_id ={member.id} and guild_id = {member.guild.id}")
                if cursor.fetchone() == None:  # Если не существует
                    cursor.execute(f"INSERT INTO stardust VALUES (?,?,?,?,?,?,?,?,?)", (member.guild.id, member.id, 0, 1, 1, 1, 1, 0, 1))
                else:
                    cursor.execute (f'UPDATE stardust SET x = 1, y = 1')
                db.commit()

    db = sqlite3.connect('guildspec.sqlite')
    cursor = db.cursor()
    cursor.execute('''
           CREATE TABLE IF NOT EXISTS guildspec(
           guild_id INT,
           prefix TEXT,
           channel_id INT
           )
           ''')
    for guild in bot.guilds:
        cursor.execute(f"SELECT guild_id FROM guildspec WHERE guild_id = {guild.id}")
        if cursor.fetchone() == None:
            cursor.execute(f"INSERT INTO guildspec VALUES (?,?,?)", (guild.id, 'l', 0))
        else:
            pass
        db.commit()

    activity = discord.Game(name=f"lhelp")
    await bot.change_presence(activity=activity)

    DiscordComponents(bot)

    print("Bot is ready")

initial_extensions=['cogs.help', 'cogs.notstdcom']

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}", file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_member_join(member):
    if not member.bot:
        db = sqlite3.connect('stardust.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id, guild_id FROM stardust WHERE user_id ={member.id} and guild_id = {member.guild.id}")
        if cursor.fetchone() == None:
            cursor.execute(f"INSERT INTO stardust VALUES (?,?,?,?,?,?,?,?,?)", (member.guild.id, member.id, 0, 1, 1, 1, 1, 0, 1))
            db.commit()
        else:
            pass
        db.commit()
        print('user joined')
    else:
        print('Bot has joined')

@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            em = discord.Embed(title='Stardust', description='Hello. I am StarDust Bot, ready to mine!. Type lhelp, lhello for more info. You can also change prefix(lprefix [symbol]) in any time. Create custom bot roles with lrolerankcreate.', color=0x7289da)
            try:
                await channel.send(embed=em)
                break
            except Exception:
                continue

    db = sqlite3.connect('guildspec.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT guild_id FROM guildspec WHERE guild_id = {guild.id}")
    if cursor.fetchone() == None:
        cursor.execute(f"INSERT INTO guildspec VALUES (?,?,?)", (guild.id, 'l', 0))
    else:
        pass
    db.commit()

    for guild in bot.guilds:
        for member in guild.members:
            if not member.bot:
                db = sqlite3.connect('stardust.sqlite')
                cursor = db.cursor()
                cursor.execute(f"SELECT user_id, guild_id FROM stardust where user_id = {member.id} and guild_id = {member.guild.id}")
                if cursor.fetchone() == None:  # Если не существует
                    cursor.execute(f"INSERT INTO stardust VALUES (?,?,?,?,?,?,?,?,?)", (member.guild.id, member.id, 0, 1, 1, 1, 1, 0, 1))
                else:
                    pass
                db.commit()

    print('joined a server')

@bot.event
async def on_member_remove(member):
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f'DELETE FROM stardust WHERE user_id = {member.id} and guild_id = {member.guild.id}')
    db.commit()
    print('user deleted')

@bot.event
async def on_bot_remove(guild):
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f'DELETE FROM stardust WHERE guild_id = {guild.id}')
    db.commit()
    db = sqlite3.connect('guildspec.sqlite')
    cursor = db.cursor()
    cursor.execute(f'DELETE FROM guildspec WHERE guild_id = {guild.id}')
    db.commit()
    print('guild deleted')

@bot.event
async def on_guild_remove(guild):
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f'DELETE FROM stardust WHERE guild_id = {guild.id}')
    db.commit()
    db = sqlite3.connect('guildspec.sqlite')
    cursor = db.cursor()
    cursor.execute(f'DELETE FROM guildspec WHERE guild_id = {guild.id}')
    db.commit()
    print('guild deleted')

@bot.event
async def on_message(ctx):
    if not ctx.author.bot:
        randcode = random.randint(1, 200)
        money = random.randint(10, 5000)

        if randcode == 1:
            await bot.process_commands(ctx)
            code_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            code = ''
            for i in range(0, 6):
                slice_start = random.randint(0, len(code_chars) - 1)
                code += code_chars[slice_start: slice_start + 1]
            realcode = str(code.lower())

            db = sqlite3.connect('promocode.sqlite')
            cursor = db.cursor()
            cursor.execute(f'INSERT INTO promocode VALUES (?,?,?)', (ctx.guild.id, money, realcode))
            db.commit()

            channel = discord.utils.get(bot.get_all_channels(), id=ctx.channel.id)
            em = discord.Embed(title='The stars are falling', description=f'Quick, use ({pref(bot, ctx)}redeem [code in lowercase]) to collect {money}✨. They will vanish soon if nobody will pick them up!\n\n||{code}||', color=0xfeeb49)
            em.set_thumbnail(url='https://starchild.gsfc.nasa.gov/Images/StarChild/solar_system_level2/1966_leonids_small.gif')

            message = await channel.send(embed=em)
            await asyncio.sleep(45)
            await message.delete()

            try:
                db = sqlite3.connect('promocode.sqlite')
                cursor = db.cursor()
                cursor.execute(f'DELETE FROM promocode WHERE guild_id = {ctx.guild.id} and code = "{realcode}"')
                db.commit()
                em = discord.Embed(title='The stars are falling', description=f'The stars are faded away...', color=0xfeeb49)
                msg = await channel.send(embed=em)
                await asyncio.sleep(10)
                await msg.delete()
            except Exception:
                pass

        db = sqlite3.connect('stardust.sqlite')
        cursor = db.cursor()

        cursor.execute(f"SELECT user_id, guild_id FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
        if cursor.fetchone() is None:
            print(f'{ctx.author.id} - user is not in database')
        else:
            cursor.execute(f"SELECT y FROM stardust WHERE user_id ={ctx.author.id} and guild_id = {ctx.guild.id}")
            resy = cursor.fetchone()
            y = int(resy[0])
            if y == 1:
                given = random.randint(1, 5)
                cursor.execute(f'SELECT level, exp FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}')
                result = cursor.fetchone()
                level = int(result[0])
                exp = int(result[1])
                db = sqlite3.connect('level.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT maxexp FROM level WHERE level = {level}')
                result1 = cursor.fetchone()
                maxexp = int(result1[0])
                db = sqlite3.connect('stardust.sqlite')
                cursor = db.cursor()
                if exp + given < maxexp:
                    cursor.execute(f'UPDATE stardust SET exp = exp + {given}, y = 0 WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}')
                    db.commit()
                    await bot.process_commands(ctx)
                    await asyncio.sleep(30)
                    cursor.execute(f'UPDATE stardust SET y = 1 WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}')
                    db.commit()
                elif exp + given > maxexp:
                    cursor.execute(f'UPDATE stardust SET exp = {maxexp}, y = 0 WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}')
                    db.commit()
                    cursor.execute(f'UPDATE stardust SET y = 1 WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}')
                    db.commit()
                    await bot.process_commands(ctx)
                    await asyncio.sleep(30)
                elif exp + given == maxexp:
                    await bot.process_commands(ctx)
            elif y == 0:
                await bot.process_commands(ctx)
    else:
        pass

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        x = int("%.0f" % error.retry_after)
        m = x // 60
        s = x - m * 60
        await ctx.message.delete()
        em = discord.Embed(title='Stardust.exe is not answering', description=f'**Still on cooldown**, please try again after {m} minutes and {s} seconds.', color=0x7289da)
        message = await ctx.send(embed=em)
        await asyncio.sleep(6)
        await message.delete()
    elif isinstance(error, commands.MissingPermissions):
        ctx.command.reset_cooldown(ctx)
        await ctx.message.delete()
        em = discord.Embed(title='Stardust.exe is not answering', description='You have not enough permissions to do that!', color=0x7289da)
        message = await ctx.send(embed=em)
        await asyncio.sleep(6)
        await message.delete()
    elif isinstance(error, commands.MissingRequiredArgument):
        ctx.command.reset_cooldown(ctx)
        await ctx.message.delete()
        em = discord.Embed(title='Stardust.exe is not answering', description='No or wrong arguments were given. Check the arguments with help command.', color=0x7289da)
        message = await ctx.send(embed=em)
        await asyncio.sleep(6)
        await message.delete()
    elif isinstance(error, commands.BadArgument):
        ctx.command.reset_cooldown(ctx)
        await ctx.message.delete()
        em = discord.Embed(title='Stardust.exe is not answering', description='No or wrong arguments were given. Check the arguments with help command.', color=0x7289da)
        message = await ctx.send(embed=em)
        await asyncio.sleep(6)
        await message.delete()
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CommandError):
        ctx.command.reset_cooldown(ctx)
        em = discord.Embed(title='Stardust.exe is not answering', description=f'An error occured. Please, report this if you believe this is a bug.', color=0x7289da)
        em.add_field(name='Info about error', value=f'{error}')
        message = await ctx.send(embed=em)
        await asyncio.sleep(30)
        await message.delete()

@bot.command(pass_context=True)
async def hello(ctx):
    debil = ctx.message.author
    em = discord.Embed(title='StarDust', description=f"Hello, {debil.mention}. Bot version is {version}. Server prefix is: {pref(bot, ctx)}", color=0x7289da)
    em.add_field(name='ToDo', value='Enchanting system \n \nShop inventory and gacha \n \nNPC pics, dialogies and text quests \n \nРусификация')
    await ctx.send(embed=em)

@bot.command(invoke_without_command=True)
async def info(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    if ctx.author is member.bot:
        await ctx.send("NO BOTS ALLOWED")
    else:
        db = sqlite3.connect('stardust.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id, guild_id FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.author.guild.id}")
        if cursor.fetchone() == None:
            cursor.execute(f"INSERT INTO stardust VALUES (?,?,?,?,?,?,?,?,?)", (member.guild.id, member.id, 0, 1, 1, 1, 1, 0, 1))
        else:
            db.commit()
            cursor.execute(f"SELECT starcount, exp, level FROM stardust WHERE user_id = {member.id} and guild_id = {member.guild.id}")
            xl = cursor.fetchone()
            x = int(xl[0])
            exp = int(xl[1])
            lvl = int(xl[2])

            cursor.execute(f"SELECT pickaxe, drillname FROM stardust WHERE user_id = {member.id} and guild_id = {member.guild.id}")
            result = cursor.fetchone()
            level = int(result[0])
            pick = int(result[1])
            db = sqlite3.connect('level.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT maxexp FROM level WHERE level = {lvl}')
            resexp = cursor.fetchone()
            maxexp = int(resexp[0])
            rank = math.ceil(lvl / 5)
            role = discord.utils.get(ctx.guild.roles, name=roles[rank][0])
            if role is None:
                role = f'{lvl} rank'
            else:
                role = role.mention
            em = discord.Embed(title=f'{member.name}', description=f"{role}\n{x}✨ {exp}/{maxexp}📕", color=member.color)

            em.add_field(name='Drill', value=f"{drills[pick]} \n{level} level")
            em.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=em)

@bot.command(invoke_without_command=True)
async def rating(ctx):
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT starcount, level FROM stardust WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}')
    result0 = cursor.fetchone()
    money = int(result0[0])
    level = int(result0[1])
    em = discord.Embed(title='Leaderboard', description=f'You are the #{ratemoney(ctx)} by stardust with {money}✨\nAnd #{raterank(ctx)} by rank with {level} rank.', color=0xa84300)
    await ctx.send(embed=em)

@bot.command(invoke_without_command=True)
async def mine(ctx):
    time = cd(ctx)
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT x FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}')
    result = cursor.fetchone()
    x = int(result[0])

    if x == 1:
        cursor.execute(f"SELECT user_id, guild_id FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
        if cursor.fetchone() is None:
            await ctx.send(f"ERROR: user didn't exist. Please, type {pref(bot, ctx)}info for registration. (bots cannot be registered)")
        else:
            cursor.execute(f"SELECT drillname FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
            resultus = cursor.fetchone()
            pick = int(resultus[0])
            x = random.randint(frs(ctx), lst(ctx))
            cursor.execute(f"UPDATE stardust SET starcount = starcount + {x} WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
            db.commit()
            em = discord.Embed(title='Meteor mining', description=f"You have mined {x}✨", color=0xf1c40f)
            em.set_thumbnail(url=drillpic[pick])
            await ctx.send(embed=em)
            cursor.execute(f'UPDATE stardust SET x = 0 WHERE user_id = {ctx.author.id} and guild_id = {ctx.author.guild.id}')
            db.commit()
            await asyncio.sleep(time)
            cursor.execute(f'UPDATE stardust SET x = 1 WHERE user_id = {ctx.author.id} and guild_id = {ctx.author.guild.id}')
            db.commit()
    elif x == 0:
        em = discord.Embed(title='Meteor mining', description=f"Drill on cooldown! Try after {round(cd(ctx) / 60, 2)} minutes.", color=0xf1c40f)
        await ctx.send(embed=em)

@bot.command(invoke_without_command=True)
@cooldown(1, per_sec=10, type=commands.BucketType.user)
async def upgrade(ctx):
    debil = ctx.message.author.name
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, guild_id FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
    if cursor.fetchone() is None:
        await ctx.send(f"ERROR: user didn't exist. Please, type {pref(bot, ctx)}info for registration. (bots cannot be registered)")
    else:
        db = sqlite3.connect('stardust.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT pickaxe, drillname FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
        result3 = cursor.fetchone()
        lvl = int(result3[0])
        drill = int(result3[1])
        db = sqlite3.connect('pickaxelevel.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT cost FROM pickaxelevel WHERE level = {lvl} and name = {drill}")
        result2 = cursor.fetchone()
        rcost = int(result2[0])
        if rcost == 0:
            em = discord.Embed(title='Stardust blacksmith', description=f"{debil}, your drill is on max level. Ascend to a new drill by 'ascending' it ({pref(bot, ctx)}ascend)", color=0x992d22)
            em.set_thumbnail(url='https://i.imgur.com/WCZgSch.png')
            message = await ctx.send(embed=em)
            await asyncio.sleep(10)
            await message.delete()
        else:

            em = discord.Embed(title='Stardust blacksmith', description=f"{debil} You want to upgrade your pick? it will cost you {rcost}✨", color=0x992d22)
            em.set_thumbnail(url='https://i.imgur.com/WCZgSch.png')

            cursor.execute(f'SELECT min, max, cooldown FROM pickaxelevel WHERE level = {lvl + 1} and name = {drill}')
            result = cursor.fetchone()
            em.add_field(name='Upgrading', value=f'On next level you will be able to mine from {int(result[0])}✨ up to {int(result[1])}✨. Cooldown on mining will be {round (int(result[2]) / 60, 2)} minutes.')

            moreoma = ctx.author.id

            message = await ctx.send(embed=em)
            emojis = ['✅', '❌']

            for emoji in (emojis):
                await message.add_reaction(emoji)

            def check(reaction, user):
                return user.id == moreoma and str(reaction.emoji) in emojis

            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
            except asyncio.TimeoutError:
                await message.delete()
                message = await ctx.send("timeout")
                await asyncio.sleep(10)
                await message.delete()
            else:

                if reaction.emoji == "✅":
                    await message.delete()
                    db = sqlite3.connect('stardust.sqlite')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT pickaxe, drillname FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                    result3 = cursor.fetchone()
                    lvl = int(result3[0])
                    drill = int(result3[1])
                    db = sqlite3.connect('pickaxelevel.sqlite')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT cost FROM pickaxelevel WHERE level = {lvl} and name = {drill}")
                    result2 = cursor.fetchone()
                    rcost = int(result2[0])
                    db = sqlite3.connect('stardust.sqlite')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT starcount FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                    result1 = cursor.fetchone()
                    money = int(result1[0])

                    if money >= rcost and rcost != 0:
                        db = sqlite3.connect('stardust.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"UPDATE stardust SET starcount = starcount - {rcost} WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                        cursor.execute(f"UPDATE stardust SET pickaxe = pickaxe + 1 WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                        db.commit()
                        cursor.execute(f"SELECT pickaxe FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                        result = cursor.fetchone()
                        newl = int(result[0])
                        oldl = newl - 1
                        em = discord.Embed(title='Stardust blacksmith', description=f"Hey, {debil}. We have upgraded your drill from level {oldl} to {newl}.", color=0x992d22)
                        em.set_thumbnail(url='https://i.imgur.com/WCZgSch.png')
                        message = await ctx.send(embed=em)
                        await asyncio.sleep(10)
                        await message.delete()
                    elif money < rcost:
                        em = discord.Embed(title='Stardust blacksmith', description=f"Sorry, {debil}. I don't give credits! comeback when you become a little mmmm richer!", color=0x992d22)
                        em.set_thumbnail(url='https://i.imgur.com/WCZgSch.png')
                        message = await ctx.send(embed=em)
                        await asyncio.sleep(10)
                        await message.delete()

                elif reaction.emoji == "❌":
                    await message.delete()
                    em = discord.Embed(title='Stardust blacksmith', description=f'Ok, {debil}, next time...', color=0x992d22)
                    em.set_thumbnail(url='https://i.imgur.com/WCZgSch.png')
                    message = await ctx.send(embed=em)
                    await asyncio.sleep(10)
                    await message.delete()

@bot.command(invoke_without_command=True)
@cooldown(1, per_sec=10, type=commands.BucketType.user)
async def ascend(ctx):
    debil = ctx.message.author.name
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, guild_id FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
    if cursor.fetchone() is None:
        await ctx.send(f"ERROR: user didn't exist. Please, type {pref(bot, ctx)}info for registration. (bots cannot be registered)")
    else:
        db = sqlite3.connect('stardust.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT drillname FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        drill = int(result[0])
        db = sqlite3.connect('pickaxelevel.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT ascendcost FROM pickaxelevel WHERE name = {drill}")
        result1 = cursor.fetchone()
        cost = int(result1[0])
        if cost == 0:
            em = discord.Embed(title='Stardust blacksmith', description=f"{debil}, you have the best drill possible.", color=0x992d22)
            em.set_thumbnail(url='https://i.imgur.com/WCZgSch.png')
            message = await ctx.send(embed=em)
            await asyncio.sleep(10)
            await message.delete()
        else:

            em = discord.Embed(title='Stardust blacksmith', description=f'{debil}, you want to ascend you {drills[drill]} to a new one? it will cost you {cost}✨', color=0x992d22)
            em.set_thumbnail(url='https://i.imgur.com/WCZgSch.png')

            cursor.execute(f'SELECT min, max, cooldown FROM pickaxelevel WHERE level = 1 and name = {drill + 1}')
            result = cursor.fetchone()
            em.add_field(name='Ascending', value=f'On next drill 1 level you will be able to mine from {int(result[0])}✨ up to {int(result[1])}✨. Cooldown on mining will be {round (int(result[2]) / 60, 2)} minutes.')

            moreoma = ctx.author.id

            message = await ctx.send(embed=em)
            emojis = ['✅', '❌']

            for emoji in (emojis):
                await message.add_reaction(emoji)

            def check(reaction, user):
                return user.id == moreoma and str(reaction.emoji) in emojis

            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
            except asyncio.TimeoutError:
                await message.delete()
                message = await ctx.send("timeout")
                await asyncio.sleep(10)
                await message.delete()
            else:
                if reaction.emoji == "✅":
                    await message.delete()
                    db = sqlite3.connect('stardust.sqlite')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT drillname, starcount FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                    result = cursor.fetchone()
                    drill = int(result[0])
                    money = int(result[1])
                    db = sqlite3.connect('pickaxelevel.sqlite')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT ascendcost FROM pickaxelevel WHERE name = {drill}")
                    result1 = cursor.fetchone()
                    cost = int(result1[0])
                    if money >= cost and cost != 0:
                        db = sqlite3.connect('stardust.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"UPDATE stardust SET starcount = starcount - {cost} WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                        cursor.execute(f'UPDATE stardust SET drillname = drillname + 1 WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}')
                        cursor.execute(f'UPDATE stardust SET pickaxe = 1 WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}')
                        db.commit()
                        cursor.execute(f"SELECT drillname FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                        result = cursor.fetchone()
                        newl = int(result[0])
                        oldl = newl - 1
                        em = discord.Embed(title='Stardust blacksmith', description=f"Congrats, {debil}! You bought new drill and ascend it from {drills[oldl]} to {drills[newl]}.", color=0x992d22)
                        em.set_thumbnail(url='https://i.imgur.com/WCZgSch.png')
                        message = await ctx.send(embed=em)
                        await asyncio.sleep(10)
                        await message.delete()
                    elif money < cost:
                        em = discord.Embed(title='Stardust blacksmith', description=f"Sorry, {debil}. I don't give credits! comeback when you become a little mmmm richer!", color=0x992d22)
                        em.set_thumbnail(url='https://i.imgur.com/WCZgSch.png')
                        message = await ctx.send(embed=em)
                        await asyncio.sleep(10)
                        await message.delete()

                elif reaction.emoji == "❌":
                    await message.delete()
                    em = discord.Embed(title='Stardust blacksmith', description=f'Ok, {debil}, next time...', color=0x992d22)
                    em.set_thumbnail(url='https://i.imgur.com/WCZgSch.png')
                    message = await ctx.send(embed=em)
                    await asyncio.sleep(10)
                    await message.delete()

@bot.command(invoke_without_command=True)
@cooldown(1, per_sec=10, type=commands.BucketType.user)
async def rankup(ctx):
    debil = ctx.message.author.name
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, guild_id FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
    if cursor.fetchone() is None:
        await ctx.send(f"ERROR: user didn't exist. Please, type {pref(bot, ctx)}info for registration. (bots cannot be registered)")
    else:
        db = sqlite3.connect('stardust.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT level FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        level = int(result[0])
        db = sqlite3.connect('level.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT starcost, expcost FROM level WHERE level = {level}")
        result1 = cursor.fetchone()
        starcost = int(result1[0])
        expcost = int(result1[1])
        if starcost == 0 or expcost == 0:
            em = discord.Embed(title='Commandor StarLight', description=f"{debil}, you have the highest rank possible.", color=0x11806a)
            message = await ctx.send(embed=em)
            await asyncio.sleep(10)
            await message.delete()
        else:

            em = discord.Embed(title='Commandor StarLight', description=f"{debil}, for the next rank you need to pay {starcost}✨ and {expcost}📕.", color=0x11806a)

            cursor.execute(f'SELECT maxexp FROM level WHERE level = {level + 1}')
            result = cursor.fetchone()
            mexp = int(result[0])
            em.add_field(name='Rank up', value=f'On the next rank you will be able to hold up to {mexp} exp.')

            moreoma = ctx.author.id

            message = await ctx.send(embed=em)
            emojis = ['✅', '❌']

            for emoji in (emojis):
                await message.add_reaction(emoji)

            def check(reaction, user):
                return user.id == moreoma and str(reaction.emoji) in emojis

            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
            except asyncio.TimeoutError:
                await message.delete()
                message = await ctx.send("timeout")
                await asyncio.sleep(10)
                await message.delete()
            else:
                if reaction.emoji == "✅":
                    await message.delete()
                    db = sqlite3.connect('stardust.sqlite')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT level, exp, starcount FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                    result2 = cursor.fetchone()
                    curlevel = int(result2[0])
                    curexp = int(result2[1])
                    money = int(result2[2])
                    db = sqlite3.connect('level.sqlite')
                    cursor = db.cursor()
                    cursor.execute(f"SELECT starcost, expcost FROM level WHERE level = {curlevel}")
                    result1 = cursor.fetchone()
                    moneycost = int(result1[0])
                    expcost = int(result1[1])
                    if money >= moneycost and curexp >= expcost and moneycost != 0 and expcost != 0:
                        db = sqlite3.connect('stardust.sqlite')
                        cursor = db.cursor()
                        cursor.execute(f"UPDATE stardust SET starcount = starcount - {moneycost} WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                        cursor.execute(f"UPDATE stardust SET exp = exp - {expcost} WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                        cursor.execute(f'UPDATE stardust SET level = level + 1 WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}')
                        db.commit()
                        cursor.execute(f"SELECT level FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                        result = cursor.fetchone()
                        newl = int(result[0])
                        oldl = newl - 1
                        oldr = math.ceil(oldl / 5)
                        newr = math.ceil(newl / 5)

                        if oldr < newr:
                            userid = ctx.author.id
                            user = discord.utils.get(bot.get_all_members(), id=userid)
                            role = discord.utils.get(ctx.guild.roles, name=roles[newr][0])
                            try:
                                await user.add_roles(role)
                                em = discord.Embed(title='Commandor StarLight', description=f"{debil}, you get a new role! {role}", color=0x11806a)
                                msg = await ctx.send(embed=em)
                                em = discord.Embed(title='Commandor StarLight', description=f"{debil}, you ranked up from {oldl} rank to {newl} rank.", color=0x11806a)
                                message = await ctx.send(embed=em)
                                await asyncio.sleep(10)
                                await message.delete()
                                await asyncio.sleep(15)
                                await msg.delete()
                            except Exception:
                                await ctx.send(f'Error occured, or roles not found. Type {pref(bot,ctx)}rolerankcreate to create roles. If them exists, please, report it as a bug')

                            em = discord.Embed(title='Commandor StarLight', description=f"{debil}, you ranked up from {oldl} rank to {newl} rank.", color=0x11806a)
                            message = await ctx.send(embed=em)
                            await asyncio.sleep(10)
                            await message.delete()
                        else:
                            em = discord.Embed(title='Commandor StarLight', description=f"{debil}, you ranked up from {oldl} rank to {newl} rank.", color=0x11806a)
                            message = await ctx.send(embed=em)
                            await asyncio.sleep(10)
                            await message.delete()
                    elif money < moneycost or curexp < expcost:
                        em = discord.Embed(title='Commandor StarLight', description=f"{debil}, you don't have enough experience or currency.", color=0x11806a)
                        message = await ctx.send(embed=em)
                        await asyncio.sleep(10)
                        await message.delete()

                elif reaction.emoji == "❌":
                    await message.delete()
                    em = discord.Embed(title='Commandor StarLight', description=f'I\'m busy right now, you know?', color=0x11806a)
                    message = await ctx.send(embed=em)
                    await asyncio.sleep(10)
                    await message.delete()

@bot.command(invoke_without_command=True)
@cooldown(1, per_sec=300, type=commands.BucketType.user)
async def transit(ctx, member: discord.Member, number):
    if ctx.author.id == 555767665986109450:
        ctx.command.reset_cooldown(ctx)
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, guild_id FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
    if cursor.fetchone() is None:
        await ctx.send(f"ERROR: user didn't exist. Please, type {pref(bot, ctx)}info for registration. (bots cannot be registered)")
    else:
        cursor.execute(f"SELECT user_id, guild_id FROM stardust WHERE user_id = {member.id} and guild_id = {member.guild.id}")
        x = cursor.fetchone()
        if x is None:
            em = discord.Embed(title='Star Bank', description=f"Failed to transit. This user doesn't exist in the database", color=0xa84300)
            await ctx.send(embed=em)
            ctx.command.reset_cooldown(ctx)
        else:
            if int(number) <= 10000:
                number = int(number)
                db = sqlite3.connect('stardust.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT starcount FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.author.guild.id}')
                result = cursor.fetchone()
                balance = int(result[0])
                if balance >= number:
                    cursor.execute(f'UPDATE stardust SET starcount = starcount - {number} WHERE user_id = {ctx.author.id} and guild_id = {ctx.author.guild.id}')
                    cursor.execute(f'UPDATE stardust SET starcount = starcount + {number} WHERE user_id = {member.id} and guild_id = {member.guild.id}')
                    db.commit()
                    em = discord.Embed(title='Star Bank', description=f'Successfully transited {number}✨ to {member.name}', color=0xa84300)
                    await ctx.send(embed=em)
                elif balance < number:
                    em = discord.Embed(title='Star Bank', description=f"You don't have enough money on your account", color=0xa84300)
                    await ctx.send(embed=em)
                    ctx.command.reset_cooldown(ctx)
            elif int(number) > 10000:
                em = discord.Embed(title='Star Bank', description=f"Sorry, you can't transit more than 10000 stardust.", color=0xa84300)
                await ctx.send(embed=em)
                ctx.command.reset_cooldown(ctx)

@bot.command(invoke_without_command=True)
async def leaderboard(ctx):
    x = 0
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT user_id, starcount FROM stardust WHERE guild_id = {ctx.guild.id} ORDER BY starcount DESC')
    result = ""
    tupleList = cursor.fetchmany(10)  # Данные

    for element in tupleList:
        x += 1
        result = result + f'#{x} - ' + str(bot.get_user(element[0]))[:-5] + f" has {str(element[1])}✨" + "\n"

    em = discord.Embed(title=f'Leaderboard of {ctx.guild.name}', description=f'{result}', color=0xa84300)
    em.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=em)

@bot.command(invoke_without_command=True)
@cooldown(1, per_sec=1000, type=commands.BucketType.user)
async def annigilate(ctx):
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id, guild_id FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
    if cursor.fetchone() is None:
        await ctx.send(f"ERROR: user didn't exist. Please, type {pref(bot, ctx)}info for registration. (bots cannot be registered)")
    else:
        em = discord.Embed(title='???', description='DIE? YOUR PROGRESS WILL BE RESET!!!')
        moreoma = ctx.author.id

        message = await ctx.send(embed=em)
        emojis = ['✅', '❌']

        for emoji in (emojis):
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user.id == moreoma and str(reaction.emoji) in emojis

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
        except asyncio.TimeoutError:
            await message.delete()
            message = await ctx.send("timeout")
            await asyncio.sleep(10)
            await message.delete()
        else:
            if reaction.emoji == "✅":
                await message.delete()
                db = sqlite3.connect('stardust.sqlite')
                cursor = db.cursor()
                cursor.execute(f"UPDATE stardust SET drillname = 1, pickaxe = 1, starcount = 0, x = 1, level = 1, exp = 0, y = 1 WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
                db.commit()
                em = discord.Embed(title='???', description='CLEANSED')
                message = await ctx.send(embed=em)
                await asyncio.sleep(10)
                await message.delete()
            elif reaction.emoji == "❌":
                await message.delete()
                em = discord.Embed(title='???', description='HHHHHHHHHHH')
                message = await ctx.send(embed=em)
                await asyncio.sleep(10)
                await message.delete()

@bot.command(invoke_without_command=True)
@cooldown(1, per_sec=1000, type=commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def rolerankcreate(ctx):
    guild = ctx.guild
    for i in roles.values():
        if discord.utils.get(ctx.guild.roles, name=i[0]):
            await ctx.send(f'Similar role ({i[0]}) is already exist')
        else:
            await guild.create_role(name=f'{i[0]}', color=i[1])
            await ctx.send(f'New role ({i[0]}) created.')
    db = sqlite3.connect('stardust.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT level, user_id FROM stardust WHERE guild_id = {ctx.guild.id}')
    result = cursor.fetchall()
    for i in result:
        level = i[0]
        number = math.ceil(level / 5)
        userid = i[1]

        user = discord.utils.get(bot.get_all_members(), id=userid)
        role = discord.utils.get(ctx.guild.roles, name=roles[number][0])
        try:
            await user.add_roles(role)
        except Exception:
            await ctx.send(f'Failed to give a role to user {userid}')
            continue
    await ctx.send('Done!')

@bot.command(invoke_without_command=True)
@cooldown(1, per_sec=1000, type=commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def rolerankdelete(ctx):
    for i in roles.values():
        if discord.utils.get(ctx.guild.roles, name=i[0]):
            ok = discord.utils.get(ctx.guild.roles, name=i[0])
            await ok.delete()
            await ctx.send(f'Role {i[0]} deleted')
        else:
            continue
    await ctx.send('Done!')

@bot.command(invoke_without_command=True)
async def redeem(ctx, code):
    cod = str(code)
    db = sqlite3.connect('promocode.sqlite')
    cursor = db.cursor()
    cursor.execute(f"SELECT amount FROM promocode WHERE guild_id = {ctx.guild.id} and code = '{cod}'")
    result = cursor.fetchone()
    if result is None:
        em = discord.Embed(title='Code redeem', description=f'Failed to redeem. Code does not exist or already redeemed', color=0x0033cc)
        msg = await ctx.send(embed=em)
        await asyncio.sleep(8)
        await msg.delete()
    else:
        mon = int(result[0])
        cursor.execute(f'DELETE FROM promocode WHERE code = "{cod}" and guild_id = {ctx.guild.id}')
        db.commit()
        db = sqlite3.connect('stardust.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id, guild_id FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
        if cursor.fetchone() is None:
            await ctx.send(f"ERROR: user didn't exist. Please, type {pref(bot, ctx)}info for registration. (bots cannot be registered)")
        else:
            cursor.execute(f'UPDATE stardust SET starcount = starcount + {mon} WHERE guild_id = {ctx.guild.id} and user_id = {ctx.author.id}')
            db.commit()
            em = discord.Embed(title='The stars are falling', description=f'{ctx.author.mention} have collected dust of the stars...', color=0xfeeb49)
            msg = await ctx.send(embed=em)
            await asyncio.sleep(8)
            await msg.delete()

@bot.command(invoke_without_command=True)
@cooldown(1, per_sec=800, type=commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def shopadd(ctx, cost, *, name):
    cost = int(cost)
    db = sqlite3.connect('shop.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT item FROM shop WHERE guild_id = {ctx.guild.id} and item = "{name}"')
    result = cursor.fetchone()
    if result is None:
        cursor.execute('INSERT INTO shop VALUES (?,?,?,?)',(ctx.guild.id, ctx.author.id, name, cost))
        db.commit()
        await ctx.send(f'Succesfully added an item to the shop "{name}" with cost of {cost}✨ (if someone buy it, bot will send you a message).')
    else:
        await ctx.send('Item with that name is already exist.')

@bot.command(invoke_without_command=True)
@cooldown(1, per_sec=800, type=commands.BucketType.user)
@commands.has_permissions(administrator=True)
async def shopdelete(ctx, *, name):
    db = sqlite3.connect('shop.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT item FROM shop WHERE guild_id = {ctx.guild.id} and creator = {ctx.author.id} and item = "{name}"')
    result = cursor.fetchone()
    if result is None:
        await ctx.send(f'No such your items with name "{name}"')
    else:
        cursor.execute(f'DELETE FROM shop WHERE guild_id = {ctx.guild.id} and creator = {ctx.author.id} and item = "{name}"')
        db.commit()
        await ctx.send(f'Item "{name}" deleted.')

@bot.command(invoke_without_command=True)
async def shop(ctx):
    x = 0
    db = sqlite3.connect('shop.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT item, cost FROM shop WHERE guild_id = {ctx.guild.id} ORDER BY cost DESC')
    result = ""
    tupleList = cursor.fetchall()  # Данные

    for element in tupleList:
        x += 1
        result = result + f'№{x}: ' + element[0] + f" [{str(element[1])}✨]" + "\n"

    em = discord.Embed(title=f'Shop of "{ctx.guild.name}"', description=f'{result}', color=0x9b59b6)
    em.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=em)

@bot.command(invoke_without_command=True)
async def buy(ctx, *, name):
    db = sqlite3.connect('shop.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT cost, creator FROM shop WHERE guild_id = {ctx.guild.id} and item = "{name}"')
    result = cursor.fetchone()

    if result is None:
        await ctx.send(f'No such item with name "{name}".')
    else:
        db = sqlite3.connect('stardust.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT starcount FROM stardust WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
        result1 = cursor.fetchone()
        money = int(result1[0])
        cost = int(result[0])
        creator = int(result[1])
        if money >= cost:
            cursor.execute(f"UPDATE stardust SET starcount = starcount - {cost} WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
            db.commit()
            user = bot.get_user(creator)
            try:
                await user.send(f'User {ctx.author.name} has bought item: "{name}".')
            except Exception:
                await ctx.send('Failed to contact with moderation. Please, tell to the moderator that you bought the item!')
            await ctx.send(f'{ctx.author.name}, you have bought "{name}".')
        elif money < cost:
            await ctx.send('You don\'t have enough money for this item')

# AUTHOR ONLY!

@bot.command(invoke_without_command=True)
async def cheat1(ctx, number):
    if ctx.author.id == 555767665986109450:
        db = sqlite3.connect('stardust.sqlite')
        cursor = db.cursor()
        cursor.execute(f"UPDATE stardust SET starcount = starcount + {number} WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
        db.commit()
        await ctx.send('Tenhunbuk$ for u <3.')
    else:
        await ctx.send('ACCESS DENIED.')

@bot.command(invoke_without_command=True)
async def cheat2(ctx):
    if ctx.author.id == 555767665986109450:
        db = sqlite3.connect('stardust.sqlite')
        cursor = db.cursor()
        cursor.execute(f"UPDATE stardust SET exp = exp + 10000 WHERE user_id = {ctx.author.id} and guild_id = {ctx.guild.id}")
        db.commit()
        await ctx.send('Tenhunbuk$ for u <3.')
    else:
        await ctx.send('ACCESS DENIED.')

bot.run(settings['token'])