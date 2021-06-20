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

import asyncio
import pandas as pd
import discord
import re
import json

botUserId = "789202881336311849"
ownerId = 754327007331876945
timeregex = r'(([01]\d)|(\d)|(2[0123]))[:.]([012345]\d)'

async def timetable(ctx,bot,db,runTimetable):
    lang = db.getLang(ctx.guild.id)
    f = open("./languages/"+lang+".json", 'r')
    strings = json.load(f)
    f.close()
    strings = strings["timetable"]
    ttembed=discord.Embed(title=strings[0], description=strings[1], colour=0xACB6C4)
    ttembed.set_image(url="https://i.ibb.co/pRBftnx/unknown.png")
    await ctx.channel.send(embed=ttembed)
    try:
        ttLessontimes = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings[2])
        return
    if ttLessontimes.content.lower() in strings[3]:
        await ctx.channel.send(strings[4])
        return
    checkLessonTimes = list(map(
        lambda x: re.search(timeregex, x.strip()),
        ttLessontimes.content.lower().split(',')
    ))
    if None in checkLessonTimes:
        await ctx.channel.send(strings[5])
        return
    ttLessontimes = ttLessontimes.content.replace(':', '_').replace('.', '_').split(",")
    ttLessontimes = list(map(lambda x: x.strip(), ttLessontimes))

    await ctx.channel.send(strings[6])
    try:
        monday = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings[2])
        return
    if monday.content.lower() in strings[3]:
        await ctx.channel.send(strings[4])
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

    await ctx.channel.send(strings[7])
    try:
        tuesday = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings[2])
        return
    if tuesday.content.lower() in strings[3]:
        await ctx.channel.send(strings[4])
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

    await ctx.channel.send(strings[8])
    try:
        wednesday = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings[2])
        return
    if wednesday.content.lower() in strings[3]:
        await ctx.channel.send(strings[4])
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

    await ctx.channel.send(strings[9])
    try:
        thursday = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings[2])
        return
    if thursday.content.lower() in strings[3]:
        await ctx.channel.send(strings[4])
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

    await ctx.channel.send(strings[10])
    try:
        friday = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings[2])
        return
    if friday.content.lower() in strings[3]:
        await ctx.channel.send(strings[4])
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

    await ctx.channel.send(strings[11])
    try:
        saturday = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings[2])
        return
    if saturday.content.lower() in strings[3]:
        await ctx.channel.send(strings[4])
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

    await ctx.channel.send(strings[12])
    try:
        sunday = await bot.wait_for('message', check = lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings[2])
        return
    if sunday.content.lower() in strings[3]:
        await ctx.channel.send(strings[4])
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

    await ctx.channel.send(strings[13])
    while True:
        try:
            notificationChannel = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
        except asyncio.TimeoutError:
            await ctx.channel.send(strings[2])
            return
        if notificationChannel.content.lower() in strings[3]:
            await ctx.channel.send(strings[4])
            return
        notificationChannel = ' '.join(map(lambda x: x.strip('<').strip('>').strip('#'), notificationChannel.content.split()))
        notificationChannel = re.search(r'(\d){18}', notificationChannel)
        if notificationChannel == None:
            await ctx.channel.send(strings[14])
            continue
        else:
            notificationChannel = notificationChannel.group()
        try:
            testChannel = await bot.fetch_channel(notificationChannel)
            testMsg = await testChannel.send("Test")
            try:
                await testMsg.delete()
            except:
                pass
            break
        except discord.Forbidden:
            await ctx.channel.send(strings[15])

    await ctx.channel.send(strings[16])
    try:
        getmention = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings[2])
        return
    if getmention.content.lower() in strings[3]:
        await ctx.channel.send(strings[4])
        return
    if getmention.content.lower() == "nope":
        mention=''
    else:
        mention = getmention.content
        if mention.find("@everyone") > -1 or mention.find("@here") > -1:
            await ctx.channel.send(strings[17])
            return
    await ctx.channel.send(strings[18])
    try:
        getpassword = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send(strings[2])
        return
    password = getpassword.content.strip("||").strip()
    try:
        await getpassword.delete()
    except:
        await ctx.channel.send(strings[19])

    try:
        tableID = db.addTable(timetable, notificationChannel, password, mention)
    except Exception as e:
        await ctx.channel.send(strings[20].replace("{e}", str(e)))
        await bot.get_channel(798954817459716106).send(f"An error has occured while creating a timetable: {e}")
        return
    ttTask = asyncio.create_task(runTimetable(tableID))
    if ctx.author.dm_channel == None:
        await ctx.author.create_dm()
    await ctx.author.dm_channel.send(strings[21].replace("{tableID}", str(tableID)).replace("{password}",password))
    await ttTask
