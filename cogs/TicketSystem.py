from discord.commands import slash_command
import ezcord
import discord


class TicketSystem(ezcord.Cog, hidden=True):
    pass


def setup(bot):
    bot.add_cog(TicketSystem(bot))


class TicketView(discord.ui.View):
    @discord.ui.button(label='Support', style=discord.ButtonStyle.primary, emoji='👮')
    async def button_callback(self, button, interaction: discord.Interaction):
