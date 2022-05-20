# -*- coding: utf-8 -*-

"""
SP radio stats discord bot
~~~~~~~~~~~~~~~~~~~

Statistics for SP radio discord bot

:copyright: (c) 2022 Stepan Khozhempo
:license: MIT

"""

from discord.ext import commands
import time

import TOKEN
import config as cfg

client = commands.Bot(command_prefix=cfg.command_prefix)


def guilds(guilds_attr: list) -> str:
    guilds_return = []
    for guild in guilds_attr:
        guilds_return.append(guild.name)
    return str(guilds_return)


def total_users(guilds_attr: list) -> str:
    total = 0
    for guild in guilds_attr:
        total += guild.member_count
    return str(total)


@client.event
async def on_ready():
    print('guilds: ' + guilds(client.guilds))
    print('guild count: ' + str(len(client.guilds)))
    print('total number of users ' + total_users(client.guilds))
    time.sleep(10)
    exit(0)


client.run(TOKEN.TOKEN)
