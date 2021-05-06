"""
Copyright (C) 2021  Berat Gökgöz

This file is a part of Timetable project.

Timetable is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or any
later version.

Timetable is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import random as rd
import discord
import sys, os, platform
import time

characterSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"


async def token(ctx):
    faketoken = ""
    for i in range(25):
        faketoken = faketoken + rd.choice(characterSet)
    faketoken = faketoken + '.'
    for i in range(6):
        faketoken = faketoken + rd.choice(characterSet)
    faketoken = faketoken + '.'
    for i in range(27):
        faketoken = faketoken + rd.choice(characterSet)
    await ctx.channel.send(f"Here is my token:\n{faketoken}")



async def stats(ctx, startuptime, bot, db):
    statsembed = discord.Embed(title="Stats",colour=0xACB6C4)
    platform1 = sys.platform
    cpuinfo="Unknown"
    if platform1 == "darwin":
        platform1 = "<:appl:833599104944570398>  MacOS"
        cpuinfo = os.popen("sysctl -n machdep.cpu.brand_string").read()
    elif platform1 == "linux":
        cpuinfo = os.popen("cat /proc/cpuinfo | grep 'model name'").read().split("\n")[0].split(':')[1].strip()
        platform1 = "<:tux:833598721219624972>  Linux"
    elif platform1 == "win32":
        cpuinfo = platform.processor()
        platform1 = "<:win10:833599311207727114>  Windows"
    else:
        platform1 = sys.platform.title()
        cpuinfo = platform.processor()
    uptime = int(time.time()-startuptime)
    uptimedays = uptime//(24*60*60)
    uptime = uptime-((uptime//(24*60*60))*(24*60*60))
    uptimehours = uptime//(60*60)
    uptime = uptime-((uptime//(60*60))*(60*60))
    uptimemins = uptime//60
    statsembed.add_field(name="OS",value=platform1)
    statsembed.add_field(name="Servers",value="<:serverinsights:833606061658341417>  "+str(len(bot.guilds)))
    statsembed.add_field(name="Python Version",value="<:py:833598476100829194>  "+sys.version[:5])
    statsembed.add_field(name="D.py Version",value="<:dpy:833597765321097226>  "+discord.__version__[:5])
    statsembed.add_field(name="Uptime",value="<:clockicon:833599517747576862>  "+str(uptimedays)+"d, "+str(uptimehours)+"h, "+str(uptimemins)+"m")
    statsembed.add_field(name="Shards",value="1")
    statsembed.add_field(name="Timetables",value="<:timetable:834285443196518410>  "+str(len(db.getTableIds())))
    statsembed.add_field(name="Active Reminders",value="⏰ "+str(len(db.getReminders())))
    statsembed.add_field(name="Commands",value=str(len(bot.commands)-2))
    statsembed.add_field(name="CPU",value="<:cpu:833632344534941747>  "+cpuinfo)
    await ctx.channel.send(embed=statsembed)


async def suggest(ctx, suggestion_text, bot):
    channel = bot.get_channel(839461823375081483)
    await channel.send(embed=discord.Embed(
        title=f"Suggestion by {ctx.author.name}#{ctx.author.discriminator}",
        description=suggestion_text,
        colour=0xACB6C4))
    await ctx.channel.send("Your suggestion has sent to bot's support server!")


async def report(ctx, report_text, bot):
    channel = bot.get_channel(838770130146033674)
    await channel.send(embed=discord.Embed(
        title=f"Bug Report by {ctx.author.name}#{ctx.author.discriminator}",
        description=report_text,
        colour=0xACB6C4))
    await ctx.channel.send("Your bug report has sent to bot's support server!")


async def support(ctx):
    await ctx.channel.send(embed=discord.Embed(
    title="Support",
    description="If you didn't understand how to use the bot, you can join our support server:\n\
[Join](https://https://discord.gg/btaGQ6zB6u)",
    colour=0xACB6C4
    ))
