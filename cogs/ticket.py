import discord
from discord.ext import commands
import config
import utils

class ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx, *, name: str = None):
        adminrole = discord.utils.get(ctx.guild.roles, id=543060916086767617)
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True),
            self.bot.user: discord.PermissionOverwrite(read_messages=True),
            adminrole: discord.PermissionOverwrite(read_messages=True),
        }
        ticketcategory = discord.utils.get(ctx.guild.categories, name="tickets")
        if not ticketcategory:
            await ctx.guild.create_category_channel(name="tickets")
            ticketcategory = discord.utils.get(ctx.guild.categories, name="tickets")
        ticketname = "ticket-{0}".format(ctx.author.id)
        ticketchannelmade = discord.utils.get(ctx.guild.channels, name=ticketname)
        if not ticketchannelmade:
            embed = utils.MakeEmbed(title="Ticket", description="Making your Ticket...", doFooter=True)
            await ctx.send(embed=embed)
            ticketchannel = await ctx.guild.create_text_channel(ticketname, overwrites=overwrites,
                                                                category=ticketcategory)
            print(ctx.author.name + "Needs A Ticket..")
            ticketembed = utils.MakeEmbed(title="Ticket",
                                    description="Welcome " + ctx.author.mention + " This is your Ticket! ",
                                    doFooter=True)
            await ticketchannel.send(embed=ticketembed)
            adminmention = await ticketchannel.send("<@&543060916086767617>")
            adminmention.delete()
            usermention = await ticketchannel.send(ctx.author.mention)
            usermention.delete()

        else:
            ticketExists = utils.MakeEmbed(title="ERROR", description="You already have a ticket open!", doFooter=True,
                                     color=discord.Color.dark_red())
            await ctx.send(embed=ticketExists)

    @commands.command()
    async def adduser(self, ctx, member: discord.Member = None):
        if member is not None:
            category = discord.utils.get(ctx.guild.categories, name="tickets")
            if category is None:
                error_embed = utils.MakeEmbed(title="ERROR", description="an error has occured. There is no Ticket category.")
                await ctx.send(embed=error_embed)
                return
            if ctx.channel.category_id == category.id:
                await ctx.channel.set_permissions(member, read_messages=True, send_messages=True)
                successadd = utils.MakeEmbed(title="Ticket",
                                       description="I have added " + member.mention + " to this Ticket!")
                await ctx.send(embed=successadd)
            else:
                notinticket = utils.MakeEmbed(title="ERROR", description="This command must be made in a Ticket Channel!",
                                        doFooter=True, color=discord.Color.dark_red())
                await ctx.send(embed=notinticket)
        else:
            membernotexist = utils.MakeEmbed(title="ERROR", description="Please Specify a User!", doFooter=True,
                                       color=discord.Color.dark_red())
            await ctx.send(embed=membernotexist)
            return

    @commands.command()
    async def rmuser(self, ctx, member: discord.Member = None):
        if member is not None:
            category = discord.utils.get(ctx.guild.categories, name="tickets")
            if category is None:
                error_embed = utils.MakeEmbed(title="ERROR", description="an error has occured. There is no Ticket category.")
                await ctx.send(embed=error_embed)
                return
            if ctx.channel.category_id == category.id:
                await ctx.channel.set_permissions(member, read_messages=False, send_messages=False)
                successrm = utils.MakeEmbed(title="Ticket",
                                      description="I have removed " + member.name + " from this Ticket.")
                await ctx.send(embed=successrm)
            else:
                notinticket = utils.MakeEmbed(title="ERROR", description="This command must be made in a Ticket Channel!",
                                        doFooter=True, color=discord.Color.dark_red())
                await ctx.send(embed=notinticket)
                return
        else:
            membernotexist = utils.MakeEmbed(title="ERROR", description="Please Specify a User!", doFooter=True,
                                       color=discord.Color.dark_red())
            await ctx.send(embed=membernotexist)
            return

    @commands.command()
    async def close(self, ctx):
        ticketcategory = discord.utils.get(ctx.guild.categories, name="tickets")
        roleid = 543060916086767617
        if ctx.channel.category_id == ticketcategory.id:
            if ctx.channel.name == "ticket-{0}".format(ctx.author.id):
                await ctx.channel.delete()
            elif roleid in [y.id for y in ctx.author.roles]:
                await ctx.channel.delete()
            else:
                noturticketlol = utils.MakeEmbed(title="ERROR", description="This is not your Ticket!", doFooter=True,
                                           color=discord.Color.dark_red())
                await ctx.send(embed=noturticketlol)

        else:
            notinticketcategory = utils.MakeEmbed(title="ERROR", description="This command can only be done in a ticket!",
                                            doFooter=True, color=discord.Color.dark_red())
            await ctx.send(embed=notinticketcategory)
def setup(bot):
    bot.add_cog(ticket(bot))