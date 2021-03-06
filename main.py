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

import discord
from discord.ext import commands
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
import urllib.request as url
from urllib.parse import quote
import random as rd
import sys, re, os, platform, json, asyncio, time

import timetable as timetablefile
import reminder as reminderfile
import promotion, utils
import database as datab
from plotting import plottable
from botlists import BotLists

startuptime = time.time()

f=open("./secret/token.txt", 'r')
TOKEN = f.read()
f.close()
db = datab.Connection()
botlistsmanager = BotLists(db)
botUserId = "789202881336311849"
ownerId = 754327007331876945
hugeregex = r'(((([012]\d)|(\d)|(30))[/.-](([0][469])|([1][1])))|((([012]\d)|(\d)|(3[01]))[/.-](([0][13578])|([1][02])))|((([01]\d)|(\d)|([2][012345678]))[/.-]((02)|(2))))[/.-]((20[2][123456789])|(20[3456789]\d))'
timeregex = r'(([01][0123456789])|(\d)|([2][0123]))[:.]([012345]\d)'
characterSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_"

def getDayTime(option):
    hour = str(dt.utcnow().hour)
    if len(hour)<2:
        hour = '0'+hour
    minute = str(dt.utcnow().minute)
    if len(minute)<2:
        minute = '0'+minute
    a = [dt.utcnow().weekday(), "t" + hour + "_" + minute]
    if option == "day":
        return a[0]
    elif option == "time":
        return a[1]
    else:
        return


def getDate(option="today"):
    if option=="today":
        date = str(dt.now().date()).split('-')
        date.reverse()
        date[0] = date[0].lstrip('0')
        date[1] = date[1].lstrip('0')
        date = "-".join(date)
        return date
    elif option=="tomorrow":
        date = str((dt.now()+timedelta(days=1)).date()).split('-')
        date.reverse()
        date[0] = date[0].lstrip('0')
        date[1] = date[1].lstrip('0')
        date = "-".join(date)
        return date
    else:
        return


def get_prefix_tuple(client, message):
    try:
        pf = db.getPrefix(message.guild.id)
    except:
        db.refresh()
        pf = db.getPrefix(message.guild.id)
    return (pf,
    f"{pf} ",
    f"<@!{botUserId}>",
    f"<@{botUserId}>")


def get_prefix(client, message):
    pf = db.getPrefix(message.guild.id)
    return pf


async def runReminders():
    global db
    while True:
        reminders = db.getReminders()
        currentdate = getDate()
        currenttime = getDayTime("time")
        timeOf = {}
        for rid, r in reminders.items():
            if r[0] == currentdate and r[1] == currenttime[1:]:
                timeOf[rid] = r
        for rid, r in timeOf.items():
            try:
                notificationChannel = bot.get_channel(r[2])
            except Exception as e:
                print(e)
                timeOf.pop(rid)
            lang = db.getLang(notificationChannel.guild.id)
            f = open("./languages/"+lang+".json", 'r')
            strings = json.load(f)
            f.close()
            await notificationChannel.send(strings["announcements"] + r[3].strip() + '.')
            db.delReminder(rid)
        await asyncio.sleep(10)



async def runTimetable(tableid):
    global db
    dataframe = db.getTable(tableid)
    while True:
        if getDayTime("time") in dataframe.columns:
            try:
                infos = db.getTableInfos(tableid)
            except Exception as e:
                print(e)
                break
            try:
                notificationChannel = bot.get_channel(infos["channel"])
                peopleToMention = infos["mention"]
            except:
                continue
            currentDay = getDayTime("day")
            currentTime = str(getDayTime("time"))
            if dataframe.at[currentDay, currentTime].lower().strip() == 'nope':
                await asyncio.sleep(30)
                continue
            else:
                try:
                    lang = db.getLang(notificationChannel.guild.id)
                    f = open("./languages/"+lang+".json", 'r')
                    strings = json.load(f)
                    f.close()
                    await notificationChannel.send(peopleToMention+"  "+strings["announcements"]+str(dataframe.at[currentDay, currentTime]).strip()+'.')
                except AttributeError:
                    break
                await asyncio.sleep(60)
        else:
            await asyncio.sleep(30)

