import utils
import discord
from discord.ext import commands
import asyncio
import config
import logging
import time
import datetime

start_time = time.time()

cogs = ["verification", "help", "identify", "roles", "weather", "ticket"]

version = "Release 2.0.1"

async def get_prefix(bot, message):
    return commands.when_mentioned_or("h!")(bot, message)


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)

bot.remove_command("help")

for cog in cogs:
    bot.load_extension("Cogs." + cog)



def owner(ctx):
    return int(ctx.author.id) in config.ownerID


@commands.check(owner)
@bot.command()
async def restart(ctx):
    """
    Restart the bot.
    """
    restarting = discord.Embed(
        title="Restarting...",
        color=config.MAINCOLOR
    )
    msg = await ctx.send(embed=restarting)
    for cog in cogs:
        bot.reload_extension("Cogs." + cog)
        restarting.add_field(name=f"{cog}", value="✅ Restarted!")
        await msg.edit(embed=restarting)
    restarting.title = "Bot Restarted"
    await msg.edit(embed=restarting)
    logging.info(
        f"Bot has been restarted succesfully in {len(bot.guilds)} server(s) with {len(bot.users)} users by {ctx.author.name}#{ctx.author.discriminator} (ID - {ctx.author.id})!")
    await msg.delete(delay=3)
    if ctx.guild != None:
        await ctx.message.delete(delay=3)


@commands.check(owner)
@bot.command()
async def purge(ctx):
    x = config.USERS.delete_many({})
    print(x.deleted_count, "Documents deleted.")
    Guestrole = discord.utils.get(ctx.guild.roles, id = int(600884705277247489))
    middleschoolRole = discord.utils.get(ctx.guild.roles, id = int(546025605221711882))
    freshmen = discord.utils.get(ctx.guild.roles, id = int(543060124600762406))
    sophomore = discord.utils.get(ctx.guild.roles, id = int(543060215646388224))
    junior = discord.utils.get(ctx.guild.roles, id=int(543060357191827478))
    senior = discord.utils.get(ctx.guild.roles, id=int(543060511441289216))
    alumni = discord.utils.get(ctx.guild.roles, id=int(578278845648732173))

    for member in Guestrole.members:
        print("Kicked " + member.name)
        await member.kick()
    for member in middleschoolRole.members:
        print("Kicked " + member.name)
        await member.kick()
    for member in freshmen.members:
        embed = utils.MakeEmbed(title="New HHS Discord",
                                description="Hello, You have been kicked from the HCS Discord server, it is now going to become the HHS Discord Server, Please rejoin using this link. - " + config.invite_url)
        await member.send(embed=embed)
        print("Kicked " + member.name)
        await member.kick()
    for member in sophomore.members:
        embed = utils.MakeEmbed(title="New HHS Discord",
                                description="Hello, You have been kicked from the HCS Discord server, it is now going to become the HHS Discord Server, Please rejoin using this link. - " + config.invite_url)
        await member.send(embed=embed)
        print("Kicked " + member.name)
        await member.kick()
    for member in junior.members:
        if member.id != 245653078794174465:
            embed = utils.MakeEmbed(title="New HHS Discord",
                                    description="Hello, You have been kicked from the HCS Discord server, it is now going to become the HHS Discord Server, Please rejoin using this link. - " + config.invite_url)
            await member.send(embed=embed)
            print("Kicked " + member.name)
            await member.kick()
    for member in senior.members:
        embed = utils.MakeEmbed(title="New HHS Discord",
                                description="Hello, You have been kicked from the HCS Discord server, it is now going to become the HHS Discord Server, Please rejoin using this link. - " + config.invite_url)
        await member.send(embed=embed)
        print("Kicked " + member.name)
        await member.kick()
    for member in alumni.members:
        embed = utils.MakeEmbed(title="New HHS Discord",
                                description="Hello, You have been kicked from the HCS Discord server, it is now going to become the HHS Discord Server, Please rejoin using this link. - " + config.invite_url)
        await member.send(embed=embed)
        print("Kicked " + member.name)
        await member.kick()


@bot.command()
async def ping(ctx):
    embed=utils.MakeEmbed(title='🏓 PONG 🏓', description="**{0} ms**".format(round(bot.latency * 1000, 1)))
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    await bot.change_presence(status='idle')
    print("bot logged in with version: "+version)
    print("Connected to " + str(len(bot.guilds)) + " server(s):")
    print("Bot Connected to Gmail Servers")
    print('Started Status Loop')
    old_status = ""
    while True:
        status = await utils.get_weather()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
        if status != old_status:
            old_status = status
            print("Weather Updated to " + status)
        await asyncio.sleep(60)

@bot.command()
async def status(ctx):
    current_time = time.time()
    difference = int(round(current_time - start_time))
    uptime = str(datetime.timedelta(seconds=difference))
    online = 0
    offline = 0
    await bot.wait_until_ready()
    theservers = [543059123730644992]
    for server in theservers:
        for member in ctx.guild.members:
            if str(member.status) == 'online':
                online += 1
            elif str(member.status) == 'idle':
                online += 1
            elif str(member.status) == 'offline':
                offline += 1
            elif str(member.status) == 'dnd':
                online += 1
            elif str(member.status) == 'invisible':
                offline += 1
    allmembers=online + offline
    embed = utils.MakeEmbed(title="Status", description="**HCS Discord Server Status**:\n\nTotal **Members**:" + str(allmembers) +"\nOnline **Members**: "+ str(online) + "\nOffline **Members**: "+ str(offline) +"\nBot running for: "+uptime+"\n", doFooter=True)
    await ctx.send(embed=embed)

bot.run(config.TOKEN)
