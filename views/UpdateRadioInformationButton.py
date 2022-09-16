import nextcord

from functions.get_radio_information import get_radio_information


class UpdateRadioInformationButton(nextcord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Обновить',
            style=nextcord.ButtonStyle.green,
            custom_id='spradioUpdateRadioInfomationButton'
        )

    async def callback(self, interaction: nextcord.Interaction):
        embed = await get_radio_information()

        if embed is None:
            await interaction.edit(content='Не получается получить инорфмацию 😠')
            return

        await interaction.edit(embed=embed)


class UpdateRadioInformationButtonView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(UpdateRadioInformationButton())