bot = commands.Bot(command_prefix=get_prefix_tuple, help_command=None)


@bot.event
async def on_ready():
    global db
    global botlistsmanager
    prefixesdb = dict(db.getPrefixes())
    for g in bot.guilds:
        if g.id in prefixesdb.keys():
            pass
        else:
            db.addServer(g.id, "t.", "en")
    for g in prefixesdb.keys():
        if not g in tuple(map(lambda x: x.id, bot.guilds)):
            db.delServer(g)
    await bot.change_presence(activity=discord.Game("t.help"))
    tableIds = db.getTableIds()
    tabletasks=[]
    resp = await botlistsmanager.session.get("https://covid19.who.int/WHO-COVID-19-global-table-data.csv",
        headers={ "User-Agent": "Mozilla/5.0" })
    resp = await resp.text()
    os.system("type nul > covid.csv")
    f = open("covid.csv",'w')
    print(resp, file=f)
    f.close()
    tabletasks.append(asyncio.create_task(runReminders()))
    for t in tableIds:
        tabletasks.append(asyncio.create_task(runTimetable(t)))
    print("Bot is ready!")
    await botlistsmanager.postServerCount(len(bot.guilds))
    await asyncio.gather(*tabletasks)


@bot.event
async def on_message(message):
    global db
    if message.content == f"<@{botUserId}>" or message.content == f"<@!{botUserId}>":
        lang = db.getLang(message.guild.id)
        f = open("./languages/"+lang+".json", 'r')
        strings = json.load(f)
        f.close()
        await message.channel.send(strings["prefixforthisserver"]+'"'+get_prefix(None,message)+'"')
    elif message.content.startswith(get_prefix(None,message)+"eval"):
        await runcode(message, message.content.split(get_prefix(None,message)+"eval ")[1].strip().strip("\t").strip("\n"))
    else:
        try:
            await bot.process_commands(message)
        except:
            db.refresh()
            await bot.process_commands(message)


@bot.command()
async def support(ctx):
    global db
    await utils.support(ctx, db)


@bot.command()
async def suggest(ctx, *text):
    global db
    suggestion_text = ' '.join(text)
    if suggestion_text == '' or suggestion_text.isspace():
        f = open("./languages/"+db.getLang(ctx.guild.id)+".json", 'r')
        strings = json.load(f)
        f.close()
        await ctx.channel.send(strings["suggestwarning"].replace("<prefix>", get_prefix(None, ctx)))
        return
    await utils.suggest(ctx, suggestion_text, bot, db)


@bot.command()
async def report(ctx, *text):
    global db
    report_text = ' '.join(text)
    if report_text == '' or report_text.isspace():
        f = open("./languages/" + db.getLang(ctx.guild.id) + ".json", 'r')
        strings = json.load(f)
        f.close()
        await ctx.channel.send(strings["reportwarning"].replace("<prefix>", get_prefix(None, ctx)))
        return
    await utils.report(ctx, report_text, bot, db)


@bot.event
async def on_guild_join(sv):
    global db
    global botlistsmanager
    db.addServer(sv.id, "t.", "en")
    channel = sv.system_channel
    if channel != None:
        await channel.send(embed=discord.Embed(description="Thanks for adding me to your server! My default prefix is `t.` and to see my commands, use `t.help`\n\
I hope that you love me and don't kick me after a few minutes after I joined. Let me explain what you can do with me:\n\
You can create your timetables and be informed when a lesson, online meeting, or any useless(!) event has started,\n\
You can learn your next event today,\n\
You can see your weekly timetable\n\
You can be notified on events you set a reminder,\n\
and much more...\n\
If you love me, please don't forget to add me on your other servers, join to my support server and vote me on bot list websites!",
            colour=0xACB6C4))
    else:
        for ch in sv.text_channels:
            try:
                await ch.send(embed=discord.Embed(description="Thanks for adding me to your server! My default prefix is `t.` and to see my commands, use `t.help`\n\
I hope that you love me and don't kick me after a few minutes after I joined. Let me explain what you can do with me:\n\
You can create your timetables and be informed when a lesson, online meeting, or any useless(!) event has started,\n\
You can learn your next event today,\n\
You can see your weekly timetable\n\
You can be notified on events you set a reminder,\n\
and much more...\n\
If you love me, please don't forget to add me on your other servers, join to my support server and vote me on bot list websites!",
                    colour=0xACB6C4))
                break
            except:
                pass
    logchannel = bot.get_channel(839766392156717056)
    msg = await logchannel.send(f"Bot joined to a new server: {sv.name}")
    await msg.add_reaction('🎉')
    await botlistsmanager.postServerCount(len(bot.guilds))

