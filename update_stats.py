import discord


class Updater():
    def __init__(self, bot):
        self.bot = bot

    async def update(self):
        channel = await self.bot.fetch_channel(1259432546786349126)

        try:
            message = await channel.fetch_message(1259435457054380103)
            bots = 0
            async for member in channel.guild.fetch_members(limit=None):
                if member.bot:
                    bots += 1

            embed = discord.Embed(
                title=':chart_with_upwards_trend: Server Stats',
                color=discord.Color.green()
            )
            embed.add_field(name='Members', value=f"{channel.guild.member_count - bots}", inline=False)
            embed.add_field(name='Text channels', value=len(channel.guild.text_channels), inline=False)
            embed.add_field(name='Voice channels', value=len(channel.guild.voice_channels), inline=False)
            embed.add_field(name='Roles', value=len(channel.guild.roles), inline=False)
            embed.set_footer(icon_url=self.bot.user.avatar.url, text='Coding Soul - Stats')

            await message.edit(embed=embed)
        except discord.NotFound:
            print('Nachricht wurde nicht gefunden')
        except discord.Forbidden:
            print("Fehlende Berechtigung")
        except discord.HTTPException as e:
            print(f'HTTP-Fehler: {e}')
