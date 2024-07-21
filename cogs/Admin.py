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
            title=f'<:home:1264678646531227751> › SERVER ANNOUNCEMENT',
            description="We have news for you all\n",
            color=discord.Colour.orange()
        )
        embed.set_image(url='https://media.discordapp.net/attachments/1259158345760243765/1264676190296211476/standard.gif?ex=669ebcfc&is=669d6b7c&hm=4ab19ed763ba768b5f5b501b1665858cc58ca652d07f297123f4dd9eaebf93eb&=&width=605&height=213')

        await interaction.response.send_message(embed=embed)