@bot.event
async def on_guild_remove(sv):
    global db
    global botlistsmanager
    db.delServer(sv.id)
    logchannel = bot.get_channel(839766392156717056)
    msg = await logchannel.send(f"Bot removed from a server: {sv.name}")
    await msg.add_reaction('😳')
    await botlistsmanager.postServerCount(len(bot.guilds))


@bot.command()
async def token(ctx):
    global db
    await utils.token(ctx, db)


@bot.command()
async def contribute(ctx):
    global db
    await promotion.contribute(ctx, db)


@bot.command(aliases=("stat","statistics"))
async def stats(ctx):
    await utils.stats(ctx,startuptime,bot,db)

@bot.command()
async def invite(ctx):
    global db
    await promotion.invite(ctx, db)

@bot.command()
async def vote(ctx):
    global db
    await promotion.vote(ctx, db)

@bot.command(aliases=("tt",))
async def timetable(ctx):
    global db
    await timetablefile.timetable(ctx,bot,db,runTimetable)


@bot.command()
async def show(ctx, tableid=None):
    global db
    global botlistsmanager
    await plottable(ctx, db, tableid, get_prefix, botlistsmanager)


@bot.command(aliases=('h',))
async def help(ctx, helpTopic=""):
    global db
    helpTopic = helpTopic.lower().strip()
    file = open(f"./languages/help_{db.getLang(ctx.guild.id)}.json",'r')
    helpcommands = json.load(file)
    if helpTopic in helpcommands:
        if helpTopic == "thereisnocommand":
            await ctx.channel.send(helpcommands["thereisnocommand"])
            return
        helpembed = discord.Embed(title=helpcommands[helpTopic][0],description=helpcommands[helpTopic][1].replace("<prefix>",get_prefix(None,ctx)),colour=0xACB6C4)
        for field in helpcommands[helpTopic][2:]:
            helpembed.add_field(name=field[0], value=field[1], inline=field[2] if len(field) > 2 else True)
        await ctx.channel.send(embed=helpembed)
    else:
        await ctx.channel.send(helpcommands["thereisnocommand"])
    file.close()


@bot.command()
async def delete(ctx, tid=None):
    global db
    lang = db.getLang(ctx.guild.id)
    f = open("./languages/" + lang + ".json", 'r')
    strings = json.load(f)
    f.close()
    if tid == '' or tid == None:
        await ctx.channel.send(embed=discord.Embed(
        description=strings["delete"][0].replace("<prefix>", get_prefix(None,ctx)),
        colour=0xACB6C4
        ))
        return
    try:
        realPassword = db.getTableInfos(tid)["password"]
    except:
        await ctx.channel.send(strings["cantsee"])
        return
    await ctx.channel.send(strings["delete"][2])
    try:
        getpassword = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings["enterpassword"])
        return
    password = getpassword.content.strip("||").strip()
    try:
        await getpassword.delete()
    except:
        await ctx.channel.send(strings["timetable"][19])
    if password==realPassword:
        db.delTable(tid)
        await ctx.channel.send(strings["delete"][2].replace("{tid}", tid))
    else:
        await ctx.channel.send(strings["wrongpassword"])


