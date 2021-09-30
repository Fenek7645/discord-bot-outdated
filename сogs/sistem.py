import discord
from discord.ext.commands.core import command
from discord.ext import commands
from discord.ext.commands import Bot
import os
from pymongo import MongoClient


class sistem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient("mongodb+srv://Fenek7645:qIFXybPrqBECqqcH@cluster0.aujkm.mongodb.net/ecodb?retryWrites=true&w=majority")
        self.collection = self.cluster.ecodb.colldb

    @commands.command(aliases = ['info'] )
    async def инфо(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.message.author
            data = self.collection.find_one({"_id": member.id})["balance"]
            lvl = self.collection.find_one({"_id": member.id})["lvl"]
            emb = discord.Embed(title='Информация', color=0x6495ed)
            emb.add_field(name='Когда присоединися', value=member.joined_at, inline=False)
            emb.add_field(name="Айди", value=member.id, inline=False)
            emb.add_field(name='Имя', value=member.display_name, inline=False)
            emb.add_field(name='Баланс',value=data, inline=False)
            emb.add_field(name='Уровень',value=lvl, inline=False)
            emb.set_thumbnail(url=member.avatar_url)
            emb.set_footer(text = f'{self.bot.user.name} © 2021', icon_url = self.bot.user.avatar_url)
            await ctx.send(embed = emb)
        else:
            data = self.collection.find_one({"_id": member.id})["balance"]
            lvl = self.collection.find_one({"_id": member.id})["lvl"]
            emb = discord.Embed(title='Информация', color=0x6495ed)
            emb.add_field(name='Когда присоединися', value=member.joined_at, inline=False)
            emb.add_field(name="Айди", value=member.id, inline=False)
            emb.add_field(name='Имя', value=member.display_name, inline=False)
            emb.add_field(name='Баланс',value=data, inline=False)
            emb.add_field(name='Уровень',value=lvl, inline=False)
            emb.set_thumbnail(url=member.avatar_url)
            emb.set_footer(text = f'{self.bot.user.name} © 2021', icon_url = self.bot.user.avatar_url)
            await ctx.send(embed = emb)

    #latancy
    @commands.command(aliases = ['latancy', 'ping'] )
    async def пинг(self, ctx):
        message = (f'Задержка {round(self.bot.latency * 1000)} мс.')
        embed_odj = discord.Embed(description = message, color= 0x6495ed)
        await ctx.send(embed = embed_odj)


def setup(bot):
    bot.add_cog(sistem(bot))
    print('[Cog] sistem загружен!')