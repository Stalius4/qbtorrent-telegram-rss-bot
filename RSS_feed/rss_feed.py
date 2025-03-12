import feedparser

from bs4 import BeautifulSoup
url = "https://yts.mx/rss/0/all/documentary/5/en"

def last_documentary():
    '''fetch last updated documentary from selected link, eventualy this function should be connected with telegram bot and bot should send notifications when list is updated'''
    d = feedparser.parse(url)
    first_entry = d.entries[0].summary
    torrent_link = d.entries[0].links[1].href
    soup = BeautifulSoup(first_entry, 'html.parser')
    result ={
        "title":soup.img["alt"],
        "image":soup.img["src"],
        "torrent_link": torrent_link


    }
    print(result)