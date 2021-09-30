import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
import requests
import json
import random


class Fan(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#Cat
	@commands.command(
		name= "Коты",
		aliases = ['Кот', 'кот', 'rjn', 'rjns'],
		brief= "Выводит изображения котов",
		usage= "Коты"
	)

	@commands.cooldown(1, 5, commands.BucketType.user)
	async def коты(self, ctx):
		response = requests.get('https://some-random-api.ml/img/cat')
		json_data = json.loads(response.text)
		emb = discord.Embed(title = "🐱Рандомные коты🐱",color =0x6495ed)
		emb.set_image(url = json_data['link'])
		emb.set_footer(text = f'{self.bot.user.name} © 2021 ', icon_url = self.bot.user.avatar_url)
		await ctx.send(embed = emb)

	#Hug
	@commands.command(
		name= "обнять",
		aliases = ['Обьятие'],
		brief= "Позволяет сделять счастливее мир",
		usage= "обнять <@user>",
		)
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def обнять(self, ctx, member : discord.Member = None):
		response = requests.get('https://some-random-api.ml/animu/hug')
		json_data = json.loads(response.text)
		if member == None:
			embed = discord.Embed(title = f"{ctx.author} обнял'а {self.bot.user.name}",color =0x6495ed)
			embed.set_image(url = json_data['link'])
			embed.set_footer(text = f'{self.bot.user.name} © 2021 ', icon_url = self.bot.user.avatar_url)
			await ctx.send(embed = embed)
		else:
			embed = discord.Embed(title = f"{ctx.author} обнял'а {member}",color =0x6495ed)
			embed.set_image(url = json_data['link'])
			embed.set_footer(text = f'{self.bot.user.name} © 2021 ', icon_url = self.bot.user.avatar_url)
			await ctx.send(embed = embed)
	
	#Coin
	@commands.command(
		name="монетка",
		aliases = ['coin', 'Coin', 'vjytnrf', 'Монетка'],
		brief= "Позволяет подкинуть монетку",
		usage= "Монетка"
		)
	@commands.cooldown(1, 5, commands.BucketType.user) 
	async def монетка(self, ctx):
		if random.randint(1, 2) == 1:
			emb = discord.Embed(title ='Выпала решка',color=0x6495ed)
			file = discord.File("решка.jpg")
			emb.set_image(url="https://cdn.discordapp.com/attachments/834869147363442751/849777537495203870/86b3c01fa0c78b21.jpg")
			emb.set_footer(text = f'{self.bot.user.name} © 2021', icon_url = self.bot.user.avatar_url)
			await ctx.send(embed = emb)
		else:
			emb = discord.Embed(title = 'Выпал орел', color=0x6495ed)
			file = discord.File("орел.jpg")
			emb.set_image(url="https://cdn.discordapp.com/attachments/834869147363442751/849777529459048488/72cf6483d1f78ba9.jpg")
			emb.set_footer(text = f'{self.bot.user.name} © 2021 ', icon_url = self.bot.user.avatar_url)
			await ctx.send(embed = emb)
		




def setup(bot):
	bot.add_cog(Fan(bot))
	print('[Cog] Fan загружен!')