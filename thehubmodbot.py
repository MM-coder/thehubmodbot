import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import random
import time
import json
import requests
import inspect
import aiohttp
import datetime

bot = commands.Bot(command_prefix='h!')
bot.remove_command('help')
async def loop():
    while True:
        await bot.change_presence(game=discord.Game(name="h!help", type=2))
        await asyncio.sleep(15)
        await bot.change_presence(game=discord.Game(name="some dope people", type=2))
        await asyncio.sleep(15)


@bot.event
async def on_ready():
    print ("Bot has Booted!")
    print ("I am running on " + bot.user.name)
    print ("With the ID: " + bot.user.id)
    await bot.change_presence(game=discord.Game(name="mmgamerbot.com", url="https://twitch.tv/MMgamerBOT", type=1))
    await loop()


async def webupdate():
   while 1:
      interfacewebhook = "http://hub-interface.herokuapp.com/webhook"
      headers = {
         "X-Hub-Signature": "e8ef5fc42e475fc0e929986dac9352a6c298119b"
      }
      data = {
         "time": datetime.datetime.now(),
         "servermembers": bot.get_server(468031201886863372).member_count
      }
      response = requests.post(interfacewebhook, data=json.dumps(status), headers=header)
      await asyncio.sleep(60)




@bot.command(pass_context=True)
async def remove_cmd(ctx, cmd):
    if ctx.message.author.id != '397745647723216898':
        return await bot.say("No perms from developers")
    bot.remove_command(cmd)



