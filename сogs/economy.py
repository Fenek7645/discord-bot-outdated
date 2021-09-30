import discord
from discord.ext import commands
from pymongo import MongoClient, database

class Economic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient("mongodb+srv://Fenek7645:qIFXybPrqBECqqcH@cluster0.aujkm.mongodb.net/ecodb?retryWrites=true&w=majority")
        self.collection = self.cluster.ecodb.colldb

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user and message.channel.id == 800342728935997470:
            return
        
        channel = discord.utils.get(message.guild.channels, id=882175028295262248)
        user = message.author
        data = self.collection.find_one({"_id": user.id})
            
        if data["xp"] == 500 + 1000 * data["lvl"]:           
            self.collection.update_one({"_id": user.id},     
                {"$set": {"lvl": data["lvl"] + 1}})
            self.collection.update_one({"_id": user.id},
                {"$set": {"balance": data["balance"] + 100}})
            self.collection.update_one({"_id": user.id}, 
                {"$set": {"xp": 0}})
            await channel.send(f"👉{user.mention} + 1️⃣ уровень 👈") 
        else:
            self.collection.update_one({"_id": user.id},
                {"$set": {"xp": data["xp"] + 50}})


    @commands.command(
        name= "баланс",
        aliases = ["balance", "cash"],
        brief = "Просмотр баланса пользавотеля",
        usage= "баланс <@user>"
        )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def баланс(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(embed = discord.Embed(
                description = f"Баланс пользователя __{ctx.author}__: 💵 **{self.collection.find_one({'_id': ctx.author.id})['balance']}** 💵", color=0x6495ed
            ))
        else:
            await ctx.send(embed = discord.Embed(
                description = f"Баланс пользователя __{member}__: 💵 **{self.collection.find_one({'_id': member.id})['balance']}** 💵", color=0x6495ed
            ))

    @commands.command(
        name = "перевод",
        aliases = ["pay", "givecash"],
        brief = "Перевод денег другому пользователю",
        usage = "перевод <@user> <количесво>"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def перевод(self, ctx, member: discord.Member, amount: int):
        ubalance = self.collection.find_one({"_id": ctx.author.id})["balance"]
        mbalance = self.collection.find_one({"_id": member.id})["balance"]

        if amount <= 0:
            await ctx.send(embed = discord.Embed(
                description = f"{ctx.author}Что то вызывает скриптовые ошибки", color=0x6495ed
            ))
        else:
            self.collection.update_one({"_id": ctx.author.id},
                {"$set": {"balance": ubalance - amount}})

            self.collection.update_one({"_id": member.id},
                {"$set": {"balance": mbalance + amount}})

            await ctx.message.add_reaction("✅")


def setup(bot):
    bot.add_cog(Economic(bot))
    print('[Cog] Economic загружен!')
