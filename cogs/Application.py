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
        
        await interaction.response.send_message(f'Requirements for {position}:\n', ephemeral=True)