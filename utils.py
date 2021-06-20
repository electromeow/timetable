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
import pandas as pd
import sys, os, platform, json
import time

characterSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"


async def token(ctx,db):
    lang = db.getLang(ctx.guild.id)
    f = open("./languages/"+lang+".json", 'r')
    strings = json.load(f)
    f.close()
    faketoken = ""
    for i in range(25):
        faketoken = faketoken + rd.choice(characterSet)
    faketoken = faketoken + '.'
    for i in range(6):
        faketoken = faketoken + rd.choice(characterSet)
    faketoken = faketoken + '.'
    for i in range(27):
        faketoken = faketoken + rd.choice(characterSet)
    await ctx.channel.send(strings["hereismytoken"]+faketoken)



async def stats(ctx, startuptime, bot, db):
    lang = db.getLang(ctx.guild.id)
    f = open("./languages/"+lang+".json", 'r')
    strings = json.load(f)
    strings = strings["stats"]
    f.close()
    statsembed = discord.Embed(title=strings[11],colour=0xACB6C4)
    platform1 = sys.platform
    if platform1 == "darwin":
        platform1 = "<:appl:833599104944570398>  MacOS"
        cpuinfo = os.popen("sysctl -n machdep.cpu.brand_string").read()
    elif platform1 == "linux":
        cpuinfo = os.popen("cat /proc/cpuinfo | grep 'model name'").read().split("\n")[0].split(':')[1].strip()
        platform1 = "<:tux:833598721219624972>  Linux"
    elif platform1.startswith("win"):
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
    statsembed.add_field(name=strings[0],value=platform1)
    statsembed.add_field(name=strings[1],value="<:serverinsights:833606061658341417>  "+str(len(bot.guilds)))
    statsembed.add_field(name=strings[2],value="<:py:833598476100829194>  "+sys.version[:5])
    statsembed.add_field(name=strings[3],value="<:dpy:833597765321097226>  "+discord.__version__[:5])
    statsembed.add_field(name=strings[4],value="<:clockicon:833599517747576862>  "+str(uptimedays)+strings[10][0]+str(uptimehours)+strings[10][1]+str(uptimemins)+strings[10][2])
    statsembed.add_field(name=strings[5],value="1")
    statsembed.add_field(name=strings[6],value="<:timetable:834285443196518410>  "+str(len(db.getTableIds())))
    statsembed.add_field(name=strings[7],value="⏰ "+str(len(db.getReminders())))
    statsembed.add_field(name=strings[8],value=str(len(bot.commands)-2))
    statsembed.add_field(name=strings[9],value="<:cpu:833632344534941747>  "+cpuinfo)
    await ctx.channel.send(embed=statsembed)


async def suggest(ctx, suggestion_text, bot, db):
    channel = bot.get_channel(839461823375081483)
    await channel.send(embed=discord.Embed(
        title=f"Suggestion by {ctx.author.name}#{ctx.author.discriminator}",
        description=suggestion_text,
        colour=0xACB6C4))
    lang = db.getLang(ctx.guild.id)
    f = open("./languages/"+lang+".json", 'r')
    strings = json.load(f)
    f.close()
    await ctx.channel.send(strings["suggestionsent"])


async def report(ctx, report_text, bot, db):
    channel = bot.get_channel(838770130146033674)
    await channel.send(embed=discord.Embed(
        title=f"Bug Report by {ctx.author.name}#{ctx.author.discriminator}",
        description=report_text,
        colour=0xACB6C4))
    lang = db.getLang(ctx.guild.id)
    f = open("./languages/"+lang+".json", 'r')
    strings = json.load(f)
    f.close()
    await ctx.channel.send(strings["reportsent"])


async def support(ctx, db):
    lang = db.getLang(ctx.guild.id)
    f = open("./languages/"+lang+".json", 'r')
    strings = json.load(f)
    strings = strings["support"]
    f.close()
    await ctx.channel.send(embed=discord.Embed(
    title=strings[0],
    description=strings[1],
    colour=0xACB6C4
    ))

