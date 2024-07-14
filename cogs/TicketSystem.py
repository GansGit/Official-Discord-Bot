from discord.commands import slash_command
import ezcord

class TicketSystem(ezcord.Cog, hidden=True):
    pass

def setup(bot):
    bot.add_cog(TicketSystem(bot))