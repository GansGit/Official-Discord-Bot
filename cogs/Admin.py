from discord.commands import slash_command
import discord
import ezcord
import datetime


class AdminTools(ezcord.Cog, hidden=True):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='Post the news!')
    @discord.default_permissions(administrator=True)
    async def news(self, ctx: discord.ApplicationContext):
        await ctx.send_modal(NewsModal(title='News', bot=self.bot))


def setup(bot):
    bot.add_cog(AdminTools(bot))


class NewsModal(discord.ui.Modal):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label='Heading',
                placeholder='Enter heading'
            ),
            discord.ui.InputText(
                label=f'Description',
                placeholder='Enter news description',
                style=discord.InputTextStyle.long
            )
            , *args, **kwargs)

        self.bot = bot

    async def callback(self, interaction):
        today = datetime.date.today()

        heading = self.children[0].value
        description = self.children[1].value

        embed = discord.Embed(
            title=f'<:home:1264678646531227751> › SERVER-NEWS',
            description=f"# {heading}\n\n{description}",
            color=discord.Colour.orange(),
            timestamp=datetime.datetime.now()
        )
        embed.set_image(url='https://media.discordapp.net/attachments/1259158345760243765/1264676190296211476/standard.gif?ex=669ebcfc&is=669d6b7c&hm=4ab19ed763ba768b5f5b501b1665858cc58ca652d07f297123f4dd9eaebf93eb&=&width=605&height=213')
        embed.set_footer(text='Coding Soul - News', icon_url='https://cdn.discordapp.com/attachments/1254423265707954178/1256938221665779763/coding-soul-high-resolution-logo-white.png?ex=669e45f0&is=669cf470&hm=30789a585bf50fdfc73d49a835e516983dd574551c433892af070c8509ee3b63&')

        channel: discord.TextChannel = await self.bot.fetch_channel(1265357865225424897)
        message = await channel.send(embed=embed)
        await message.publish()