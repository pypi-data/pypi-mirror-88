import steam
import asyncio
import sys

client = steam.Client()

async def test():
    if len(sys.argv) < 2 or not sys.argv[1].isdigit():
        return print("Invalid app id! Usage: python [file] [appid:int]")
    
    await client.start()
    app = await client.get_app_from_id(int(sys.argv[1]))
    if app is None:
        print("Invalid app id!")
    else:
        print(app.name)
    client.stop()

loop = asyncio.get_event_loop()

loop.run_until_complete(test())