import datetime
from typing import Optional
from nextcord import Embed

from functions import declination
from sprapi.api import SPRadioApi
import config as cfg


async def get_radio_information() -> Optional[Embed]:
    api = SPRadioApi()
    info = await api.get_information()

    if info is None:
        return None

    now_track_end = datetime.datetime.now() - info.now_playing.played_at
    now_track_end_secs = info.now_playing.duration - now_track_end.seconds
    seconds_text = declination.seconds(now_track_end_secs)
    description = f'*{info.playing_next.title}* начнет играть в **{info.playing_next.played_at.time()}**\n' \
                  f'*{info.now_playing.title}* закончится через **{now_track_end_secs}** {seconds_text}'

    embed = Embed(title='Информация о SPradio',
                  description=description,
                  timestamp=datetime.datetime.now()
                  )

    embed.set_thumbnail(cfg.Radio.spradio_icon_url)

    embed.add_field(name='Предыдущая песня', value=info.previous_playing.full_title, inline=False)
    embed.add_field(name='Текущая песня', value=info.now_playing.full_title, inline=False)
    embed.add_field(name='Следущая песня', value=info.playing_next.full_title, inline=False)
    embed.add_field(name='Слушателей', value=info.listeners, inline=False)

    return embed
