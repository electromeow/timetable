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


async def vote(ctx):
    await ctx.channel.send(
    embed=discord.Embed(title="Loved Timetable? Then vote it to support!",
    description="Our heart would wish that you voted in both bot lists,\n\
    but your vote on top.gg would be enough.\n\
<:topgg:834421312994279535>  [top.gg](https://top.gg/bot/789202881336311849/vote) (waiting to be verified)\n\
<:discordbotlist:834424137224814642>  [DiscordBotList](https://discordbotlist.com/bots/timetable/upvote)\n\
<:discordboats:834424137174614086>  [Discord Boats](https://discord.boats/bot/789202881336311849/vote)\n\
**We don't earn money from your votes!**",
    colour=0xACB6C4))


async def invite(ctx):
    await ctx.channel.send(
    embed=discord.Embed(title="Loved Timetable? Then invite it to other servers!",
    description="Invite link can be found at:\n\
<:topgg:834421312994279535>  [top.gg](https://top.gg/bot/789202881336311849) (waiting to be verified)\n\
<:botsgg:834424137631006720>  [bots.gg](https://discord.bots.gg/bots/789202881336311849) (waiting to be verified)\n\
<:discordbotlist:834424137224814642>  [DiscordBotList](https://discordbotlist.com/bots/timetable)\n\
<:discordboats:834424137174614086>  [Discord Boats](https://discord.boats/bot/789202881336311849)",
    colour=0xACB6C4))


async def contribute(ctx):
    await ctx.channel.send(
    embed=discord.Embed(
    title="Contribute",
    description="I heard that you have enough Python knowledge to improve this bot.\n\
If I didn't hear wrong, then go to [my GitHub Repository](https://github.com/electromeow/timetable).\
Fork, improve and submit a pull request.\nActually bot isn't deployed by that repository.\n\
But I sync them with the original private deployment repository including secret information like token.\n\
So you can make sure that your improvements will be applied to actual bot.\n\
If you are a person don't know enough Python and if you're a free rider, please don't copy-paste & host \
it. Because that's not easy to develop that huge code and hosting is a big problem even if you developed that.\n\
Moreover, legally you aren't permitted to copy-paste and host it without \
making your project open source due to [GPLv3 License](https://www.gnu.org/licenses/gpl-3.0.en.html).",
    colour=0xACB6C4))
