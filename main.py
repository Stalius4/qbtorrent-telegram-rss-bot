from qbittorrent import qbt_login, qbt_functions
import asyncio






def main():
  
    qbt_client =qbt_login.qbt_log_in()
    # Check if login is successful 
    if qbt_client is None:
        print("Login failed; stopping execution.")
        return
    asyncio.run(qbt_functions.async_add_torrent(qbt_client))
    # asyncio.run(qbt_functions.async_torrent_count(qbt_client))
    # asyncio.run(qbt_functions.async_list_all_torrents(qbt_client))
if __name__ == '__main__':
    main()

#Button to add the torrent is working, but in need to be adjusted to rss feed 
#rss feed is sending last updated movie. In there should be link for torrent.
# torrent_link = rss_function()     returns last updated movie link
# asyncio.run(qbt_functions.async_add_torrent(qbt_client, torrent_link))