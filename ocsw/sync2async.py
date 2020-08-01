import asyncio

import aiohttp

from .api.client import APIClient
from .utils.config import Config


def run(func, **kwargs):
    if asyncio.iscoroutinefunction(func):
        loop = asyncio.get_event_loop()
        future = start_cmd(func=func, **kwargs)
        return loop.run_until_complete(future)
    if callable(func):
        return func(**kwargs)
    raise Exception("func must be callable")


async def start_cmd(func, **kwargs):
    config_path = kwargs["config_path"]
    config_filename = kwargs["config_filename"]
    config = Config(
        config_path=config_path, config_filename=config_filename
    ).as_dict()
    async with aiohttp.ClientSession() as session:
        client = APIClient(session=session, **config)
        return await func(client=client, **kwargs)