@bot.command()
async def changemention(ctx, tid=None, *mentions):
    global db
    strings = json.load(open("./languages/"+db.getLang(ctx.guild.id)+".json", 'r'))
    if tid == None or tid == '':
        await ctx.channel.send(embed=discord.Embed(
        description=strings["changemention"][0].replace("<prefix>", get_prefix(None,ctx)),
        colour=0xACB6C4
        ))
        return
    mention = ' '.join(mentions)
    if mentions.find("@everyone") > -1 or mentions.find("@here") > -1:
        await ctx.channel.send(strings["timetable"][17])
        return
    try:
        tableInfos = db.getTableInfos(tid)
    except:
        await ctx.channel.send(strings["cantsee"])
        return
    realPassword = tableInfos["password"]
    channelid = tableInfos["channel"]
    await ctx.channel.send(strings["enterpassword"])
    try:
        getpassword = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings["timetable"][2])
        return
    password = getpassword.content.strip("||").strip()
    try:
        await getpassword.delete()
    except:
        await ctx.channel.send(strings["timetable"][19])
    if password == realPassword:
        db.changeTableInfo(tid, channelid, realPassword, mention)
        if mention.isspace() or mention == '':
            await ctx.channel.send(strings["changemention"][1].replace("{tid}", tid))
        else:
            await ctx.channel.send(strings["changemention"][2].replace("{tid}", tid).replace("{mention}", mention))
    else:
        await ctx.channel.send(strings["wrongpassword"])


@bot.command()
async def changechannel(ctx, tid=None, channel=None):
    global db
    strings = json.load(open("./languages/"+db.getLang(ctx.guild.id)+".json", 'r'))
    if tid == '' or tid == None or channel == '' or channel == None:
        await ctx.channel.send(embed=discord.Embed(
        description=strings["changechannel"][0].replace("<prefix>", get_prefix(None,ctx)),
        colour=0xACB6C4
        ))
        return
    channelid = int(channel.strip('<').strip('>').strip('#'))
    try:
        tableInfos = db.getTableInfos(tid)
    except:
        await ctx.channel.send(strings["cantsee"])
        return
    realPassword = tableInfos["password"]
    mention = tableInfos["mention"]
    await ctx.channel.send(strings["enterpassword"])
    try:
        getpassword = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings["timetable"][2])
        return
    password = getpassword.content.strip("||").strip()
    try:
        await getpassword.delete()
    except:
        await ctx.channel.send(strings["timetable"][19])
    if password == realPassword:
        db.changeTableInfo(tid, channelid, realPassword, mention)
        await ctx.channel.send(strings["changechannel"][2]
            .replace("{tid}", tid)
            .replace("{channelid}", channelid))
    else:
        await ctx.channel.send(strings[wrongpassword])

@bot.command(aliases=("corona",))
async def covid(ctx, cmd=None, *args):
    global botlistsmanager
    global db
    await utils.covid(ctx, cmd, args, get_prefix, botlistsmanager, db)

@bot.command()
async def changepassword(ctx, tid=None):
    global db
    strings = json.load(open("./languages/"+db.getLang(ctx.guild.id)+".json", 'r'))
    if tid == '' or tid == None:
        await ctx.channel.send(embed=discord.Embed(
        description=strings["changepassword"][0].replace("<prefix>", get_prefix(None,ctx)),
        colour=0xACB6C4
        ))
        return
    try:
        tableInfos = db.getTableInfos(tid)
    except:
        await ctx.channel.send(strings["cantsee"])
        return
    channelid = tableInfos["channel"]
    realPassword = tableInfos["password"]
    mention = tableInfos["mention"]
    await ctx.channel.send(strings["enterpassword"])
    try:
        getpassword = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings["timetable"][2])
        return
    password = getpassword.content.strip("||").strip()
    try:
        await getpassword.delete()
    except:
        await ctx.channel.send(strings["timetable"][19])
    if password == realPassword:
        await ctx.channel.send(strings["changepassword"][1])
        try:
            getnewpassword = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
        except asyncio.TimeoutError:
            await ctx.channel.send(strings["timetable"][2])
            return
        newpassword = getnewpassword.content
        await getnewpassword.delete()
        db.changeTableInfo(tid, channelid, newpassword, mention)
        await ctx.channel.send(strings["changepassword"][2].replace("{tid}",tid))
    else:
        await ctx.channel.send(strings["wrongpassword"])



