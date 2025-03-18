import asyncio
import qbittorrentapi

# Get torrent count
def torrent_count(qbt_client):
    '''qbt_client will be in main.py  that is returned form login function'''
    torrents = qbt_client.torrents.info()
    num_torrents = len(torrents)
    print("Number of torrents:", num_torrents)
    qbt_client.auth_log_out()
    return num_torrents  # <-- Explicitly return the count
    
async def async_torrent_count(qbt_client):
    return await asyncio.to_thread(torrent_count, qbt_client)


#Display all saved torrents
def list_all_torrents(qbt_client):
    torrents = qbt_client.torrents_info()
    if not torrents:
        return "No active torrents found."

    torrent_list = "\n".join(
        [f"{i+1}.{torrent.name}: ({torrent.state})" for i,torrent in enumerate(torrents)]
    )

    qbt_client.auth_log_out()

    return torrent_list

async def async_list_all_torrents(qbt_client):
    return await asyncio.to_thread(list_all_torrents, qbt_client)




def add_torrent(qbt_client, url):
    try:
        torrent = qbt_client.torrents_add(urls=url)
        print(torrent)
        if torrent != "Ok.":
            print("Wrong magnet link.")
            return torrent
    except qbittorrentapi.UnsupportedMediaType415Error:
        print("Error: Unsupported media type for this torrent file.")
    except qbittorrentapi.TorrentFileNotFoundError:
        print("Error: Torrent file was not found.")
    return None

async def async_add_torrent(qbt_client):
   return await asyncio.to_thread(add_torrent, qbt_client) 