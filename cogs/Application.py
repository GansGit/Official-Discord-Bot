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
        await ctx.send_modal(ApplicationModal(title="Application"))
    
def setup(bot):
    bot.add_cog(Application(bot))
    
class RequirementView(discord.ui.View):
    
    options = [
        discord.SelectOption(label='Moderator', description='Moderate the chat', emoji='👮'),
        discord.SelectOption(label='Developer', description='Develope on the system', emoji='<:python:1259196508906197054>'),
        discord.SelectOption(label='Creator', description='Promote your social media', emoji='📣'),
        discord.SelectOption(label='Partner', description='Promote your discord server', emoji='🤝')
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
    def __init__(self, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label=f'POSITION',
                placeholder='On which role are you applying to?',
                style=discord.InputTextStyle.short
            ),
            discord.ui.InputText(
                label=f'Personal Statement',
                placeholder='Write down your Personal Statement (Why are you applying for / and so on...).',
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label=f'Strengths',
                placeholder='Tell us something about your strengths.',
                style=discord.InputTextStyle.long
            ),
            discord.ui.InputText(
                label=f'Weaknesses',
                placeholder='Tell us something about your weaknesses.',
                style=discord.InputTextStyle.long
            ),
            *args, **kwargs)
        
    async def callback(self, interaction):
        pass