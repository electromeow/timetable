import discord
from discord.ext import commands
import asyncio
import pandas as pd
import database as datab
from datetime import datetime as dt
from datetime import timedelta
import urllib.request as url
from urllib.parse import quote
import json
import os
import time
import re
import random as rd


f=open("token.txt", 'r')
TOKEN = f.read()
f.close()
db = datab.Connection()
botUserId = "789202881336311849"
ownerId = 754327007331876945
hugeregex = r'(((([012]\d)|(\d)|(30))[/.-](([0][469])|([1][1])))|((([012]\d)|(\d)|(3[01]))[/.-](([0][13578])|([1][02])))|((([01]\d)|(\d)|([2][012345678]))[/.-]((02)|(2))))[/.-]((20[2][123456789])|(20[3456789]\d))'
timeregex = r'(([01][0123456789])|(\d)|([2][0123]))[:.]([012345]\d)'
characterSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.1234567890"

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


def get_prefix(client, message):
    return db.getPrefix(message.guild.id)

async def runReminders():
    global db
    while True:
        print("reminders are running")
        reminders = db.getReminders()
        print(reminders)
        currentdate = getDate()
        currenttime = getDayTime("time")
        print(currenttime, currentdate)
        timeOf = {}
        for rid, r in reminders.items():
            if r[0] == currentdate and r[1] == currenttime[1:]:
                timeOf[rid] = r
        print(timeOf)
        for rid, r in timeOf.items():
            try:
                notificationChannel = bot.get_channel(r[2])
            except Exception as e:
                print(e)
                timeOf.pop(rid)
            await notificationChannel.send("Hey, it is the time of " + r[3].strip() + '.')
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
                await notificationChannel.send(peopleToMention+"  Hey! It's the time of "+str(dataframe.at[currentDay, currentTime]).strip()+'.')
                await asyncio.sleep(60)
        else:
            await asyncio.sleep(30)

bot = commands.Bot(command_prefix=get_prefix, help_command=None)


@bot.event
async def on_ready():
    global db
    prefixesdb = dict(db.getPrefixes())
    for g in bot.guilds:
        if g.id in prefixesdb.keys():
            pass
        else:
            db.addPrefix(g.id, "t.")
    await bot.change_presence(activity=discord.Game("with your time"))
    tableIds = db.getTableIds()
    tabletasks=[]
    tabletasks.append(asyncio.create_task(runReminders()))
    for t in tableIds:
        tabletasks.append(asyncio.create_task(runTimetable(t)))
    await asyncio.gather(*tabletasks)


@bot.event
async def on_message(message):
    if message.content == f"<@{botUserId}>" or message.content == f"<@!{botUserId}>":
        await message.channel.send(f"Hey! My prefix for this server is \"{get_prefix(None,message)}\"")
    elif message.content.startswith(get_prefix(None,message)+"eval"):
        await runcode(message, message.content.split(get_prefix(None,message)+"eval ")[1].strip().strip("\t").strip("\n"))
    else:
        await bot.process_commands(message)


@bot.event
async def on_guild_join(sv):
    db.addPrefix(sv.id, "t.")


@bot.event
async def on_guild_remove(sv):
    db.delPrefix(sv.id)


@bot.command()
async def token(ctx):
    faketoken = ""
    for i in range(59):
        faketoken = faketoken + rd.choice(characterSet)
    await ctx.channel.send(f"Here is my token:\n{faketoken}")

