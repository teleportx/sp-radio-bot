import nextcord
from nextcord import User, Message
from nextcord.types.channel import Channel

from views.DeleteMessageButton import DeleteMessageButtonView
import config as cfg


class ReportNewSongAdminAcceptButton(nextcord.ui.Button):
    def __init__(self, get_user_function: callable):
        self.get_user_function = get_user_function

        super().__init__(
            label='Принять',
            style=nextcord.ButtonStyle.green,
            custom_id='spradioReportNewSongAdminAcceptButton'
        )

    async def callback(self, interaction: nextcord.Interaction):
        await self.send_user_notify(interaction.message)

        await interaction.message.edit(content='Вы приняли заявку на добавление песни!', view=DeleteMessageButtonView())

    async def send_user_notify(self, message: Message):
        reported_user: User = self.get_user_function(int(message.content))

        fields = message.embeds[0].fields

        song_title = fields[1].value
        song_author = fields[0].value

        try:
            await reported_user.send(f'Ваша заявка на добавлении песни *{song_title}* от {song_author} была принята! '
                                     f'Данную песню вы вскоре сможете услышать на SP Radio')

        except:
            pass


class ReportNewSongAdminDenyButton(nextcord.ui.Button):
    def __init__(self, get_user_function: callable):
        self.get_user_function = get_user_function

        super().__init__(
            label='Отклонить',
            style=nextcord.ButtonStyle.gray,
            custom_id='spradioReportNewSongAdminDenyButton'
        )

    async def callback(self, interaction: nextcord.Interaction):
        await self.send_user_notify(interaction.message)

        await interaction.message.edit(content='Заявка была отклонена.', view=None, embed=None)

        await interaction.message.delete(delay=5)

    async def send_user_notify(self, message: Message):
        reported_user: User = self.get_user_function(int(message.content))

        fields = message.embeds[0].fields

        song_title = fields[1].value
        song_author = fields[0].value

        try:
            await reported_user.send(f'Ваша заявка на добавлении песни *{song_title}* от {song_author} была отклонена. '
                                     f'Не расстраивайтесь, вероятно пенся не подошла под требования добавления на SP Radio')

        except:
            pass


class ReportNewSongAdminBanButton(nextcord.ui.Button):
    def __init__(self, get_user_function: callable):
        self.get_user_function = get_user_function

        super().__init__(
            label='Алава Кедавра',
            style=nextcord.ButtonStyle.red,
            custom_id='spradioRepDenyortNewSongAdminBanButton'
        )

    async def callback(self, interaction: nextcord.Interaction):
        reason = 'злоупотребление функцией "Заявка на добавление песни"'
        cfg.db.insert_ban(interaction.message.content, reason)

        await self.send_user_notify(interaction.message, reason)

        await interaction.message.edit(content='Челик аннигилировался', view=None, embed=None)
        await interaction.message.delete(delay=10)

    async def send_user_notify(self, message: Message, reason: str):
        reported_user: User = self.get_user_function(int(message.content))

        try:
            await reported_user.send(f'Вы были забанины в дискорд боте SP Radio по причине `{reason}`')

        except:
            pass


class ReportNewSongAdminButtonsView(nextcord.ui.View):
    def __init__(self, get_user_function: callable):
        super().__init__(timeout=None)

        self.add_item(ReportNewSongAdminAcceptButton(get_user_function))
        self.add_item(ReportNewSongAdminDenyButton(get_user_function))
        self.add_item(ReportNewSongAdminBanButton(get_user_function))
