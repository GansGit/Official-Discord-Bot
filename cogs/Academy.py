from discord.commands import slash_command, SlashCommandGroup
import discord
import ezcord
from cogs.AcademyConfig import Config
from cogs.Config import Config as BotConfig
import json

class Academy(ezcord.Cog, hidden=True):
    academy = SlashCommandGroup('academy', description='The Academy is the place where you can learn coding from Zero!')
    
    def __init__(self, bot):
        super().__init__(bot)
        self.config = Config('courses.json')

    @academy.command(description="Show's the profile of a user!")
    async def profile(self, ctx):
        user_id_str = str(ctx.user.id)
        
        courses = self.config.load_config()
        
        # Initialisiere value standardmäßig
        value = "No courses enrolled"
        
        # Prüfe, ob die Benutzer-ID in der Konfiguration existiert
        if user_id_str in courses:
            data = courses[user_id_str].get('courses', [])
            
            if 'python' in data:
                value = '<:python:1259196508906197054>'
        
        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s profile",
            color=discord.Color.blue()
        )
        embed.add_field(name='Courses', value=value)
        
        await ctx.respond(embed=embed)
    
    @academy.command(description="Gives you a overview over all the courses")
    async def courses(self, ctx):
        
        embed = discord.Embed(
            title='Course Selection',
            description='1. <:python:1259196508906197054> Python',
            color=discord.Color.blue()
        )
        embed.set_footer(text=f'{BotConfig.get_config('footer')['text']} - Course Selection', icon_url=ctx.author.avatar.url)
        
        await ctx.respond(embed=embed, view=CourseView(self.config), ephemeral=True)
    
    @academy.command(description="Show's your current lesson.")
    @discord.option('language', type=discord.SlashCommandOptionType.string)
    async def lesson(self, ctx, language: str):
        
        user_id_str = str(ctx.user.id)
        courses = self.config.load_config()
        
        # Initialisiere value standardmäßig
        value = "No courses enrolled"
        # Prüfe, ob die Benutzer-ID in der Konfiguration existiert
        if user_id_str in courses:
            data = courses[user_id_str].get('courses', [])
            
            if language in data:
                module = f'{data[language]['module']}'
                level = f'{data[language]['level']}'
        
            embed = discord.Embed(
                title=f'Current lesson',
                description=f'Language: {language}\nLevel: {level}\nModule: {module}',
                color=discord.Color.blue()
            )
            embed.set_footer(text=f'{BotConfig.get_config('footer')['text']} - Lesson', icon_url=ctx.author.avatar.url)
            
            with open(f'{language}.json', 'r') as f:
                json_data = json.load(f)
            task = json_data[f'level-{level}'][f'module-{module}']['task']
            result = json_data[f'level-{level}'][f'module-{module}']['result']
            
            modal = LessonModal(title='Lesson', task=task, result=result)
            await ctx.send_modal(modal)
        else:
            await ctx.respond('This course is not enrolled.')
        
    
def setup(bot):
    bot.add_cog(Academy(bot))

class CourseView(discord.ui.View):
    def __init__(self, config):
        super().__init__()
        self.config = config

    @discord.ui.button(label="Python", style=discord.ButtonStyle.secondary, emoji="<:python:1259196508906197054>")
    async def python_callback(self, button, interaction):
        self.config.add_course_to_user(interaction.user.id, 'python')
        await interaction.response.send_message('Python Course was added to your courses!', ephemeral=True)

class LessonModal(discord.ui.Modal):
    def __init__(self, task, result, *args, **kwargs):
        super().__init__(
            discord.ui.InputText(
                label=f'Task:',
                placeholder=f"Do not delete: {task}",
                style=discord.InputTextStyle.long,
                required=False
            ), discord.ui.InputText(
                label=f'Solution',
                placeholder='Print the code out here!'
            )
            ,*args, **kwargs)