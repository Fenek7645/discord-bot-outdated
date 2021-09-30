import discord
from discord import message
from discord import embeds
from discord.ext import commands
from discord import Activity, ActivityType
import os
import asyncio
from discord.ext.commands import bot

from discord.ext.commands.bot import Bot


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_message_id = 882310245504942081 # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {
            discord.PartialEmoji(name='✅'): 881284495913943041, 
        }

    @commands.command()
    @commands.has_role(601771612701851662)
    async def react(self, ctx, *, message):
        await ctx.message.delete()
        embed_odj = discord.Embed(description=message, color=0x6495ed)
        message = await ctx.send(embed=embed_odj)
        await message.add_reaction('✅')

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


    @commands.command()
    @commands.has_any_role(601771612701851662)
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        embed_odj = discord.Embed(description=message, color=0x6495ed)
        await ctx.send(embed=embed_odj)


    @commands.command(aliases=['clear'])
    @commands.has_any_role(601771612701851662, 880893369516187699)  
    async def чистка(self, ctx, amount=1):  
        await ctx.message.channel.purge(limit=amount + 1)
        embed_odj = discord.Embed(description=f'❌ Вы удалили сообщения ❌', color=0x6495ed)
        await ctx.send(embed=embed_odj)
        await asyncio.sleep(3)
        await ctx.message.channel.purge(limit=1)
    
def setup(bot):
    bot.add_cog(General(bot))
    print('[Cog] General загружен!')