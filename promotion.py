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
import json

async def vote(ctx, db):
    strings = json.load(open(f"./languages/{db.getLang(ctx.guild.id)}.json", 'r'))["vote"]
    await ctx.channel.send(
    embed=discord.Embed(title=strings[0],
    description=strings[1],
    colour=0xACB6C4))


async def invite(ctx, db):
    strings = json.load(open(f"./languages/{db.getLang(ctx.guild.id)}.json", 'r'))["invite"]
    await ctx.channel.send(
    embed=discord.Embed(title=strings[0],
    description=strings[1],
    colour=0xACB6C4))


async def contribute(ctx, db):
    strings = json.load(open(f"./languages/{db.getLang(ctx.guild.id)}.json", 'r'))["contribute"]
    await ctx.channel.send(
    embed=discord.Embed(
    title=strings[0],
    description=strings[1],
    colour=0xACB6C4))
