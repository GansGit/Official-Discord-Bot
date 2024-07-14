from discord.commands import slash_command
import ezcord
import discord
from discord.ext import commands
from cogs.Config import Config


class TicketSystem(ezcord.Cog, hidden=True):
    @commands.Cog.listener()
    async def on_ready(self):
        view = TicketView()
        self.bot.add_view(view)
        print(f'Bot is ready. Loaded persistent views.')

    @slash_command()
    @discord.default_permissions(administrator=True)
    async def setup_ticket(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title='Ticket System',
            color=discord.Colour.green(),
            description='Select the type of the ticket you want to create'
        )
        embed.set_footer(text='Coding Soul - TicketSystem', icon_url=Config.get_config('footer')['icon-url'])

        await ctx.send(embed=embed, view=TicketView())
        await ctx.respond('Made successfully a setup of the ticket system.', ephemeral=True)

def setup(bot):
    bot.add_cog(TicketSystem(bot))


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.support_button = discord.ui.Button(label='Support', custom_id='ticket_support_btn',
                                                style=discord.ButtonStyle.primary, emoji='👮')
        self.report_bug_button = discord.ui.Button(label='Report Bug', custom_id='ticket_report_bug_btn',
                                                   style=discord.ButtonStyle.primary, emoji='🤯')
        self.support_button.callback = self.support_button_callback
        self.report_bug_button.callback = self.report_bug_button_callback
        self.add_item(self.support_button)
        self.add_item(self.report_bug_button)

    async def support_button_callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        channel_name = f'support-{interaction.user.id}'

        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f'A channel with the name {channel_name} already exists.',
                                                    ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        category = discord.utils.get(guild.categories, id=1256616177887875153)
        channel: discord.TextChannel = await guild.create_text_channel(name=channel_name, overwrites=overwrites,
                                                                       category=category)

        embed = discord.Embed(
            title='New Ticket created',
            description=f'Your Support-Ticket was successfully created. (Enter your Question / etc..)',
            color=discord.Color.brand_green()
        )

        await channel.send(f"{interaction.user.mention}", embed=embed)
        await interaction.response.send_message(f'Ticket channel {channel_name} created.', ephemeral=True)

    async def report_bug_button_callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        channel_name = f'bug-{interaction.user.id}'

        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f'A channel with the name {channel_name} was already exists.',
                                                    ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        category = discord.utils.get(guild.categories, id=1256616177887875153)
        channel: discord.TextChannel = await guild.create_text_channel(name=channel_name, overwrites=overwrites,
                                                                       category=category)

        embed = discord.Embed(
            title='New Ticket created',
            description=f'Your Bug-Report-Ticket was successfully created. (Enter Bug! Please include Screenshots!)',
            color=discord.Color.brand_green()
        )

        await channel.send(f"{interaction.user.mention}", embed=embed)
        await interaction.response.send_message(f'Ticket channel {channel_name} was created.', ephemeral=True)