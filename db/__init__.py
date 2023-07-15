import asyncio
from db import discord, polaris


async def init():
    await polaris.init()
    await discord.init()
