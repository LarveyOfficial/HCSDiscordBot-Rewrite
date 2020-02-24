import discord
from discord.ext import commands
import config
import csv
import utils

class identify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='identify')
    async def identify(self, ctx, name: discord.Member = None):
        if name is None:
            embed = utils.MakeEmbed(title="Identify", description="Please Specify which user to Identify", doFooter=True)
            await ctx.send(embed=embed)
        else:
            if name.id:
                userid = config.USERS.find_one({'user_id': str(name.id)})
                if userid is None:
                    nouser = utils.MakeEmbed(title="ERROR", description="User does not Exist.")
                    await ctx.send(embed=nouser)
                else:
                    studentid = str(userid['student_id'])
                    with open('eggs.csv', newline='') as csvfile:
                        csvReader = csv.reader(csvfile, delimiter=',')
                        for row in csvReader:
                            student_id12 = ''.join(filter(lambda x: x.isdigit(), row[30]))
                            if str(student_id12) in row[30] and str(student_id12) == str(studentid):
                                firstname = row[1]
                                lastname = row[3]
                                discordname = str(name.name)
                                print("Finding " + discordname + "'s name..")
                                studentname = utils.MakeEmbed(title="Identify",
                                                        description=discordname + "'s" + " name is: " + firstname + " " + lastname)
                                print("Name found, sending")
                                await ctx.send(embed=studentname)
            else:
                nouser = utils.MakeEmbed(title="ERROR", description="User does not Exist.", color=config.ERRORCOLOR,
                                   doFooter=True)
                ctx.send(embed=nouser)

    @commands.command(name='identifyall')
    async def identifyall(self, ctx):
        Guestrole = discord.utils.get(ctx.guild.roles, id=int(600884705277247489))
        freshmen = discord.utils.get(ctx.guild.roles, id=int(543060124600762406))
        LeFreshmen = ""
        sophomore = discord.utils.get(ctx.guild.roles, id=int(543060215646388224))
        Sophomores = ""
        junior = discord.utils.get(ctx.guild.roles, id=int(543060357191827478))
        Juniors = ""
        senior = discord.utils.get(ctx.guild.roles, id=int(543060511441289216))
        seniors = ""
        alumni = discord.utils.get(ctx.guild.roles, id=int(578278845648732173))
        TheAlumni = ""
        loading = await ctx.send("Loading Freshmen...")
        for member in freshmen.members:
            if member in Guestrole.members:
                LeFreshmen += "\n- " + "**" + str(member.display_name) + "**" + " is a Guest"
            else:
                student = config.USERS.find_one({'user_id': str(member.id)})
                if student is None:
                    await ctx.send("ERROR: Member File Missing for + " + member.mention + ". Aborting Freshmen count")
                    break
                else:
                    studentid = str(student['student_id'])
                    with open('eggs.csv', newline='') as csvfile:
                        csvReader = csv.reader(csvfile, delimiter=',')
                        for row in csvReader:
                            thestudent_id = ''.join(filter(lambda x: x.isdigit(), row[30]))
                            if str(thestudent_id) in row[30] and str(thestudent_id) == str(studentid):
                                firstname = row[1]
                                lastname = row[3]
                                LeFreshmen += "\n- " + "**" + str(member.display_name) + "**" + " is " + str(
                                    firstname) + " " + str(lastname)
        await loading.edit(content="Loading Sophomores...")
        for member in sophomore.members:
            if member in Guestrole.members:
                Sophomores += "\n- " + "**" + str(member.display_name) + "**" + " is a Guest"
            else:
                student = config.USERS.find_one({'user_id': str(member.id)})
                if student is None:
                    await ctx.send("ERROR: Member File Missing for + " + member.mention + ". Aborting Sophomore count")
                    break
                else:
                    studentid = str(student['student_id'])
                    with open('eggs.csv', newline='') as csvfile:
                        csvReader = csv.reader(csvfile, delimiter=',')
                        for row in csvReader:
                            thestudent_id = ''.join(filter(lambda x: x.isdigit(), row[30]))
                            if str(thestudent_id) in row[30] and str(thestudent_id) == str(studentid):
                                firstname = row[1]
                                lastname = row[3]
                                Sophomores += "\n- " + "**" + str(member.display_name) + "**" + " is " + str(
                                    firstname) + " " + str(lastname)
        await loading.edit(content="Loading Juniors...")
        for member in junior.members:
            if member in Guestrole.members:
                Juniors += "\n- " + "**" + str(member.display_name) + "**" + " is a Guest"
            else:
                student = config.USERS.find_one({'user_id': str(member.id)})
                if student is None:
                    await ctx.send("ERROR: Member File Missing for + " + member.mention + ". Aborting Junior count")
                    break
                else:
                    studentid = str(student['student_id'])
                    with open('eggs.csv', newline='') as csvfile:
                        csvReader = csv.reader(csvfile, delimiter=',')
                        for row in csvReader:
                            thestudent_id = ''.join(filter(lambda x: x.isdigit(), row[30]))
                            if str(thestudent_id) in row[30] and str(thestudent_id) == str(studentid):
                                firstname = row[1]
                                lastname = row[3]
                                Juniors += "\n- " + "**" + str(member.display_name) + "**" + " is " + str(
                                    firstname) + " " + str(lastname)
        await loading.edit(content="Loading Seniors...")
        for member in senior.members:
            if member in Guestrole.members:
                seniors += "\n- " + "**" + str(member.display_name) + "**" + " is a Guest"
            else:
                student = config.USERS.find_one({'user_id': str(member.id)})
                if student is None:
                    await ctx.send("ERROR: Member File Missing for + " + member.mention + ". Aborting Senior count")
                else:
                    studentid = str(student['student_id'])
                    with open('eggs.csv', newline='') as csvfile:
                        csvReader = csv.reader(csvfile, delimiter=',')
                        for row in csvReader:
                            thestudent_id = ''.join(filter(lambda x: x.isdigit(), row[30]))
                            if str(thestudent_id) in row[30] and str(thestudent_id) == str(studentid):
                                firstname = row[1]
                                lastname = row[3]
                                seniors += "\n- " + "**" + str(member.display_name) + "**" + " is " + str(
                                    firstname) + " " + str(lastname)
        await loading.edit(content="Loading Alumni...")
        for member in alumni.members:
            if member in Guestrole.members:
                TheAlumni += "\n- " + "**" + str(member.display_name) + "**" + " is a Guest"
            else:
                student = config.USERS.find_one({'user_id': str(member.id)})
                if student is None:
                    await ctx.send("ERROR: Member File Missing for + " + member.mention + ". Aborting Alumni count")
                else:
                    studentid = str(student['student_id'])
                    with open('eggs.csv', newline='') as csvfile:
                        csvReader = csv.reader(csvfile, delimiter=',')
                        for row in csvReader:
                            thestudent_id = ''.join(filter(lambda x: x.isdigit(), row[30]))
                            if str(thestudent_id) in row[30] and str(thestudent_id) == str(studentid):
                                firstname = row[1]
                                lastname = row[3]
                                TheAlumni += "\n- " + "**" + str(member.display_name) + "**" + " is " + str(
                                    firstname) + " " + str(lastname)
        await loading.delete()
        AlumniEmbed = utils.MakeEmbed(title="**Alumni**", description=TheAlumni)
        await ctx.send(embed=AlumniEmbed)
        SeniorEmbed = utils.MakeEmbed(title="**Seniors**", description=seniors)
        await ctx.send(embed=SeniorEmbed)
        JuniorEmbed = utils.MakeEmbed(title="**Juniors**", description=Juniors)
        await ctx.send(embed=JuniorEmbed)
        SophEmbed = utils.MakeEmbed(title="**Sophomores**", description=Sophomores)
        await ctx.send(embed=SophEmbed)
        FreshEmbed = utils.MakeEmbed(title="**Freshmen**", description=LeFreshmen)
        await ctx.send(embed=FreshEmbed)

def setup(bot):
    bot.add_cog(identify(bot))