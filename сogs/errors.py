import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import errors


class Errors(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):
		if isinstance(err, commands.UserInputError):
			await ctx.send(embed = discord.Embed(
				description = f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief}): `{ctx.prefix}{ctx.command.usage}`", color=0x6495ed 
		))
		elif isinstance(err, errors.MissingPermissions):
			await ctx.send(embed=discord.Embed(title= "Недостаточно прав!", description=f"У вас недостаточно прав для команды!", colour= 0x6495ed))
		elif isinstance(err, commands.errors.NSFWChannelRequired):
			await ctx.send(embed=discord.Embed(title= "Ошибка!", description=f"Использование данной команды разрешено только в NSFW каналах!", colour= 0x6495ed))
		elif isinstance(err, commands.CommandOnCooldown):
			h = int(err.retry_after)
			m = int((err.retry_after) - h * 3600)
			s = int(err.retry_after) % 60
			if h < 10:
				h = f"0{h}"
			if m < 10:
				m = f"0{m}"
			if s < 10:
				s = f"0{s}"
				time_reward = f"`{h}` Часов `{m}` минут `{s}` секунд"
			await ctx.send(embed=discord.Embed(title= "У вас кулдаун!", description=f"У вас не прошёл кулдаун! Осталось: `{time_reward}` ", colour= 0x6495ed))

		else:
			await ctx.send(embed=discord.Embed(title= "Неизвестная ошибка!", description=f"Произошла неизвестная ошибка: `{err}`\nПожалуйста, свяжитесь с техниеским админом для исправления этой ошибки", colour= 0x6495ed))

def setup(bot):
	bot.add_cog(Errors(bot))
	print('[Cog] Errors загружен!')