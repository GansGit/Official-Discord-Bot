from discord.commands import slash_command
import ezcord
import discord


class TicketSystem(ezcord.Cog, hidden=True):
    pass


def setup(bot):
    bot.add_cog(TicketSystem(bot))


class TicketView(discord.ui.View):
    def __int__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Support', style=discord.ButtonStyle.primary, emoji='👮', custom_id='ticket-support-btn')
    async def button_callback(self, button, interaction: discord.Interaction):
        guild = interaction.guild
        channel: discord.TextChannel = await guild.create_text_channel(name=f'support-{interaction.user.id}')

        embed = discord.Embed(
            title='New Ticket created',
            description=f'Hey {interaction.user.mention}! Your Support-Ticket was successfully created. (Enter your '
                        f'Question / etc..)',
            color=discord.Color.brand_green()
        )

        await channel.send(embed=embed)
