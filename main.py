# -*- coding: utf-8 -*-

"""
SP radio discord bot
~~~~~~~~~~~~~~~~~~~

An official discord bot that broadcasts Internet radio SP radio

:copyright: (c) 2022 Stepan Khozhempo
:license: MIT

"""

import platform
import os

import nextcord
from nextcord.ext import commands, tasks

import logging
import logger

from db import Database
from sprapi.api import SPRadioApi

import config as cfg

from views.DeleteMessageButton import DeleteMessageButtonView
from views.ReportNewSongAdminButtons import ReportNewSongAdminButtonsView
from views.ReportNewSongWarningButton import ReportNewSongWarningButtonView
from views.UpdateRadioInformationButton import UpdateRadioInformationButtonView

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True

last_song = None

logger.setup()

logging.info('Starting Bot...')
logging.info(f"Python version: {platform.python_version()}")
logging.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")

logging.info('Connecting to database...')
cfg.db = Database(cfg.Database.host, cfg.Database.port, cfg.Database.user, cfg.Database.password, cfg.Database.database)

logging.info('Loading bans to memory')
bans = cfg.db.get_bans()

cfg.Discord.bans = [ban[0] for ban in bans]


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.load_extension('cogs.events')
        self.load_extension('cogs.commands')

    async def on_ready(self):
        logging.info(f"Logged in as {self.user.name}")

        report_channel = self.get_channel(cfg.Discord.reports_new_songs_channel_id)

        self.add_view(DeleteMessageButtonView())
        self.add_view(UpdateRadioInformationButtonView())
        self.add_view(ReportNewSongWarningButtonView(report_channel, self.get_user))
        self.add_view(ReportNewSongAdminButtonsView(self.get_user))

        self.change_activity.start()

    @tasks.loop(seconds=cfg.Discord.radio_request_song_time)
    async def change_activity(self):
        global last_song

        api = SPRadioApi()

        song = await api.get_now_playing()
        song = song.full_title

        if song != last_song:
            logging.debug(f'Activity change from "{last_song}" to "{song}"')
            last_song = song
            await self.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=song))

        elif song is None:
            await self.change_presence(
                activity=nextcord.Activity(type=nextcord.ActivityType.listening, name='СП Радио'))


bot = Bot(intents=intents)
bot.run(cfg.Discord.TOKEN)