@bot.event
async def on_command_error(ctx, error):
    if isinstance(ctx, discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(title="Error:",
                              description="Damm it! I cant find that! Try `!help`.",
                              colour=0xe73c24)
        await bot.send_message(error.message.channel, embed=embed)
    else:
        embed = discord.Embed(title="Error:",
                              description=f"{ctx}",
                              colour=0xe73c24)
        await bot.send_message(error.message.channel, embed=embed)
        raise(ctx)



@bot.command(pass_context=True)
async def pfp(ctx, member: discord.Member):
     embed=discord.Embed(title="The users profile picture", color=0x2C2C2C)
     embed.set_image(url=member.avatar_url)
     embed.set_footer(icon_url="https://i.imgur.com/yB0Lig7.png", text="Moderation bot for The Hub!")
     await bot.say(embed=embed)

@bot.command(pass_context=True, name="StatChange", aliases=['cp'])
async def cp(ctx, pt: int, *, name):
    """
    Changes the bot status (Admin-Only)
    """
    if ctx.message.author.server_permissions.administrator:
        await bot.change_presence(game=discord.Game(name=name, type=2))
        embed = discord.Embed(title='Status changed!', description='The bot status was changed!', colour=mc)
        await bot.say(embed=embed)
    else:
        embed=discord.Embed(title='No perms', description='You dont have perms to change the bot status', color=mc)
        await bot.say(embed=embed)



@bot.command(pass_context=True)
async def help(ctx):
        embed=discord.Embed(title="All Help", description="""
        Moderation Commands:
        •`h!warn <user> <reason>` - Warns a user (Also DM's)
        •`h!kick <@user>` - Kicks the user from the server
        •`h!ban <@user>` - Bans a user for the server
        •`h!mute <@user>` - Mutes a user
        •`h!leave` - Makes the bot leave the server
        """, color=0x2C2C2C)
        embed.set_footer(icon_url="https://i.imgur.com/yB0Lig7.png", text="Moderation bot for The Hub!")
        await bot.whisper(embed=embed)
        await bot.say("Check your DMs")


@bot.command(pass_context=True)
async def mute(ctx, member: discord.Member, time: int, *, reason):
    if ctx.message.author.server_permissions.administrator != True:
        return await bot.say("No perms!")
    await bot.send_message(member, f"You have been muted for {time} Seconds in {ctx.message.server.name}! Be sure to read the rules again! ")
    role = discord.utils.get(ctx.message.server.roles, name="Muted")
    await bot.add_roles(member, role)
    embed = discord.Embed(title="MUTED", description="{} You have been Muted for **{}** Seconds. Reason: {}".format(member.mention, time, reason), color=0x2C2C2C)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    await bot.say(embed=embed)
    await asyncio.sleep(time)
    await bot.remove_roles(member, role)
    await bot.send_message(member, f"You have been unmuted! Be careful!")
    embed = discord.Embed(title="Member unmuted", description="{} Has been UnMuted".format(member.mention), color=0x2C2C2C)
    embed.set_author(name=member.name, icon_url=member.avatar_url)
    await bot.say(embed=embed)



@bot.command(pass_context=True)
async def ping(ctx):
        t1 = time.perf_counter()
        tmp = await bot.say("pinging...")
        t2 = time.perf_counter()
        await bot.say("Ping: {}ms".format(round((t2-t1)*1000)))
        await bot.delete_message(tmp)
@bot.command(pass_context = True)
async def ban(ctx, member: discord.Member):
    if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '397745647723216898':
        try:
            await bot.ban(member)
            await bot.say(":thumbsup: Succesfully issued a ban!")
        except discord.errors.Forbidden:
            await bot.say(":x: No perms!")

@bot.command(pass_context=True)
async def info(ctx, user: discord.Member=None):
    if user is None:
        embed = discord.Embed(color=0x2C2C2C)
        embed.set_author(name=ctx.message.author.display_name)
        embed.add_field(name=":desktop:ID:", value=ctx.message.author.id, inline=True)
        embed.add_field(name=":satellite:Status:", value=ctx.message.author.status, inline=True)
        embed.add_field(name=":star2:Joined server::", value=ctx.message.author.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=True)
        embed.add_field(name=":date:Created account:", value=ctx.message.author.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=True)
        embed.add_field(name=":bust_in_silhouette:Nickname:", value=user.display_name)
        embed.add_field(name=":robot:Is Bot:", value=user.bot)
        embed.add_field(name=':ballot_box_with_check: Top role:', value=ctx.message.author.top_role.name, inline=True)
        embed.add_field(name=':video_game: Playing:', value=ctx.message.author.game, inline=True)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        await asyncio.sleep(0.3)
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(color=0x2C2C2C)
        embed.set_author(name=ctx.message.author.display_name)
        embed.add_field(name=":desktop:ID:", value=ctx.message.author.id, inline=True)
        embed.add_field(name=":satellite:Status:", value=ctx.message.author.status, inline=True)
        embed.add_field(name=":star2:Joined server::", value=ctx.message.author.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=True)
        embed.add_field(name=":date:Created account:", value=ctx.message.author.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=True)
        embed.add_field(name=":bust_in_silhouette:Nickname:", value=user.display_name)
        embed.add_field(name=":robot:Is Bot:", value=user.bot)
        embed.add_field(name=':ballot_box_with_check: Top role:', value=ctx.message.author.top_role.name, inline=True)
        embed.add_field(name=':video_game: Playing:', value=ctx.message.author.game, inline=True)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        await asyncio.sleep(0.3)
        await bot.say(embed=embed)


@bot.command(pass_context=True)
async def checkuser(ctx, user: discord.Member=None):
    if user is None:
        embed = discord.Embed(color=0x2C2C2C)
        embed.set_author(name=ctx.message.author.name ,icon_url=ctx.message.author.avatar_url)
        embed.add_field(name=":star2:Joined server:", value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=True)
        embed.add_field(name=":date:Created account:", value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=True)
        await bot.say (embed=embed)
    else:
        embed = discord.Embed(color=0x2C2C2C)
        embed.set_author(name=ctx.message.author.name , icon_url=ctx.message.author.avatar_url)
        embed.add_field(name=":star2:Joined server:", value=user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=True)
        embed.add_field(name=":date:Created account:", value=user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=True)
        await bot.say (embed=embed)

@bot.command(pass_context=True)
async def warn(ctx, userName: discord.Member ,*, reason: str):
    if "Staff" in [role.name for role in ctx.message.author.roles] or ctx.message.author.server_permissions.administrator:
        embed = discord.Embed(title="Warned", description="{} You have been warned for **{}**".format(userName.mention, reason), color=0x2C2C2C)
        embed.set_thumbnail(url=userName.avatar_url)
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        await bot.send_message(bot.get_channel("468043561875800095"), embed=embed)
        await bot.say(embed=embed)
        await bot.send_message(userName, "You Have Been Warned. Reason: {}".format(reason))
    else:
        await bot.say("{} :x: You are not allowed to use this command!".format(ctx.message.author.mention))

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def delete(ctx, number):
    msgs = []
    number = int(number)
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        msgs.append(x)
    await bot.delete_messages(msgs)
    embed = discord.Embed(title=f"{number} messages deleted", description="Wow, somebody's been spamming", color=0x2C2C2C)
    test = await bot.say(embed=embed)
    await asyncio.sleep(10)
    await bot.delete_message(test)

@bot.command(pass_context = True)
async def kick(ctx, member: discord.Member):
    if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '397745647723216898':
        try:
            await bot.kick(member)
            await bot.say("Kicked that BAD coder!")
        except discord.errors.Forbidden:
            await bot.say(":x: No perms!")
    else:
        await bot.say("You dont have perms")



@bot.command(pass_context=True)
async def server(ctx):
    embed = discord.Embed(description="Here's what I could find:", color=0x2C2C2C)
    embed.add_field(name="Name", value=ctx.message.server.name)
    embed.add_field(name="Owner", value=ctx.message.server.owner)
    embed.add_field(name="Region", value=ctx.message.server.region)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles))
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.add_field(name="Channels", value=len(ctx.message.server.channels))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def leave(ctx):
    if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '397745647723216898':
        if ctx.message.author != bot.user:
            await bot.leave_server(ctx.message.server)
        else:
            await bot.say(":x: No Perms")
    else:
        await bot.say("To low perms")

@bot.command(pass_context=True)
async def remove_all_servers(ctx):
    if ctx.message.author.id == '279714095480176642':
        tmp = bot.servers
        for server in tmp:
            await bot.leave_server(server)
        await bot.say("Operation completed")

@bot.command(pass_context=True)
async def say(ctx, *, message):
    if ctx.message.author.id == bot.user.id:
        return
    else:
        await bot.say(message)

@bot.command(pass_context=True)
async def reboot(ctx):
    if not (ctx.message.author.id == '279714095480176642' or ctx.message.author.id == '449641568182206476'):
        return await bot.say(":x: You **Must** Be Bot Owner Or Developer")
    await bot.logout()
@bot.event
async def on_message(message):
    await bot.process_commands(message)





bot.loop.create_task(webupdate())
bot.run(os.getenv('TOKEN'))
