## Learning outcomes

-Setup local connection with qbt

-Add and test functionalities:

- Check how many torrents have

- List all my torrents

- Stop/resume torrents

- Download torrent with given link

  

If I manage to do all the things listed above I can try to implement rrs feed link

## Async vs. Sync

While reading the qBittorrent documentation, I looked at the async support section. I knew from past experience that it was related to the event loop and I/O blocking, but I never completely understood why we need to use it. This example helped me gain a better understanding:

I am using an asynchronous Telegram bot that is constantly waiting for messages from users. This means that the event loop must not be blocked. Since the qBittorrent API is synchronous, if one of my functions takes a long time to execute, it will prevent the bot from listening for incoming commands and drastically slow down its functionality.

To avoid this, the documentation provided the following solution:

```python
import asyncio
import qbittorrentapi

qbt_client = qbittorrentapi.Client()

async def fetch_qbt_info():
    return await asyncio.to_thread(qbt_client.app_build_info)

print(asyncio.run(fetch_qbt_info()))
```
With this code, the qBittorrent API call is executed in a separate thread, preventing it from blocking the event loop.