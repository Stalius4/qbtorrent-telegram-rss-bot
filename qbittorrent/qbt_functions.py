

def torrent_count(qbt_client):
    '''qbt_client will be in main.py  that is returned form login function'''
    torrents = qbt_client.torrents.info()
    num_torrents = len(torrents)
    print("Number of torrents:", num_torrents)
    qbt_client.auth_log_out()
    return num_torrents  # <-- Explicitly return the count
    


def list_all_torrents(qbt_client):
    for torrent in qbt_client.torrents_info():
        print(f"{torrent.hash[-6:]}: {torrent.name} ({torrent.state})")
    qbt_client.auth_log_out()