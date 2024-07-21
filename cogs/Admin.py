from discord.commands import slash_command
import discord
import ezcord
import datetime


class AdminTools(ezcord.Cog, hidden=True):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @discord.default_permissions(administrator=True)
    async def news(self, ctx: discord.ApplicationContext):
        await ctx.send_modal(NewsModal(title='News'))


def setup(bot):
    bot.add_cog(AdminTools(bot))


class NewsModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label=f'Print the news',
                placeholder='News... news... and more news!',
                style=discord.InputTextStyle.long
            )
            , *args, **kwargs)

    async def callback(self, interaction):
        today = datetime.date.today()
        embed = discord.Embed(
            title=f'{today} - News',
            description="We have news for you all\n",
            color=discord.Colour.orange()
        )

        await interaction.response.send_message(embed=embed)
