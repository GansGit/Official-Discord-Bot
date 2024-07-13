import discord
from discord.commands import slash_command, SlashCommandGroup

import ezcord

class Application(ezcord.Cog):
    
    application = SlashCommandGroup("application")
    
    @application.command(description="Displays the requirements for the different positions.")
    async def requirements(self, ctx):
        embed = discord.Embed(
            title="Requirements for Application",
            description="Select the position you want apply to",
            color=discord.Colour.blurple()
        )
        
        await ctx.respond(embed=embed, ephemeral=True, view=RequirementView())
    
    @application.command(description="Send your application")
    async def send(self, ctx):
        await ctx.send_modal(ApplicationModal(title="Application", bot=self.bot))
    
def setup(bot):
    bot.add_cog(Application(bot))
    
class RequirementView(discord.ui.View):
    
    options = [
        discord.SelectOption(label='Moderator - Open', description='Moderate the chat', emoji='👮'),
        discord.SelectOption(label='Developer - Closed', description='Develope on the system', emoji='<:python:1259196508906197054>'),
        discord.SelectOption(label='Creator - Open', description='Promote your social media', emoji='📣'),
        discord.SelectOption(label='Partner - Open', description='Promote your discord server', emoji='🤝')
    ]
    
    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder='Select position',
        options=options
    )
    async def select_callback(self, select, interaction):
        position = select.values[0]
        
        if position == 'Moderator':
            req = "* Min. 16y/o\n* Experience in Moderating\n* Motivation to work\n* Friendly and helpful"
        elif position == 'Developer':
            req = "* Min. 16y/o\n* Basics of Progamming\n* One of the following languages: Python or JavaScript\nAdditional skills are necessary"
        elif position == 'Creator':
            req = "* Min. \n    50 Followers on Twich /\n    500 on Instagram /\n    1000 on YouTube"
        elif position == 'Partner':
            req = "* Not available yet"
        
        embed=discord.Embed(
            title=f'Requirements for {position}',
            color=discord.Colour.blurple(),
            description=f"{req}"
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
class ApplicationModal(discord.ui.Modal):
    def __init__(self, *args, bot, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label=f'POSITION',
                placeholder='On which role are you applying to?',
                style=discord.InputTextStyle.short
            ),
            discord.ui.InputText(
                label=f'Personal Statement',
                placeholder='Write down your Personal Statement (Describe yourself / e.g. age / motivation etc...).',
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label=f'Strengths',
                placeholder='Tell us something about your strengths.',
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label=f'Weaknesses',
                placeholder='Tell us something about your- weaknesses.',
                style=discord.InputTextStyle.long
            ),
            *args, **kwargs)
        self.bot = bot
        
    async def callback(self, interaction):
        channel = await self.bot.fetch_channel(1261658865129226240)
        
        embed_personal_statement = discord.Embed(
            title='Personal Statement',
            color=discord.Colour.blurple(),
            description=f'{self.children[1].value}'
        )
        
        embed_strengths = discord.Embed(
            title='Strengths',
            color=discord.Colour.blurple(),
            description=f'{self.children[2].value}'
        )
        
        embed_weaknesses = discord.Embed(
            title='Weaknesses',
            color=discord.Colour.blurple(),
            description=f'{self.children[3].value}'
        )
        
        await channel.send(f"Application by: {interaction.user.mention} / For: {self.children[0].value}", embed=embed_personal_statement)
        await channel.send(embed=embed_strengths)
        await channel.send(embed=embed_weaknesses)
        
        await interaction.response.send_message('Application was successfully sent.', ephemeral=True)
        