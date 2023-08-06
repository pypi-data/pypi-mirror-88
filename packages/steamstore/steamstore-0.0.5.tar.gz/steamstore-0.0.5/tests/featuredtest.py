import steam
import asyncio

client = steam.Client()

async def test():

    await client.start()
    featured = await client.get_featured()
    
    [print(ff.name) for ff in featured.featured_win]

    client.stop()

loop = asyncio.get_event_loop()

loop.run_until_complete(test())