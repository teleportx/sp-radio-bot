import nextcord
from nextcord.types.channel import Channel

from views.ReportNewSongModal import ReportNewSongModal


class ReportNewSongWarningButton(nextcord.ui.Button):
    def __init__(self, report_channel: Channel, get_user_function:callable):
        self.report_channel = report_channel
        self.get_user_function = get_user_function

        super().__init__(
            label='Я понимаю',
            style=nextcord.ButtonStyle.green,
            custom_id='spradioReportNewSongWarningButton'
        )

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(ReportNewSongModal(self.report_channel, self.get_user_function))


class ReportNewSongWarningButtonView(nextcord.ui.View):
    def __init__(self, report_channel: Channel, get_user_function: callable):
        super().__init__(timeout=None)
        self.add_item(ReportNewSongWarningButton(report_channel, get_user_function))
