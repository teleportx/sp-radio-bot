import datetime

import psycopg2
from nextcord import Interaction, slash_command, SlashOption, Embed, message_command
from nextcord.ext.commands import Bot, Cog
import nextcord

import config as cfg
from functions.create_paste import create_paste
from sprapi.api import SPRadioApi

from functions.playback_control import play_song, stop_song
from functions import declination
from functions.get_radio_information import get_radio_information
from functions.interaction_ban import interaction_ban, check_ban

from views.DeleteMessageButton import DeleteMessageButtonView
from views.ReportNewSongWarningButton import ReportNewSongWarningButtonView
from views.UpdateRadioInformationButton import UpdateRadioInformationButtonView


class Commands(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @message_command
    async def eldaradio(self, inter: Interaction, message: nextcord.Message):
        if await check_ban(inter.user.id):
            await inter.send(cfg.Radio.ban_video_url, ephemeral=True)
            return
        await play_song(inter, cfg.Radio.eldaradio_stream_url)

    @message_command
    async def uuuuunoradio(self, inter: Interaction, message: nextcord.Message):
        if await check_ban(inter.user.id):
            await inter.send(cfg.Radio.ban_video_url, ephemeral=True)
            return
        await play_song(inter, cfg.Radio.uuuuunoradio_stream_url)

    @slash_command(description='SP radio')
    async def spradio(self):
        pass

    @spradio.subcommand(description="Запустить воспроизведение")
    @interaction_ban
    async def play(self, inter: Interaction):
        await play_song(inter)

    @spradio.subcommand(description="Остановить воспроизведение")
    @interaction_ban
    async def stop(self, inter: Interaction):
        await stop_song(inter)

    @spradio.subcommand(description="Вам тю пиливудупай")
    @interaction_ban
    async def bear_theme(self, inter: Interaction):
        await play_song(inter, cfg.Radio.bear_theme_stream_url)

    @spradio.subcommand(description='Если у вас есть крутая песня как-либо связанная с сп, то пропишите эту команду!')
    @interaction_ban
    async def report_new_song(self, inter: Interaction):
        report_channel = self.bot.get_channel(cfg.Discord.reports_new_songs_channel_id)

        await inter.send('Вы подаете заявку на добавление песни на СПРадио. '
                         'Эта песня должна хоть как-то связанна с СП, иначе ваша заявка может быть отклонена. '
                         'Если вы будите спамить заявками или указывать заведомо ложную информацию вы можете '
                         'быть забанены как для подачи заявок, так и для пользования СПРадио',
                         view=ReportNewSongWarningButtonView(report_channel, self.bot.get_user),
                         ephemeral=True)

    @spradio.subcommand(description="Получить информацию о текущей песне")
    @interaction_ban
    async def now(self, inter: Interaction):
        api = SPRadioApi()
        song = await api.get_now_playing()

        lyrics = song.lyrics
        if lyrics == '':
            lyrics = 'Лириксы для этой песни не найдены'

        now_track_end = datetime.datetime.now() - song.played_at
        now_track_end_secs = song.duration - now_track_end.seconds
        seconds_text = declination.seconds(now_track_end_secs)

        duration_text = declination.seconds(song.duration)

        if now_track_end_secs <= 0:
            now_track_end_secs = 'now'
            seconds_text = ''

        embed = Embed(title=song.title, description=lyrics, timestamp=song.played_at)

        embed.set_author(name=song.author)
        embed.set_thumbnail(song.art)

        embed.add_field(name='Информация', value=f'Песня начала играть в **{song.played_at.time()}**\n'
                                                 f'Продолжительность песни **{song.duration}** {duration_text}\n'
                                                 f'Закончит играть через **{now_track_end_secs}** {seconds_text}')

        await inter.send(embed=embed, view=DeleteMessageButtonView())

    @spradio.subcommand(description="Получить информацию о радио или боте")
    async def info(self, inter: Interaction,
                   choise: int = SlashOption(
                       name="about",
                       choices={"radio": 0, "bot": 1},
                   )):
        if await check_ban(inter.user.id):
            await inter.send(cfg.Radio.ban_video_url, ephemeral=True)
            return

        if choise == 0:
            embed = await get_radio_information()

            if embed is None:
                await inter.send('Не получается получить инорфмацию 😠', ephemeral=True)
                return

            await inter.send(embed=embed, view=UpdateRadioInformationButtonView(), ephemeral=True)

        elif choise == 1:
            if inter.user.id not in cfg.Discord.admin_ids:
                await inter.send('У вас нет прав для выполнения этого действия', ephemeral=True)
                return

            mutual_guilds = inter.user.mutual_guilds

            guilds = [guild.name for guild in self.bot.guilds]
            guilds_text = '\n'.join(guilds)

            total_users = 0
            for guild in self.bot.guilds:
                total_users += guild.member_count
            total_users = total_users

            total_listeners = 0

            for voice_client in self.bot.voice_clients:
                total_listeners += len(voice_client.channel.members) - 1

            mutual_guilds_text = [guild.name for guild in mutual_guilds]

            guilds_url = create_paste(guilds_text)

            embed = Embed(title='Информация о SPradio бот')

            embed.set_thumbnail('https://radio.uuuuuno.net/static/uploads/browser_icon/192.1653387216.png')

            embed.add_field(name='Общее количество пользователей', value=total_users)
            embed.add_field(name='Общее количество серверов', value=len(self.bot.guilds))
            embed.add_field(name='Текущее количество каналов слушателей бота', value=len(self.bot.voice_clients))
            embed.add_field(name='Текущее количество слушателей бота', value=total_listeners)
            embed.add_field(name='Общие сервера', value=' ,'.join(mutual_guilds_text), inline=False)
            embed.add_field(name='Все сервера бота', value=f'||{guilds_url}||')

            await inter.send(
                '**Настоятельная просьба не распростронять информацию представленную ниже не доверенным лицам**',
                embed=embed,
                ephemeral=True)


    @spradio.subcommand()
    async def admin(self):
        pass

    @admin.subcommand(description='Ban user in bot SP radio')
    async def ban(self, inter: Interaction,
                  user_id: str = SlashOption(required=True),
                  reason: str = SlashOption(required=False)):
        if await check_ban(inter.user.id):
            await inter.send(cfg.Radio.ban_video_url, ephemeral=True)
            return

        elif inter.user.id not in cfg.Discord.admin_ids:
            await inter.send('У вас нет прав для выполнения этого действия', ephemeral=True)
            return

        try:
            cfg.db.insert_ban(user_id, reason)
            await inter.send('Забанен.', ephemeral=True)

            try:
                await self.bot.get_user(int(user_id))\
                    .send(f'Вы были забанины в дискорд боте SP Radio по причине `{reason}`\n'
                          f'{cfg.Radio.ban_video_url}')

            except:
                pass

        except psycopg2.errors.UniqueViolation:
            await inter.send('Он уже забанен', ephemeral=True)

    @admin.subcommand(description='Unban user in bot SP radio')
    async def unban(self, inter: Interaction,
                    user_id: str = SlashOption(required=True)):
        if await check_ban(inter.user.id):
            await inter.send(cfg.Radio.ban_video_url, ephemeral=True)
            return

        elif inter.user.id not in cfg.Discord.admin_ids:
            await inter.send('У вас нет прав для выполнения этого действия', ephemeral=True)
            return

        cfg.db.delete_ban(user_id)
        await inter.send('Пользователь разбанен!', ephemeral=True)

        try:
            await self.bot.get_user(int(user_id)) \
                .send(f'Наши поздравления! Вы были разабанины в дискорд боте SP Radio! '
                      f'Постарайтесь больше не нарушать правила')

        except:
            pass


def setup(bot: Bot):
    bot.add_cog(Commands(bot))
