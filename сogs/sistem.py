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
        self.role_message_id = 882310245504942081 # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {
            discord.PartialEmoji(name='⛏'): 880919466463088662,
            discord.PartialEmoji(name='🕯'): 880895891546968074,
            discord.PartialEmoji(name='🕹'): 880905281008173097,
            discord.PartialEmoji(name='🧙'): 882290339891793940,
        }
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
    
    @commands.command()
    @commands.has_role(601771612701851662)
    async def react2(self, ctx, *, message):
        await ctx.message.delete()
        embed_odj = discord.Embed(description=message, color=0x6495ed)
        message = await ctx.send(embed=embed_odj)
        await message.add_reaction('⛏')
        await message.add_reaction('🕯')
        await message.add_reaction('🕹')
        await message.add_reaction('🧙')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            await payload.member.add_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass
    #latancy
    @commands.command(aliases = ['latancy', 'ping'] )
    async def пинг(self, ctx):
        message = (f'Задержка {round(self.bot.latency * 1000)} мс.')
        embed_odj = discord.Embed(description = message, color= 0x6495ed)
        await ctx.send(embed = embed_odj)


def setup(bot):
    bot.add_cog(sistem(bot))
    print('[Cog] sistem загружен!')