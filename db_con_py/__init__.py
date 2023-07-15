import asyncio
from db_con_py import discord, polaris


async def init():
    await polaris.init()
    await discord.init()
