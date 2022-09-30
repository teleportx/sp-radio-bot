from nextcord import User
from nextcord.ext import commands
import asyncio

import config as cfg


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.delete()
            notify = await ctx.send('Стандартные команды больше не поддерживаются, используйте слэш-команды')

            await asyncio.sleep(cfg.Discord.notify_time_auto_delete)
            await notify.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel and self.bot.user in before.channel.members:
            if before.channel.guild.voice_client and len(before.channel.members) == 1:
                before.channel.guild.voice_client.stop()
                await before.channel.guild.voice_client.disconnect()

            members_bots = []
            for user in before.channel.members:
                if not user.bot:
                    break

                members_bots.append(True)

            if set(members_bots) == {True}:
                try:
                    before.channel.guild.voice_client.stop()
                    await before.channel.guild.voice_client.disconnect()

                except:
                    pass




def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