@bot.command()
async def timetable(ctx):
    global db
    await ctx.channel.send("""Can you enter the times(in UTC) in your timetable seperated with commas? For example:
`09:00,09:40,10:20`""")
    try:
        ttLessontimes = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    ttLessontimes = ttLessontimes.content.replace(':', '_').replace('.', '_').split(",")
    ttLessontimes = list(map(lambda x: x.strip(), ttLessontimes))

    await ctx.channel.send("""Now you will enter the events on your timetable in order of times you entered for each day of the week.
You will pass "nope" for blank times. If you don't have any events on that day, you will pass a "nope".
First enter the events that you have on mondays:""")
    try:
        monday = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    if monday.content.lower() == "nope":
        monday = len(ttLessontimes)*["nope"]
    else:
        monday = monday.content.split(",")
        monday = list(map(lambda x: x.strip(), monday))
        if len(monday) > len(ttLessontimes):
            monday = monday[:len(ttLessontimes)]
        elif len(monday) < len(ttLessontimes):
            while len(monday) < len(ttLessontimes):

                monday.append("nope")
        else:
            pass

    monday = pd.DataFrame([monday], columns=ttLessontimes)

    await ctx.channel.send("""Enter the events that you have on tuesdays:""")
    try:
        tuesday = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    if tuesday.content.lower() == "nope":
        tuesday = len(ttLessontimes)*["nope"]
    else:
        tuesday = tuesday.content.split(",")
        tuesday = list(map(lambda x: x.strip(), tuesday))
        if len(tuesday) > len(ttLessontimes):
            tuesday = tuesday[:len(ttLessontimes)]
        elif len(tuesday) < len(ttLessontimes):
            while len(tuesday) < len(ttLessontimes):
                tuesday.append("nope")
        else:
            pass
    tuesday = pd.DataFrame([tuesday], columns=ttLessontimes)

    await ctx.channel.send("""Enter the events that you have on wednesdays:""")
    try:
        wednesday = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    if wednesday.content.lower() == "nope":
        wednesday = len(ttLessontimes) * ["nope"]
    else:
        wednesday = wednesday.content.split(",")
        wednesday = list(map(lambda x: x.strip(), wednesday))
        if len(wednesday) > len(ttLessontimes):
            wednesday = wednesday[:len(ttLessontimes)]
        elif len(wednesday) < len(ttLessontimes):
            while len(wednesday) < len(ttLessontimes):
                wednesday.append("nope")
        else:
            pass
    wednesday = pd.DataFrame([wednesday], columns=ttLessontimes)

    await ctx.channel.send("""Enter the events that you have on thursdays:""")
    try:
        thursday = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    if thursday.content.lower() == "nope":
        thursday = len(ttLessontimes) * ["nope"]
    else:
        thursday = thursday.content.split(",")
        thursday = list(map(lambda x: x.strip(), thursday))
        if len(thursday) > len(ttLessontimes):
            thursday = thursday[:len(ttLessontimes)]
        elif len(thursday) < len(ttLessontimes):
            while len(thursday) < len(ttLessontimes):
                thursday.append("nope")
        else:
            pass
    thursday = pd.DataFrame([thursday], columns=ttLessontimes)

    await ctx.channel.send("""Enter the events that you have on fridays:""")
    try:
        friday = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    if friday.content.lower() == "nope":
        friday = len(ttLessontimes) * ["nope"]
    else:
        friday = friday.content.split(",")
        friday = list(map(lambda x: x.strip(), friday))
        if len(friday) > len(ttLessontimes):
            friday = friday[:len(ttLessontimes)]
        elif len(friday) < len(ttLessontimes):
            while len(friday) < len(ttLessontimes):
                friday.append("nope")
        else:
            pass
    friday = pd.DataFrame([friday], columns=ttLessontimes)

    await ctx.channel.send("""Enter the events that you have on saturdays:""")
    try:
        saturday = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    if saturday.content.lower() == "nope":
        saturday = len(ttLessontimes) * ["nope"]
    else:
        saturday = saturday.content.split(",")
        saturday = list(map(lambda x: x.strip(), saturday))
        if len(saturday) > len(ttLessontimes):
            saturday = saturday[:len(ttLessontimes)]
        elif len(saturday) < len(ttLessontimes):
            while len(saturday) < len(ttLessontimes):
                saturday.append("nope")
        else:
            pass
    saturday = pd.DataFrame([saturday], columns=ttLessontimes)

    await ctx.channel.send("""Enter the events that you have on sundays:""")
    try:
        sunday = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    if sunday.content.lower() == "nope":
        sunday = len(ttLessontimes) * ["nope"]
    else:
        sunday = sunday.content.split(",")
        sunday = list(map(lambda x: x.strip(), sunday))
        if len(sunday) > len(ttLessontimes):
            sunday = sunday[:len(ttLessontimes)]
        elif len(sunday) < len(ttLessontimes):
            while len(sunday) < len(ttLessontimes):
                sunday.append("nope")
        else:
            pass
    sunday = pd.DataFrame([sunday], columns=ttLessontimes)

    timetable = pd.concat([monday, tuesday, wednesday, thursday, friday, saturday, sunday], ignore_index=True)
    print(timetable)
    def formattime(time):
        hour = str(time).split('_')[0]
        minute = str(time).split('_')[1]
        if len(hour) < 2:
            hour = '0'+hour
        if len(minute) < 2:
            minute = '0'+minute
        return hour+'_'+minute
    timetable.columns = list(map(formattime, timetable.columns))

    await ctx.channel.send("Mention or enter the id of the channel for notifications:")
    while True:
        try:
            notificationChannel = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
        except asyncio.TimeoutError:
            await ctx.channel.send("Command has canceled due to timeout.")
            return
        notificationChannel = int(notificationChannel.content.split()[0].strip('<').strip('>').strip('#'))
        try:
            testChannel = await bot.fetch_channel(notificationChannel)
            testMsg = await testChannel.send("Test")
            try:
                await testMsg.delete()
            except:
                pass
            break
        except discord.Forbidden:
            await ctx.channel.send("I don't have the permission to access or send message this channel or to delete messages from this channel.\nTry with another channel or give me the permission to access and send messages to that channel, then try again:")

    await ctx.channel.send("Mention the people or roles to inform, they will be mentioned when an event has started:")
    try:
        getmention = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    mention = getmention.content

    await ctx.channel.send("Lastly enter a password for your timetable that others can't change it. You can also send it as a spoiler. Message will be immediately deleted.")
    try:
        getpassword = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    password = getpassword.content.strip("||").strip()
    try:
        await getpassword.delete()
    except:
        await ctx.channel.send("I don't have the permission to delete messages on this channel.")

    try:
        id = db.addTable(timetable, notificationChannel, password, mention)
    except Exception as e:
        await ctx.channel.send(f"An error has occured. Error: {e}")
        await bot.get_channel(798954817459716106).send(f"An error has occured while creating a timetable: {e}")
        return

    ttTask = asyncio.create_task(runTimetable(id))
    await ctx.channel.send(f"Timetable created with ID {id}.")
    await ttTask