@bot.command(aliases=("dl",))
async def download(ctx, tid=None):
    global db
    global botlistsmanager
    strings = json.load(open("./languages/"+db.getLang(ctx.guild.id)+".json", 'r'))
    if not await botlistsmanager.isVoted(ctx.author.id):
        await ctx.channel.send(embed=discord.Embed(title=strings["votetouse"][0], description=strings["votetouse"][1], colour=0xACB6C4))
        return
    if tid == '' or tid == None:
        await ctx.channel.send(embed=discord.Embed(
        description=strings["download"].replace("<prefix>", get_prefix(None,ctx)),
        colour=0xACB6C4
        ))
        return
    try:
        re.match(r'[123456789](\d){5}', tid)
        if re.match == None:
            await ctx.channel.send(embed=discord.Embed(
            description=strings["download"].replace("<prefix>", get_prefix(None,ctx)),
            colour=0xACB6C4
            ))
            return
        tableDf = db.getTable(tid)
    except:
        await ctx.channel.send(strings["cantsee"])
        return
    tableDf.columns = list(map(lambda x: x.lstrip('t').replace('_',':'), tableDf.columns))
    tableDf.to_csv(f"table-{tid}.csv", sep=';', index=False)
    await ctx.channel.send(file=discord.File(f"table-{tid}.csv"))
    os.remove(f"table-{tid}.csv")


@bot.command()
async def exit(ctx):
    global db
    if int(ctx.author.id) != ownerId:
        return
    else:
        db.disconnect()
        exit()


async def runcode(ctx, codeblock):
    if int(ctx.author.id) != ownerId:
        return
    else:
        #print(code)
        startTime = time.time()
        err = None
        resp = None
        codeblockregex = r"`{3}([a-zA-Z0-9\-+]*)(.*)`{3}"
        code = '\n'.join(re.search(codeblockregex, codeblock, re.DOTALL)
        .group()
        .strip(r'```')
        .strip('\n')
        .strip()
        .split('\n')[1:])
        try:
            print(code)
            exec("async def EvalCode(ctx,bot,db):\n"+'\n'.join(map(lambda x: '    '+x, code.split('\n'))),
            globals())
            resp = await EvalCode(ctx,bot,db)
            err = None
        except Exception as e:
            err = e
        endTime = time.time()
        executionTime = endTime-startTime
        responseEmbed = discord.Embed(title="Eval",colour=0xACB6C4)
        if err is not None:
            responseEmbed.add_field(name="Error", value=f"```{str(err)}```")
        if resp is not None:
            responseEmbed.add_field(name="Return", value=f"```{str(resp)}```", inline=False)
        responseEmbed.add_field(name="Time", value=f"`{str(executionTime)}` secs",inline=False)
        await ctx.channel.send(embed=responseEmbed)


@bot.command()
async def countdown(ctx, seconds=None, *name):
    global db
    strings = json.load(open("./languages/"+db.getLang(ctx.guild.id)+".json", 'r'))
    if seconds == '' or seconds == None or name == tuple():
        await ctx.channel.send(embed=discord.Embed(
        description=strings["countdown"][0].replace("<prefix>", get_prefix(None, ctx)),
        colour=0xACB6C4
        ))
        return
    try:
        secs = int(seconds)
    except:
        await ctx.channel.send(strings["countdown"][1])
        return
    if secs > (24*60*60):
        await ctx.channel.send(strings["countdown"][2])
        return
    eventname = ' '.join(name)
    if eventname.find("@everyone") > -1 or eventname.find("@here") > -1:
        await ctx.channel.send(strings["timetable"][17])
        return
    if eventname == '' or eventname.isspace():
        await ctx.channel.send(strings["countdown"][0])
        return
    await asyncio.sleep(secs)
    await ctx.channel.send(strings["countdown"][3].replace("{author}", ctx.author.id).replace("{eventname}", eventname))


@bot.command()
async def reminder(ctx, cmd=None, *args):
    global db
    global botlistsmanager
    strings = json.load(open("./languages/"+db.getLang(ctx.guild.id)+".json", 'r'))
    if not await botlistsmanager.isVoted(ctx.author.id):
        await ctx.channel.send(embed=discord.Embed(title=strings["votetouse"][0], description=strings["votetouse"][1], colour=0xACB6C4))
        return
    await reminderfile.reminder(ctx, cmd, args, bot, db, getDate, getDayTime, get_prefix)


