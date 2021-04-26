import asyncio
import pandas as pd
import discord


botUserId = "789202881336311849"
ownerId = 754327007331876945

async def timetable(ctx,bot,db,runTimetable):
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

    await ctx.channel.send("Mention the people or roles to inform, they will be mentioned when an event has started\n\
You can also make mentioning people off by sending a \"nope\":")
    try:
        getmention = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel,timeout=120)
    except asyncio.TimeoutError:
        await ctx.channel.send("Command has canceled due to timeout.")
        return
    if getmention.content.lower() == "nope":
        mention=''
    else:
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
