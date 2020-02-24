import discord
from discord.ext import commands
import config
import utils


class roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(aliases = ["roles"])
    async def role(self, ctx, _role: str = None):
        if _role is None:
            embed = utils.MakeEmbed(title="List of Roles:", description=(', '.join(config.role_list)), doFooter=True)
            await ctx.send(embed=embed)
        else:
            if _role.lower() in config.role_list:
                get_role = discord.utils.get(ctx.guild.roles, name=_role.lower())
                if get_role is not None:
                    await ctx.author.add_roles(get_role)
                    print("Adding " + str(ctx.author) + " To Role: " + str(get_role))
                    embedconfirm = utils.MakeEmbed(title="Added you to Role:", description=str(get_role), doFooter=True)
                    await ctx.send(embed=embedconfirm)
                else:
                    await ctx.send("That Role Dosen't Exist")
            else:
                await ctx.send("That Role Dosen't Exist")

    @commands.command()
    async def rmrole(self, ctx, _role: str = None):
        if _role is None:
            embed = utils.MakeEmbed(title="List of Roles:", description=(', '.join(config.role_list)), doFooter=True)
            await ctx.send(embed=embed)
        else:
            get_role = discord.utils.get(ctx.guild.roles, name=_role.lower())
            if get_role is not None and get_role in ctx.author.roles:
                await ctx.author.remove_roles(get_role)
                print("Removing " + str(ctx.author) + " From Role: " + str(get_role))
                embedconfirm = utils.MakeEmbed(title="Removed you From Role:", description=str(get_role), doFooter=True)
                await ctx.send(embed=embedconfirm)
            else:
                embederror = utils.MakeEmbed(title="ERROR", description="You don't have that Role!", doFooter=True,
                                       color=config.ERRORCOLOR)
                await ctx.send(embed=embederror)

def setup(bot):
    bot.add_cog(roles(bot))
