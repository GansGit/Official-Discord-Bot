from discord.commands import slash_command
import ezcord
import discord


class TicketSystem(ezcord.Cog, hidden=True):
    pass


def setup(bot):
    bot.add_cog(TicketSystem(bot))


class TicketView(discord.ui.View):
