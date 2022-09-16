import nextcord


class DeleteMessageButton(nextcord.ui.Button):
    def __init__(self):
        super().__init__(
            label='Удалить',
            style=nextcord.ButtonStyle.red,
            custom_id='spradioDeleteMessageButton'
        )

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.message.delete()


class DeleteMessageButtonView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(DeleteMessageButton())
