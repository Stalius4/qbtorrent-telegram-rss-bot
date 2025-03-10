from qbittorrent import qbt_login, qbt_functions



def main():
  
    qbt_client =qbt_login.qbt_log_in()
    qbt_functions.torrent_count(qbt_client)
    qbt_functions.list_all_torrents(qbt_client)
if __name__ == '__main__':
    main()