import discord
from discord.ext import commands
from discord.ext.commands import Bot
import os
import logging
from Config import settings
from discord import Activity, ActivityType
import pymongo


clusterr = pymongo.MongoClient("mongodb+srv://Fenek7645:hKHTjZTvCfS7D2fn@cluster0.aujkm.mongodb.net/ecodb?retryWrites=true&w=majority")
collection = clusterr.ecodb.colldb
 


bot = commands.Bot(command_prefix = settings['prefix'], intents=discord.Intents.all())
bot.remove_command('help')


for filename in os.listdir("./сogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"сogs.{filename[:-3]}")

@bot.event
async def on_ready():
	await bot.change_presence(status=discord.Status.online, activity=discord.Game('.помощь'))

	for guild in bot.guilds:
		for member in guild.members:
			post = {
				"_id": member.id,
				"balance": 500,
				"xp": 0,
				"lvl": 1
			}

			if collection.count_documents({"_id": member.id}) == 0:
				collection.insert_one(post)
	print("started")


@bot.event
async def on_member_join(member):
	file = discord.File("hi.gif")
	channel = bot.get_channel(791709222937034752)
	role_1 = member.guild.get_role(role_id=601762430024155155)
	emb = discord.Embed(title='Новый учасник', color=0x6495ed)
	emb.add_field(name='Имя', value=member.mention, inline=False)
	emb.set_image(url="attachment://hi.gif")
	emb.set_thumbnail(url=member.avatar_url)
	emb.set_footer(text = f'{bot.user.name} © 2021', icon_url = bot.user.avatar_url)
	await member.add_roles(role_1)
	await channel.send(embed = emb, file=file)
	post = {
		"_id": member.id,
		"balance": 500,
		"xp": 0,
		"lvl": 1
	}

	if collection.count_documents({"_id": member.id}) == 0:
		collection.insert_one(post)


@bot.event
async def on_voice_state_update(member, before, after):
	if after.channel.id == 773114804067237909:
		for guild in bot.guilds:
			maincategory = discord.utils.get(guild.categories, id=773114920870346782)
			channel2 = await guild.create_voice_channel(name=f'канал {member.display_name}', category = maincategory)
			await channel2.set_permissions(member, connect=True, mute_members=True, manage_channels=True)
			await member.move_to(channel2)
			def check(x, y, z):
				return len(channel2.members) == 0
			await bot.wait_for('voice_state_update', check=check)
			await channel2.delete()
			
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
	bot.unload_extension(f"cogs.{extension}")
	bot.load_extension(f"cogs.{extension}")
bot.run(settings['token'])