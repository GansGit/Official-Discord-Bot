import subprocess

from discord.commands import slash_command, SlashCommandGroup
import discord
import ezcord
from cogs.AcademyConfig import Config
from cogs.Config import Config as BotConfig
import json
import ast
import io
import contextlib


class Academy(ezcord.Cog, hidden=True):
    academy = SlashCommandGroup('academy', description='The Academy is the place where you can learn coding from Zero!')
    lesson = academy.create_subgroup('lesson')

    def __init__(self, bot):
        super().__init__(bot)
        self.config = Config('courses.json')

    @academy.command(description="Show's the profile of a user!")
    async def profile(self, ctx):
        user_id_str = str(ctx.user.id)
        courses = self.config.load_config()
        value = "No courses enrolled"
        if user_id_str in courses:
            data = courses[user_id_str].get('courses', [])

            if 'python' in data:
                level = courses[user_id_str].get('courses')['python']['level']

                if level >= 5:
                    value = '<:py_rank_2:1259426955393241192>'
                if level >= 10:
                    value = '<:python:1259196508906197054>'
                if level < 5:
                    value = '<:py_rank_1:1259426957175685170>'

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
        embed.set_footer(text=f'Coding Soul - Course Selection', icon_url=self.bot.user.avatar.url)

        await ctx.respond(embed=embed, view=CourseView(self.config), ephemeral=True)

    @lesson.command(description="Show's your current lesson.", name='task')
    async def task(self, ctx: discord.ApplicationContext,
                   language: discord.Option(str, choices=['python'])):  # type: ignore

        user_id_str = str(ctx.user.id)
        courses = self.config.load_config()

        value = "No courses enrolled"
        if user_id_str in courses:
            data = courses[user_id_str].get('courses', [])

            if language in data:
                module = data[language]['module']
                level = data[language]['level']
                print(module)
                print(level)

            with open(f'{language}.json', 'r') as f:
                json_data = json.load(f)
            try:
                task = json_data[f'level-{level}'][f'module-{module}']['task']
                embed = discord.Embed(
                    title=f'Current lesson | {language}',
                    description=f"### Todo: {task}\n\n**Tip:** Prepare the code in your IDE. When you are finished, you enter: /academy lesson solve and you'll get an Modal.",
                    color=discord.Color.blue()
                )
                embed.set_footer(text=f'Coding Soul - Lesson', icon_url=self.bot.user.avatar.url)
                await ctx.respond(embed=embed, ephemeral=True)
            except KeyError:
                await ctx.respond("You've reached the final level! :tada:", ephemeral=True)


        else:
            await ctx.respond('This course is not enrolled.')

    @lesson.command(description="Show's you a modal for entering your code!")
    @discord.default_permissions(administrator=True)
    async def solve(self, ctx):

        result = "abc"

        await ctx.send_modal(LessonModal(title='Lesson', result=result))

    @academy.command()
    async def ressources(self, ctx: discord.ApplicationContext,
                         language: discord.Option(str, choices=['Python'])):  # type: ignore

        if language == 'Python':
            await ctx.respond("Python Ressources: <:python:1259196508906197054>", ephemeral=True,
                              view=PythonRessourceView())


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
    def __init__(self, result, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(
            label='Solution',
            placeholder='Print the code out here!',
            style=discord.InputTextStyle.long
        ))
        self.solution = result

    async def callback(self, interaction):
        code_input = self.children[0]  # Saving Code
        code = code_input.value  # Get the actual text from the InputText object
        print(f"Code received: {code}")

        output_buffer = io.StringIO()

        with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(output_buffer):
            try:
                exec(code)
            except Exception as e:
                print(f'Error: {e}')

        # Get the output from the buffer
        output = output_buffer.getvalue()
        print(f"Execution output: {output}")

        # Optionally send the output back to the user via Discord interaction
        await interaction.response.send_message(f"Execution output:\n{output}", ephemeral=True)

class PythonRessourceView(discord.ui.View):
    options = [
        discord.SelectOption(label='Basics', description='Basics of python', emoji='<:python:1259196508906197054>')
    ]

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder='Select category',
        options=options
    )
    async def select_callback(self, select, interaction):
        category = select.values[0]

        if category == 'Basics':
            embed = discord.Embed(
                title=f'Ressources for python',
                description=f"Hey {interaction.user.mention}\nYou'll find ressources for python basics [here](https://creative-dreamer.gitbook.io/coding-soul-python-course/basics/operators#comparision)",
                color=discord.Colour.blurple()
            )
            embed.set_thumbnail(
                url='https://media.discordapp.net/attachments/1259158345760243765/1260589734757924924/python_logo.png?ex=668fdf2d&is=668e8dad&hm=e19afe81586d1b896f1d33f5e6cf0fc2e5691372867ad010d7398fb56ab0cffa&=&format=webp&quality=lossless&width=385&height=385')
            embed.set_footer(text='Coding Soul - Academy Ressources',
                             icon_url=BotConfig.get_config('footer')['icon-url'])

        await interaction.response.send_message(embed=embed, ephemeral=True)
