from nextcord import Interaction

import config as cfg


async def check_ban(user_id: int):
    if user_id in cfg.Discord.admin_ids:
        return False

    else:
        return str(user_id) in cfg.Discord.bans


def interaction_ban(function: callable):
    async def decorator(self, interaction: Interaction):
        banned = await check_ban(interaction.user.id)

        if banned:
            await interaction.send(cfg.Radio.ban_video_url, ephemeral=True)

        else:
            await function(self, interaction)

    decorator.__name__ = function.__name__

    return decorator
