import discord
from discord.ext import commands
import config
import utils
class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = utils.MakeEmbed(title="Help", description="For more details on each category please do h!help <Category> \n\n -Identify \n\n -Roles\n\n -Tickets\n\n -Weather", doFooter=True)
            await ctx.send(embed=embed)
    @help.command()
    async def Identify(self, ctx):
        embed = utils.MakeEmbed(title="Help - Identify", description=" - h!identify <Username or Mention> - Identifies a User's real name.\n\n - h!identifyall - Identify all users in the Discord Server.")
        await ctx.send(embed=embed)
    @help.command(aliases = ["role"])
    async def Roles(self, ctx):
        embed = utils.MakeEmbed(title="Help - Roles", description=" - h!roles - See the list of available roles.\n\n - h!role <role name> - Join a role.\n\n - h!rmrole <role name> Leave a role.")
        await ctx.send(embed=embed)
    @help.command()
    async def Tickets(self, ctx):
        embed = utils.MakeEmbed(title="Help - Tickets", description=" - h!ticket - Open a Ticket for supports\n\n - h!close - Close a ticket.\n\n - h!adduser <username or mention> - Add another user to the Ticket.\n\n - h!rmuser <mention> - Remove Mentioned user from Ticket.")
        await ctx.send(embed=embed)
    @help.command()
    async def Weather(self, ctx):
        embed = utils.MakeEmbed(title="Help - Weather", description="h!weather - Check the Weather.")
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(help(bot))