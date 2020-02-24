import csv
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib
import discord
from discord.ext import commands
import config


class verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def gen_code(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    async def make_doc(self, user_name=None, user_id=None, code=None, grade=None, student_id=None, verified=False):
        doc_ = {'user_name': user_name, 'user_id': str(user_id), 'code': code, 'grade': str(grade),
                'student_id': str(student_id),
                'verified': verified}  # 'code' == None if verified and verified will be true
        return doc_

    async def sendemail(self, studentemail, emailcode):
        body = "Your HHSDiscord Verification Code is \n\n" + str(emailcode) + "\n\nPlease use h!verify " + str(
            emailcode) + " in your setup channel\nYour code will Expire in 24hours\n\n" + "If you don't believe this was you please msg Larvey#0001 on Discord."
        emailsubject = "HHSDiscord Authentication"

        emailmsg = MIMEMultipart()
        emailmsg['To'] = studentemail
        emailmsg['From'] = config.mailfromAddress
        emailmsg['Subject'] = emailsubject
        emailmsg.attach(MIMEText(body, 'plain'))
        message = emailmsg.as_string()

        emailserver = smtplib.SMTP(config.mailfromserver)
        emailserver.starttls()
        emailserver.login(config.mailfromAddress, config.mailfrompassword)
        print("Sending Email....")
        emailserver.sendmail(config.mailfromAddress, studentemail, message)
        print("Email Sent to " + studentemail)
        emailserver.quit()

    def check_for_doc(self, check_key, check_val, check_key2=None, check_val2=None):
        if not check_key2 or not check_val2:
            the_doc = config.USERS.find_one({check_key: check_val})
            if the_doc:
                return True
            else:
                return False
        else:
            the_doc = config.USERS.find_one({check_key: check_val, check_key2: check_val2})
            if the_doc:
                return True
            else:
                return False

    @commands.Cog.listener(name='on_member_join')
    async def on_member_join(self, member):
        await self.playerjoin(member)


    @commands.Cog.listener(name='on_member_remove')
    async def on_member_remove(self, member):
        await self.playerleave(member)

    async def playerjoin(self, member):
        checkdoc = config.USERS.find_one({'user_id': str(member.id), 'verified': True})
        if checkdoc is not None:
            grade_role = discord.utils.get(member.guild.roles, name=checkdoc['grade'])
            if grade_role is not None:
                await member.add_roles(grade_role)
            print("user {} joined. but is already registered".format(member.name))
            return
        else:
            await self.giverole(member)
        print('New player joined... Making Setup Room')
        channel = await self.make_new_channel(member)

        await channel.send(
            "**Welcome **" + member.mention + "** to the HHS Discord Server!**\n\n``Please Make Sure to Read the rules in #rules``\n\n__Lets Start the Setup!__\n")
        await self.select_high_school(member, channel)

    async def select_high_school(self, member, channel):
        print(member.name + " choose highschool")

        msg2 = await channel.send(
            "Whats your grade?\n\n🇦: Freshmen,\n🇧: Sophomore,\n🇨: Junior,\n🇩: Senior\n\nReact accordingly.")
        await msg2.add_reaction("🇦")
        await msg2.add_reaction("🇧")
        await msg2.add_reaction("🇨")
        await msg2.add_reaction("🇩")
        while True:
            reaction2, react_member2 = await self.bot.wait_for('reaction_add')
            if react_member2.id is member.id:
                if reaction2.emoji == "🇦":
                    print(member.name + " Choose Freshmen... ew")
                    await msg2.edit(content='9th grade selected')
                    gradeselect = "Freshmen"
                    roleid = 543060124600762406
                    role_ = discord.utils.get(member.guild.roles, id=roleid)
                    await member.add_roles(role_)
                    break
                elif reaction2.emoji == "🇧":
                    print(member.name + " Choose Sophomore")
                    await msg2.edit(content='10th grade selected')
                    gradeselect = "Sophomore"
                    roleid = 543060215646388224
                    role_ = discord.utils.get(member.guild.roles, id=roleid)
                    await member.add_roles(role_)
                    break
                elif reaction2.emoji == "🇨":
                    print(member.name + " Choose Junior")
                    await msg2.edit(content='11th grade selected')
                    gradeselect = "Junior"
                    roleid = 543060357191827478
                    role_ = discord.utils.get(member.guild.roles, id=roleid)
                    await member.add_roles(role_)
                    break
                elif reaction2.emoji == "🇩":
                    print(member.name + " Choose Senior")
                    await msg2.edit(content='12th grade selected')
                    gradeselect = "Senior"
                    roleid = 543060511441289216
                    role_ = discord.utils.get(member.guild.roles, id=roleid)
                    await member.add_roles(role_)
                    print(member.name + " Choose Senior")
                    break
                else:
                    continue
            else:
                continue

        print("generating code...")
        their_code = await self.gen_code()
        print("generated code: " + str(their_code))
        if not self.check_for_doc("user_id", str(member.id)):
            print("saving...")
            doc = await self.make_doc(member.name, member.id, their_code, gradeselect, None, False)
            config.USERS.insert_one(doc)
            print("saved.")
            await self.get_student_id(member, channel)

    async def get_student_id(self, member, channel):
        await channel.send("*Final Step:* Please type your student ID.")
        guild = self.bot.get_guild(config.guild_id)
        while member in guild.members:
            idmsg = await self.bot.wait_for('message')
            if idmsg.author.id is member.id:
                student_id6 = ''.join(filter(lambda x: x.isdigit(), idmsg.content))
                try_for_id = config.USERS.find_one({'student_id': str(student_id6)})
                if try_for_id is not None:
                    await channel.send(
                        'ERROR: That ID is already In use. Please use another one. Contact Larvey#0001 if this *is* your student ID.')
                    continue
                if student_id6 is '':
                    await channel.send('ERROR: Thats not a Valid ID')
                    continue
                if await self.compare_id(idmsg.channel, idmsg.author, student_id6):
                    return
                else:
                    continue
            else:
                continue

    async def compare_id(self, channel, member, student_id):
        print('started comparing ids for {}'.format(member.name))
        confirmmsg = await channel.send('Searching for your Student ID...')
        with open('eggs.csv', newline='') as csvfile:
            csvReader = csv.reader(csvfile, delimiter=',')
            for row in csvReader:
                student_id9 = ''.join(filter(lambda x: x.isdigit(), row[30]))
                if str(student_id) in row[30] and len(str(student_id)) == 8:
                    print("student ID matched: " + row[30] + ' - ' + student_id9)
                    their_doc = config.USERS.find_one({'user_id': str(member.id)})
                    if their_doc is not None:
                        # print('verify using this... $verify '+ their_doc['code'])
                        emailcode = their_doc['code']
                        studentemail = str(student_id) + "@hartlandschools.us"
                        # await last_message.delete()
                        await confirmmsg.edit(
                            content="Found that Student ID! (" + student_id + ") " + "Would you like us to send you an email to confirm it is you?")
                        react_yes = await confirmmsg.add_reaction("🇾")
                        react_no = await confirmmsg.add_reaction("🇳")
                        while True:
                            reaction3, react_member3 = await self.bot.wait_for('reaction_add')
                            if react_member3.id is member.id:
                                if reaction3.emoji == "🇾":
                                    print(
                                        member.name + " has confirmed that " + student_id + " is their student ID. Sending Email.")
                                    print("Email Address is: " + studentemail)
                                    await channel.send(
                                        "We have sent you an email with a Verifiation Code to " + studentemail + "\n\nEmail may take up to 2 Minutes to Send.\n\n**USE h!Verify + YOURCODE to verify**\nEx: h!verify ABC123")
                                    await self.sendemail(studentemail, emailcode)
                                    updated_tag = {"$set": {'student_id': str(student_id)}}
                                    config.USERS.update_one({'user_id': str(member.id)}, updated_tag)
                                    print('Email Sent and Finished Setup')
                                    return True
                                if reaction3.emoji == "🇳":
                                    await confirmmsg.edit(
                                        content="Not sending email. (In order to complete the setup, you will need to verify by email.)\nPlease type your student ID.")
                                    await confirmmsg.remove_reaction("🇾", self.bot.user)
                                    await confirmmsg.remove_reaction("🇳", self.bot.user)
                                    await confirmmsg.remove_reaction("🇳", react_member3)
                                    return False

            print('No ID Found (Welp.. Thats a Wrap)')
            await confirmmsg.edit(content='Sorry, That ID was not Found. Please Try Again')
            return False

    async def make_new_channel(self, member):
        overwrites = {
            member.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, add_reactions=False),
            self.bot.user: discord.PermissionOverwrite(read_messages=True)
        }

        category = discord.utils.get(member.guild.categories, name="Setup")
        if not category:
            await member.guild.create_category_channel(name='Setup')
            category = discord.utils.get(member.guild.categories, name="Setup")

        channel = await member.guild.create_text_channel(str(member.id), overwrites=overwrites, category=category)
        print("Creating new setup for " + str(member) + ".")
        return channel

    async def giverole(self, member):
        roleid = 576127240669233152
        role = discord.utils.get(member.guild.roles, id=roleid)
        await member.add_roles(role)
        print(
            member.name + "(" + str(member.id) + ") " + "has Joined the discord adding them to the role: " + str(role))

    async def joinmsg(self, member):
        welcome = discord.utils.get(member.guild.channels, id=int(543062297749487627))
        embed = discord.Embed(title="Member Joined", description=member.name, color=config.MAINCOLOR)
        await welcome.send(embed=embed)

    @commands.command()
    async def verify(self, ctx, code: str = None):
        if code is not None:
            doc = config.USERS.find_one({'code': code, 'user_id': str(ctx.author.id)})
            if doc is not None:
                updated_tag = {"$set": {'verified': True, 'code': None}}
                config.USERS.update_one({'code': code, 'user_id': str(ctx.author.id)}, updated_tag)
                roleid = 576127240669233152
                role_ = discord.utils.get(ctx.guild.roles, id=roleid)
                await ctx.author.remove_roles(role_)
                channel = discord.utils.get(ctx.guild.text_channels, name=str(ctx.author.id))
                await self.joinmsg(ctx.author)
                if channel:
                    print(str(ctx.author.id) + " is verified, deleting their setup")
                    await channel.delete()

    async def playerleave(self, member):
        if self.check_for_doc("user_id", str(member.id)):
            config.USERS.delete_many({'user_id': str(member.id), 'verified': False})

        channel = discord.utils.get(member.guild.text_channels, name=str(member.id))
        if channel:
            print(str(member.id) + " left, deleting their setup")
            await channel.delete()

def setup(bot):
    bot.add_cog(verification(bot))
