#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import ssl
import terncy


async def foo():
    return "bar"

def event_hander(t, msg):
    print("got event", msg)

async def main():
    t = terncy.Terncy(
        "homeass_nbhQ43",
        "192.168.2.187",
        443,
        "homeassistant_user",
        "0269c4ce3f0440a3ab409433ba7440fc",
    )
    t.register_event_handler(event_hander)
    # await t.check_token_state(3, "0269c4ce3f0440a3ab409433ba7440fc")
    # await t.start()
    await t.discover()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