@bot.command(aliases=("changeprefix","setprefix"))
async def prefix(ctx, pf=''):
    global db
    strings = json.load(open("./languages/"+db.getLang(ctx.guild.id)+".json", 'r'))
    if ctx.author.guild_permissions.manage_guild:
        if pf == '' or pf.isspace():
            await ctx.channel.send(strings["prefix"][0].replace("<prefix>", get_prefix(None,ctx)))
            return
        else:
            db.changePrefix(ctx.guild.id, pf)
            await ctx.channel.send(strings["prefix"][1].replace("{pf}", pf))
    else:
        await ctx.channel.send(strings["prefix"][2])

@bot.command(aliases=("server","si","server-info"))
async def serverinfo(ctx):
    global db
    global botlistsmanager
    strings = json.load(open("./languages/"+db.getLang(ctx.guild.id)+".json", 'r'))
    if not await botlistsmanager.isVoted(ctx.author.id):
        await ctx.channel.send(embed=discord.Embed(title=strings["votetouse"][0], description=strings["votetouse"][2], colour=0xACB6C4))
        return
    await utils.serverinfo(ctx, db)

@bot.command()
async def next(ctx, tid=None):
    global db
    global botlistsmanager
    strings = json.load(open("./languages/"+db.getLang(ctx.guild.id)+".json", 'r'))
    if not await botlistsmanager.isVoted(ctx.author.id):
        await ctx.channel.send(embed=discord.Embed(title=strings["votetouse"][0], description=strings["votetouse"][1], colour=0xACB6C4))
        return
    if tid == '' or tid == None:
        await ctx.channel.send(embed=discord.Embed(
        description=strings["next"][0].replace("<prefix>", get_prefix(None, ctx)),
        colour=0xACB6C4
        ))
        return
    try:
        tableDf = db.getTable(tid)
    except:
        await ctx.channel.send(strings["cantsee"])
        return
    timestamps = list(map(
        lambda x: (dt.strptime(x+f" {dt.utcnow().year}_{('0' if len(str(dt.utcnow().month))<2 else '')+str(dt.utcnow().month)}_{('0' if len(str(dt.utcnow().day))<2 else '')+str(dt.utcnow().day)}",
        "t%H_%M %Y_%m_%d")).timestamp(),
        tableDf.columns))
    while True:
        try:
            nexttime = min(list(filter(lambda x: x>dt.utcnow().timestamp(), timestamps)))
        except ValueError:
            await ctx.channel.send(strings["next"][10])
            return
        nextevent = tableDf.at[dt.utcnow().weekday(), dt.fromtimestamp(nexttime).strftime("t%H_%M")]
        if str(nextevent).lower() == "nope":
            timestamps.remove(nexttime)
            continue
        else:
            break
    await ctx.channel.send(embed=discord.Embed(
        title=strings["next"][1],
        description=f"{strings['next'][2]} {nextevent}\n\
{strings['next'][3]} {dt.fromtimestamp(nexttime).strftime('%H:%M.')} UTC\n\
{strings['next'][4]} {int((nexttime-dt.utcnow().timestamp())//(60*60)) if (nexttime-dt.utcnow().timestamp())//(60*60) > 0 else ''} \
{strings['next'][5]+', ' if (nexttime-dt.utcnow().timestamp())//(60*60)>1 else ''}\
{strings['next'][6]+', ' if (nexttime-dt.utcnow().timestamp())//(60*60) == 1 else ''}\
{int(((nexttime-dt.utcnow().timestamp())-((nexttime-dt.utcnow().timestamp())//(60*60)*60*60))//60)} \
{strings['next'][7] if ((nexttime-dt.utcnow().timestamp())-((nexttime-dt.utcnow().timestamp())//(60*60)))//60 > 1 else strings['next'][8]}\
 {strings['next'][9]}.",
        colour=0xACB6C4))


bot.run(TOKEN)
