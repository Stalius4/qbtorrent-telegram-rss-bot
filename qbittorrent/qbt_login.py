import qbittorrentapi

def qbt_log_in():
    '''Login to torrent and return qbt_client so it can be used to other functions'''
    # instantiate a Client using the appropriate WebUI configuration
    conn_info = dict(
        host="localhost",
        port=8080,
        username="admin",
        password="adminadmin",
    )
    qbt_client = qbittorrentapi.Client(**conn_info)

    # the Client will automatically acquire/maintain a logged-in state
    # in line with any request. therefore, this is not strictly necessary;
    # however, you may want to test the provided login credentials.
    try:
        qbt_client.auth_log_in()
        print("Great success ")
        return qbt_client
    except qbittorrentapi.LoginFailed as e:
        print(e)