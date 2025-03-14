import qbittorrentapi
def qbt_log_in():
    """Login to qBittorrent and return qbt_client so it can be used in other functions"""
    conn_info = dict(
        host="localhost",
        port=8080,
        username="admin",
        password="adminadmin",
    )
    qbt_client = qbittorrentapi.Client(**conn_info)

    try:
        qbt_client.auth_log_in()
        # Manually check if the client is really authenticated.
        # For example, try fetching a known piece of info (e.g., app version).
        if not getattr(qbt_client.app, "version", None):
            raise qbittorrentapi.LoginFailed("Login did not succeed: no version info found.")
        
        print("Great success")
        return qbt_client
    except qbittorrentapi.LoginFailed as e:
        print(f"Login failed: {e}")
        return None
    except qbittorrentapi.APIConnectionError as e:
        print("Connection to server error")
        

