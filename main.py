# -*- coding: utf-8 -*-

"""
SP radio discord bot
~~~~~~~~~~~~~~~~~~~

A discord bot that broadcasts Internet radio SP radio

:copyright: (c) 2022 Stepan Khozhempo
:license: MIT

"""

import discord
from discord.ext import commands
import asyncio

import TOKEN
import config as cfg

client = commands.Bot(command_prefix=cfg.command_prefix)


@client.event
async def on_ready():
    print('Bot started')


@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is not None and after.channel is None:
        if before.channel.guild.voice_client and len(before.channel.members) == 1:
            before.channel.guild.voice_client.stop()
            await before.channel.guild.voice_client.disconnect()


@client.command(pass_context=True)
async def play(ctx):
    await ctx.message.delete()

    try:
        channel = client.get_channel(ctx.message.author.voice.channel.id)
        channel = await channel.connect()

    except AttributeError:
        pass

    except discord.errors.ClientException:
        notify = await ctx.send('Бот уже находится в канале')
        await asyncio.sleep(cfg.notify_time_auto_delete)
        await notify.delete()
        return

    if ctx.voice_client:
        source = discord.FFmpegPCMAudio(cfg.radio_url)
        channel.play(source)

    else:
        notify = await ctx.send('Вы не находитесь в каком либо канале')
        await asyncio.sleep(cfg.notify_time_auto_delete)
        await notify.delete()


@client.command(pass_context=True)
async def leave(ctx):
    await ctx.message.delete()

    if ctx.voice_client is None:
        notify = await ctx.send('Бот ни находится в каком либо канале')
        await asyncio.sleep(cfg.notify_time_auto_delete)
        await notify.delete()

    elif ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
        await ctx.guild.voice_client.disconnect()

    elif ctx.author.voice.channel != ctx.voice_client.channel:
        notify = await ctx.send('Вы не находитесь в канале в котором играет бот')
        await asyncio.sleep(cfg.notify_time_auto_delete)
        await notify.delete()


client.run(TOKEN.TOKEN)
