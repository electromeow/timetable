import asyncio
import discord
import re


botUserId = "789202881336311849"
ownerId = 754327007331876945
hugeregex = r'(((([012]\d)|(\d)|(30))[/.-](([0][469])|([1][1])))|((([012]\d)|(\d)|(3[01]))[/.-](([0][13578])|([1][02])))|((([01]\d)|(\d)|([2][012345678]))[/.-]((02)|(2))))[/.-]((20[2][123456789])|(20[3456789]\d))'
timeregex = r'(([01][0123456789])|(\d)|([2][0123]))[:.]([012345]\d)'

async def reminder(ctx, cmd, args, bot, db, getDate, getDayTime, get_prefix):
    cmand = cmd.lower().strip()
    params = ' '.join(args)
    if cmand == "create" or cmand == "add":
        try:
            channelId = re.search(r'[<][#]([0-9]{18})[>]', params).group().strip('<').strip('>').strip('#')
        except AttributeError:
            await ctx.channel.send(embed=discord.Embed(
            description=f"Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\n\
Channel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\n\
Time should be a valid time in HH:MM format and in UTC/GMT timezone.\n\
Don't know your timezone by UTC? [Click here](https://www.timeanddate.com/time/map) to learn."))
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
                await ctx.channel.send(embed=discord.Embed(
                description=f"Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\n\
Channel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\n\
Time should be a valid time in HH:MM format and in UTC/GMT timezone.\n\
Don't know your timezone by UTC? [Click here](https://www.timeanddate.com/time/map) to learn."))
                return
            if result != None:
                result = result.replace('/', '-').replace('.', '-').split('-')
                result[0] = result[0].lstrip('0')
                result[1] = result[1].lstrip('0')
                reminderDate = '-'.join(result)
            elif result == None:
                await ctx.channel.send(embed=discord.Embed(
                description=f"Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\n\
Channel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\n\
Time should be a valid time in HH:MM format and in UTC/GMT timezone.\n\
Don't know your timezone by UTC? [Click here](https://www.timeanddate.com/time/map) to learn."))
                return
        searchTime = None
        searchTime = re.search(timeregex, params).group()
        if searchTime == None:
            await ctx.channel.send(embed=discord.Embed(
            description=f"Usage: {get_prefix(None,ctx)}reminder add/create time date channel name\n\
Channel should be a channel's mention.\nDate should be a valid date in DD/MM/YYYY format or 'today' or 'tomorrow'.\n\
Time should be a valid time in HH:MM format and in UTC/GMT timezone.\n\
Don't know your timezone by UTC? [Click here](https://www.timeanddate.com/time/map) to learn."))
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
