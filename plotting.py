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

from matplotlib import pyplot as plt
import discord
import os, re
from PIL import Image

async def plottable(ctx, db, tableid, get_prefix, botlistsmanager):
    if not await botlistsmanager.isVoted(ctx.author.id):
        await ctx.channel.send(embed=discord.Embed(title="Vote to use this command!", description="[Click Here to Vote](https://top.gg/bot/789202881336311849/vote)", colour=0xACB6C4))
        return
    if tableid == None or tableid == '':
        await ctx.channel.send(f"Usage: {get_prefix(None,ctx)}show table_id")
        return
    elif re.match(r'[123456789](\d){5}', tableid) == None:
        await ctx.channel.send(f"Usage: {get_prefix(None,ctx)}show table_id")
        return
    try:
        tabledf = db.getTable(tableid)
    except:
        await ctx.channel.send("I can't see a timetable with that ID.")
        return
    fig, ax = plt.subplots()
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_axis_off()
    ax.table(tabledf.replace('nope', ' ').values,
        colLabels=list(map(lambda x: x.lstrip('t').replace('_',':'),tabledf.columns)),
        rowLabels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        cellLoc="center")
    plt.savefig(f"table-{tableid}-uncropped.png", bbox_inches="tight", dpi=150, pad_inches=0.2)
    fig.clf()
    img = Image.open(f"table-{tableid}-uncropped.png")
    width, height = img.size
    img_cropped = img.crop((0, height/3*2, width, height))
    img_cropped.save(f"table-{tableid}.png")
    await ctx.channel.send("Timetable "+tableid+':', file=discord.File(f"table-{tableid}.png"))
    os.remove(f"table-{tableid}.png")
    os.remove(f"table-{tableid}-uncropped.png")
