import nextcord
import asyncio

from nextcord import Interaction

import config as cfg
from sprapi.api import SPRadioApi


async def play_song(inter: Interaction, stream_path: str = cfg.Radio.spradio_stream_url):
    try:
        channel = inter.user.voice.channel
        voice_client: nextcord.VoiceClient = await channel.connect()

    except AttributeError:
        pass

    except asyncio.exceptions.TimeoutError:
        pass

    except nextcord.errors.ClientException:
        if inter.user.id in cfg.Discord.admin_ids:
            inter.guild.voice_client.stop()
            await inter.guild.voice_client.disconnect(force=False)

            api = SPRadioApi()
            song = await api.get_now_playing()

            if stream_path == cfg.Radio.bear_theme_stream_url:
                await inter.send('Босс, переподключаемся к вам с песней `Тема Медведя` *Вам тю пиливудупай*',
                                 ephemeral=True)

            elif stream_path == cfg.Radio.eldaradio_stream_url:
                await inter.send('Босс, переподключаемся к вам c **ЭльдаРадио**', ephemeral=True)

            else:
                await inter.send(f'Босс, переподключаемся к вам с песней `{song.full_title}`', ephemeral=True)

            try:
                channel = inter.user.voice.channel
                voice_client: nextcord.VoiceClient = await channel.connect()

            except AttributeError:
                await inter.send(
                    'Босс, вы не находитесь в каком либо канале' if inter.user.id in cfg.Discord.admin_ids else
                    'Вы не находитесь в каком либо канале', ephemeral=True)
                return

            except asyncio.exceptions.TimeoutError:
                pass

            if inter.guild.voice_client:
                source = nextcord.FFmpegPCMAudio(stream_path)
                voice_client.play(source)

            else:
                await inter.edit('Бот не находится в канале', ephemeral=True)

        else:
            await inter.send('Бот уже находится в каком-то канале', ephemeral=True)

        return

    if inter.guild.voice_client:
        source = nextcord.FFmpegPCMAudio(stream_path)
        voice_client.play(source)

        if stream_path == cfg.Radio.bear_theme_stream_url:
            await inter.send(
                'Босс, включаемся с песней `Тема Медведя` *Вам тю пиливудупай*' if inter.user.id in cfg.Discord.admin_ids
                else 'Включаемся с песней `Тема Медведя` *Вам тю пиливудупай*', ephemeral=True)

        elif stream_path == cfg.Radio.eldaradio_stream_url:
            await inter.send(
                'Босс, включаем **ЭльдаРадио**' if inter.user.id in cfg.Discord.admin_ids
                else 'Включаем **ЭльдаРадио**', ephemeral=True)

        else:
            api = SPRadioApi()
            song = await api.get_now_playing()
            song = song.full_title

            if song is None:
                await inter.send(
                    'Оу черт, с СП радио что-то не так. Вероятнее всего упал сервер транслирующий радио. '
                    'Попробуйте насладится песнями позже. А пока можете послушать **ЭльдаРадио**')

                await voice_client.disconnect()
                return

            await inter.send(
                f'Босс, включаемся с песней `{song}`' if inter.user.id in cfg.Discord.admin_ids
                else f'Включаемся с песней `{song}`', ephemeral=True)

        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()

    else:
        await inter.send('Босс, вы не находитесь в каком либо канале' if inter.user.id in cfg.Discord.admin_ids else
                         'Вы не находитесь в каком либо канале', ephemeral=True)


async def stop_song(inter: Interaction):
    try:
        if inter.guild.voice_client is None:
            await inter.send('Босс, бот ни находится в каком либо канале' if inter.user.id in cfg.Discord.admin_ids
                             else 'Бот ни находится в каком либо канале', ephemeral=True)
            return

        elif inter.user.id in cfg.Discord.admin_ids or inter.user.voice.channel == inter.guild.voice_client.channel:
            inter.guild.voice_client.stop()
            await inter.guild.voice_client.disconnect(force=False)
            await inter.send('Отключаемся...', ephemeral=True)

        elif inter.user.voice.channel != inter.guild.voice_client.channel:
            await inter.send('Вы не находитесь в канале в котором играет бот', ephemeral=True)

    except AttributeError:
        await inter.send('Вы не находитесь в канале в котором играет бот', ephemeral=True)
