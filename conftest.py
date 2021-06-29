import asyncio

import pytest
from braun.mq import Queue


@pytest.fixture(scope="session", autouse=True)
async def init():
    client = await Queue.get_client()
    await client.create_queue(QueueName="test")


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    res = policy.new_event_loop()
    asyncio.set_event_loop(res)
    res._close = res.close
    res.close = lambda: None

    yield res

    res._close()