async def covid(ctx, cmd, args, get_prefix,botlistsmanager, db):
    lang = db.getLang(ctx.guild.id)
    f = open("./languages/"+lang+".json", 'r')
    strings = json.load(f)
    f.close()
    if not await botlistsmanager.isVoted(ctx.author.id):
        await ctx.channel.send(embed=discord.Embed(title=strings["votetouse"][0], description=strings["votetouse"][1], colour=0xACB6C4))
        return
    strings = strings["covid"]
    if cmd == None or cmd == '':
        await ctx.channel.send(strings[0].replace("<prefix>", get_prefix(None,ctx)))
        return
    comd = cmd.lower().strip()
    covidDf = pd.read_csv("covid.csv")
    if comd == strings[1]:
        top10embed = discord.Embed(title="<:covid:840510471547125760>  "+strings[2],colour=0xACB6C4)
        top10embed.add_field(name=strings[3], value='\n'.join([str(x) for x in range(1,11)]))
        top10embed.add_field(name=strings[4], value='\n'.join(covidDf.iloc[1:11,0].values))
        top10embed.add_field(name=strings[5], value='\n'.join(map(lambda x: str(x), covidDf.iloc[1:11,2].values)))
        top10embed.add_field(name="_ _", value=strings[6], inline=False)
        await ctx.channel.send(embed=top10embed)


    elif comd in strings[8]:
        if len(args) < 1 and comd != strings[8][2]:
            await ctx.channel.send(stringd[7].replace("<prefix>", get_prefix(None,ctx)))
            return
        if len(args) >= 1:
            if args[0].lower().strip() == strings[8][2]:
                await ctx.channel.send(strings[9].replace("<prefix>", get_prefix(None,ctx)))
                return
        if comd != strings[8][2]:
            f = open("countrycodes.json",'r')
            countrycodes = json.load(f)
            f.close()
            countryData = covidDf.loc[covidDf["Name"] == ' '.join(args).title()]
            print(countryData)
            countryName = ' '.join(args).title()
            if len(countryData.index) < 1:
                try:
                    countryName = countrycodes[' '.join(args).upper()]
                    countryData = covidDf.loc[covidDf["Name"] == countryName]
                    if len(set(countryData.index)) < 1:
                        raise Exception("unneeded")
                except:
                    await ctx.channel.send(strings[10])
                    return
            countryembed = discord.Embed(title="<:covid:840510471547125760>  "+strings[11].replace("{country}",countryName.replace('[1]','')), colour=0xACB6C4)

        else:
            countryData = covidDf.loc[covidDf["Name"] == "Global"]
            countryembed = discord.Embed(title="<:covid:840510471547125760>  "+strings[21], colour=0xACB6C4)
        countryembed.add_field(name=strings[13], value=countryData.iloc[:,2].values[0])
        countryembed.add_field(name=strings[14], value=countryData.iloc[:,6].values[0])
        countryembed.add_field(name=strings[15], value=countryData.iloc[:,4].values[0])
        countryembed.add_field(name=strings[16], value=str(round(countryData.iloc[:,3].values[0]/1000,4))+'%')
        countryembed.add_field(name=strings[17], value=countryData.iloc[:,4].values[0])
        countryembed.add_field(name=strings[18], value=countryData.iloc[:,11].values[0])
        countryembed.add_field(name=strings[19], value=countryData.iloc[:,9].values[0])
        countryembed.add_field(name="_ _", value=strings[6], inline=False)
        await ctx.channel.send(embed=countryembed)
    else:
        await ctx.channel.send(strings[20].replace("<prefix>", get_prefix(None,ctx)))


async def serverinfo(ctx, db):
    strings = json.load(open("./languages/"+db.getLang(ctx.guild.id)+".json", 'r'))["serverinfo"]
    svinfoembed = discord.Embed(title=ctx.guild.name, colour=0xACB6C4)
    svinfoembed.add_field(name="<:textchannel:844257666174943253>  "+strings[0], value=str(len(ctx.guild.text_channels)))
    svinfoembed.add_field(name="<:voicechannel:844257666141519882>  "+strings[1], value=str(len(ctx.guild.voice_channels)))
    svinfoembed.add_field(name="<:stagechannel:844262408134721576>  "+strings[2], value=str(len(ctx.guild.stage_channels)))
    svinfoembed.add_field(name="<:ruleschannel:844264338427871312>  "+strings[3], value=('<#'+str(ctx.guild.rules_channel.id)+'>') if ctx.guild.rules_channel!=None else "Nope")
    boostcount = ctx.guild.premium_subscription_count
    if boostcount >= 0 and boostcount < 2:
        boostlevel = strings[11]
    elif boostcount >= 3 and boostcount < 15:
        boostlevel = strings[12]+" 1"
    elif boostcount >= 16 and boostcount < 30:
        boostlevel = strings[12]+" 2"
    elif boostcount >= 30:
        boostlevel = strings[12]+" 3"
    svinfoembed.add_field(name="<:boost:856046472947695636>  "+strings[8], value=str(boostcount)+"\n"+boostlevel)
    svinfoembed.add_field(name="<:members:844268367950774282>  "+strings[4], value=str(ctx.guild.member_count))
    guildCreation = ctx.guild.created_at
    svinfoembed.add_field(name="📅  "+strings[5], value=f"{guildCreation.day}/{guildCreation.month}/{guildCreation.year} {guildCreation.hour}:{guildCreation.minute}")
    svinfoembed.add_field(name="<:discordid:844272660291518484>  "+strings[6], value=str(ctx.guild.id))
    svinfoembed.add_field(name="😆  "+strings[9], value=str(len(ctx.guild.emojis)))
    svinfoembed.add_field(name="🔐  "+strings[10], value=("✅" if ctx.guild.mfa_level==1 else "❌"))
    svinfoembed.add_field(name="<:role:844274430375886907>  "+strings[7], value=str(len(ctx.guild.roles)))
    svinfoembed.set_thumbnail(url=str(ctx.guild.icon_url))
    await ctx.channel.send(embed=svinfoembed)