@bot.command()
async def show(ctx, tableid):
    global db
    try:
        tableDf = db.getTable(tableid)
        tableDf.columns = list(map(lambda x: x.strip('t'),tableDf.columns))
        tableDf.index = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        await ctx.channel.send(embed=discord.Embed(title=f"Timetable {tableid}", description=f"```\n{tableDf.replace('nope','')}\n```",color=0xACB6C4))
    except:
        await ctx.channel.send("I can't find a timetable with the given ID.")


@bot.command()
async def help(ctx, helpTopic=""):
    file = open("help.json",'r')
    helpcommands = json.load(file)
    if helpTopic in helpcommands:
        await ctx.channel.send(embed=discord.Embed(title=helpcommands[helpTopic][0],description=helpcommands[helpTopic][1].replace("<prefix>",get_prefix(None,ctx)),colour=0xACB6C4))
    else:
        await ctx.channel.send("There isn't a command with that name.")
    file.close()


@bot.command()
async def delete(ctx, tid):
    global db
    realPassword = db.getTableInfos(tid)["password"]
    await ctx.channel.send("Enter password for this timetable:")
    try:
        getpassword = await bot.wait_for('message', check=lambda m: m.author==ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    password = getpassword.content.strip("||").strip()
    try:
        await getpassword.delete()
    except:
        await ctx.channel.send("I don't have the permission to delete messages on this channel.")
    if password==realPassword:
        db.delTable(tid)
        await ctx.channel.send(f"Timetable with ID {tid} has successfully deleted.")
    else:
        await ctx.channel.send("Wrong password!")


@bot.command()
async def changemention(ctx, tid, *mentions):
    global db
    mention = ' '.join(mentions)
    tableInfos = db.getTableInfos(tid)
    realPassword = tableInfos["password"]
    channelid = tableInfos["channel"]
    await ctx.channel.send("Enter password for this timetable:")
    try:
        getpassword = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    password = getpassword.content.strip("||").strip()
    try:
        await getpassword.delete()
    except:
        await ctx.channel.send("I don't have the permission to delete messages on this channel.")
    if password == realPassword:
        db.changeTableInfo(tid, channelid, realPassword, mention)
        if mention.isspace() or mention == '':
            await ctx.channel.send(f"Mention of the timetable with the {tid} successfully changed to nothing. It will no longer mention people.")
        else:
            await ctx.channel.send(f"Mention of the timetable with ID {tid} successfully changed to {mention}")
    else:
        await ctx.channel.send("Wrong password!")


@bot.command()
async def changechannel(ctx, tid, channel):
    global db
    channelid = int(channel.strip('<').strip('>').strip('#'))
    tableInfos = db.getTableInfos(tid)
    realPassword = tableInfos["password"]
    mention = tableInfos["mention"]
    await ctx.channel.send("Enter password for this timetable:")
    try:
        getpassword = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    password = getpassword.content.strip("||").strip()
    try:
        await getpassword.delete()
    except:
        await ctx.channel.send("I don't have the permission to delete messages on this channel.")
    if password == realPassword:
        db.changeTableInfo(tid, channelid, realPassword, mention)
        await ctx.channel.send(f"Channel of the timetable with ID {tid} successfully changed to <#{channelid}>")
    else:
        await ctx.channel.send("Wrong password!")



@bot.command()
async def changepassword(ctx, tid):
    global db
    tableInfos = db.getTableInfos(tid)
    channelid = tableInfos["channel"]
    realPassword = tableInfos["password"]
    mention = tableInfos["mention"]
    await ctx.channel.send("Enter password for this timetable:")
    try:
        getpassword = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    password = getpassword.content.strip("||").strip()
    try:
        await getpassword.delete()
    except:
        await ctx.channel.send("I don't have the permission to delete messages on this channel.")
    if password == realPassword:
        await ctx.channel.send("PLease enter the new password:")
        try:
            getnewpassword = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
        except asyncio.TimeoutError:
            await ctx.channel.send("Command has canceled due to timeout.")
            return
        newpassword = getnewpassword.content
        await getnewpassword.delete()
        db.changeTableInfo(tid, channelid, newpassword, mention)
        await ctx.channel.send(f"Password of the timetable with ID {tid} successfully changed.")
    else:
        await ctx.channel.send("Wrong password!")



@bot.command()
async def download(ctx, tid):
    global db
    tableDf = db.getTable(tid)
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


async def runcode(ctx, code):
    if int(ctx.author.id) != ownerId:
        return
    else:
        print(code)
        startTime = time.time()
        err = None
        resp = None
        try:
            resp = eval(code)
            err = None
        except Exception as e:
            err = e
        endTime = time.time()
        executionTime = endTime-startTime
        responseEmbed = discord.Embed(title="Eval")
        if err is not None:
            responseEmbed.add_field(name="Error", value=f"```{str(err)}```")
        if resp is not None:
            responseEmbed.add_field(name="Return", value=f"```{str(resp)}```", inline=False)
        responseEmbed.add_field(name="Time", value=f"`{str(executionTime)}` secs",inline=False)
        await ctx.channel.send(embed=responseEmbed)


@bot.command()
async def countdown(ctx, seconds, *name):
    eventname = ' '.join(name)
    await asyncio.sleep(int(seconds))
    await ctx.channel.send(f"Hey <@!{ctx.author.id}> , it's time for {eventname}.")


@bot.command()
async def reminder(ctx, cmd, *args):
    cmand = cmd.lower().strip()
    params = ' '.join(args)
    if cmand == "create" or cmand == "add":
        try:
            channelId = re.search(r'[<][#]([0-9]{18})[>]', params).group().strip('<').strip('>').strip('#')
        except AttributeError:
            await ctx.channel.send(f"Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\nChannel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\nTime should be a valid time in HH:MM format.")
            return
        if "today" in params:
            reminderDate = getDate()
        elif "tomorrow" in params:
            reminderDate = getDate("tomorrow")
        else:
            result = None
            try:
                result = re.search(hugeregex, params).group()
            except AttributeError:
                await ctx.channel.send(f"Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\nChannel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\nTime should be a valid time in HH:MM format.")
                return
            if result != None:
                result = result.replace('/', '-').replace('.', '-').split('-')
                result[0] = result[0].lstrip('0')
                result[1] = result[1].lstrip('0')
                reminderDate = '-'.join(result)
            elif result == None:
                await ctx.channel.send(f"Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\nChannel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\nTime should be a valid time in HH:MM format.")
                return
        searchTime = None
        searchTime = re.search(timeregex, params).group()
        if searchTime == None:
            await ctx.channel.send(f"Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\nChannel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\nTime should be a valid time in HH:MM format.")
            return
        elif searchTime != None:
            reminderTime = searchTime.replace(':', '_').replace('.', '_')
        remId = db.addReminder(reminderDate, reminderTime, channelId, ' '.join(params.split()[3:]))
        await ctx.channel.send(f"Reminder {' '.join(params.split()[3:])} with ID {remId} has successfully set to {reminderDate.replace('-', '/')} {reminderTime.replace('_',':')}.\nIt will be announced at channel <#{channelId}>")

    elif cmand == "delete" or cmand == "remove":
        if len(params.split())==1:
            remId = re.search(r'([1-9])([0-9]{5})')
            db.delReminder(remId)
        else:
            await ctx.channel.send(f'Usage: "{get_prefix(None, ctx)}reminder remove ID" or "{get_prefix(None, ctx)}reminder delete ID"')
    else:
        await ctx.channel.send("There isn't a reminder command like that.")
        return


@bot.command()
async def prefix(ctx, pf=""):
    global db
    if ctx.author.guild_permissions.manage_guild:
        db.changePrefix(ctx.guild.id, pf)
        await ctx.channel.send(f"Prefix for this server is changed to: {pf}")
    else:
        await ctx.channel.send("I think you don't have the permission to do that. Pick that 'Manage Server' permission, then maybe.")

bot.run(TOKEN)
