from discord.commands import slash_command
import ezcord
import discord
from discord.ext import commands


class TicketSystem(ezcord.Cog, hidden=True):
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(TicketView())

    @slash_command()
    @discord.default_permissions(administrator=True)
    async def setup_ticket(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title='Ticket System',
            color=discord.Colour.green(),
            description='Select the type of the ticket you want to create:'
        )

        await ctx.send(embed=embed, view=TicketView())


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
