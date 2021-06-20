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
import re, json
from datetime import datetime as dt

hugeregex = r'(((([012]\d)|(\d)|(30))[/.-](([0][469])|([1][1])))|((([012]\d)|(\d)|(3[01]))[/.-](([0][13578])|([1][02])))|((([01]\d)|(\d)|([2][012345678]))[/.-]((02)|(2))))[/.-]((20[2][123456789])|(20[3456789]\d))'
timeregex = r'(([01][0123456789])|(\d)|([2][0123]))[:.]([012345]\d)'

async def reminder(ctx, cmd, args, bot, db, getDate, getDayTime, get_prefix):
    lang = db.getLang(ctx.guild.id)
    f = open("./languages/"+lang+".json", 'r')
    strings = json.load(f)
    f.close()
    strings = strings["reminder"]
    if cmd=='' or cmd == None:
        await ctx.channel.send(embed=discord.Embed(
        description=strings[0].replace("<prefix>", get_prefix(None,ctx)), colour=0xACB6C4))
        return
    if len(args) < 1:
        await ctx.channel.send(embed=discord.Embed(
        description=strings[0].replace("<prefix>", get_prefix(None,ctx)), colour=0xACB6C4))
        return
    cmand = cmd.lower().strip()
    print(args)
    params = ' '.join(args)
    if cmand in strings[5]:
        if len(args) < 4:
            await ctx.channel.send(embed=discord.Embed(
                description=strings[1].replace("<prefix>", get_prefix(None,ctx)),
                colour=0xACB6C4))
            return
        if params.find("@everyone") > -1 or params.find("@here") > -1:
            await ctx.channel.send(strings[4])
            return
        try:
            channelId = re.search(r'(\d){18}', args[2]).group().strip('<').strip('>').strip('#')
            if channelId is None:
                await ctx.channel.send(embed=discord.Embed(
                    description=strings[1].replace("<prefix>", get_prefix(None,ctx)),
                    colour=0xACB6C4))
                return
        except AttributeError:
            await ctx.channel.send(embed=discord.Embed(
            description=strings[1].replace("<prefix>", get_prefix(None,ctx)), colour=0xACB6C4))
            return
        if strings[2] in params:
            reminderDate = getDate()
        elif strings[3] in params:
            reminderDate = getDate("tomorrow")
        else:
            result = None
            try:
                result = re.search(hugeregex, params)
                dateindex = result.start()
                result = result.group()
                params = params[:dateindex]+params[dateindex+len(result):]
            except AttributeError:
                await ctx.channel.send(embed=discord.Embed(
                description=strings[1].replace("<prefix>", get_prefix(None,ctx)), colour=0xACB6C4))
                return
            if result is not None:
                result = result.replace('/', '-').replace('.', '-').split('-')
                result[0] = result[0].lstrip('0')
                result[1] = result[1].lstrip('0')
                reminderDate = '-'.join(result)
            else:
                await ctx.channel.send(embed=discord.Embed(
                description=strings[1].replace("<prefix>", get_prefix(None,ctx)), colour=0xACB6C4))
                return
        searchTime = None
        searchTime = re.search(timeregex, params).group()
        if searchTime is None:
            await ctx.channel.send(embed=discord.Embed(
            description=strings[1].replace("<prefix>", get_prefix(None,ctx)), colour=0xACB6C4))
            return
        else:
            reminderTime = searchTime.replace(':', '_').replace('.', '_')
        if dt.strptime(f"{reminderDate} {reminderTime}", "%d-%m-%Y %H_%M").timestamp() < dt.utcnow().timestamp():
            await ctx.channel.send(strings[4])
            return
        remId = db.addReminder(reminderDate, reminderTime, channelId, ' '.join(params.split()[3:]))
        await ctx.channel.send(strings[6]
                                .replace("{event}",' '.join(params.split()[3:]))
                                .replace("{remId}",str(remId))
                                .replace("{date}",reminderDate.replace('-', '/'))
                                .replace("{time}",reminderTime.replace('_',':'))
                                .replace("{channel}",f"<#{channelId}>"))

    elif cmand in strings[7]:
        if len(args)>=1:
            remId = re.search(r'([1-9])([0-9]{5})', args[0])
            if remId is None:
                await ctx.channel.send(embed=discord.Embed(
                description=strings[7].replace("<prefix>", get_prefix(None,ctx)),
                colour=0xACB6C4))
                return
            remId = remId.group()
            if(len(remId) != 6):
                await ctx.channel.send(embed=discord.Embed(
                description=strings[7].replace("<prefix>", get_prefix(None,ctx)),
                colour=0xACB6C4))
                return
            try:
                remId = int(remId)
            except:
                await ctx.channel.send(embed=discord.Embed(
                description=strings[7].replace("<prefix>", get_prefix(None,ctx)),
                colour=0xACB6C4))
                return
            rids = db.run("SELECT rid FROM reminders")
            if (remId,) in rids:
                db.delReminder(remId)
                await ctx.channel.send(strings[9].replace("{remId}", str(remId)))
            else:
                await ctx.channel.send(strings[10])
        else:
            await ctx.channel.send(embed=discord.Embed(
            description=strings[7].replace("<prefix>", get_prefix(None,ctx)),
            colour=0xACB6C4))
    else:
        await ctx.channel.send(strings[10])
        return
