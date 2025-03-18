import feedparser
import asyncio
from bs4 import BeautifulSoup
url = "https://yts.mx/rss/0/all/documentary/5/en"


def fetch_rss_feed(url: str) -> feedparser.FeedParserDict | None:
    """
    Fetch and parse an RSS feed from a given URL.

    Args:
        url (str): The RSS feed URL.

    Returns:
        feedparser.FeedParserDict | None: Parsed feed data or None if an error occurs.
    """
    feed = feedparser.parse(url)

    # Check if the feed is malformed
    if feed.bozo:
        print(f"Warning: Malformed RSS feed or invalid URL ({url}).")
        print(f"Error details: {feed.get('bozo_exception')}")
        return None

    # Check if the feed has entries
    if not feed.entries:
        print("Warning: RSS feed has no entries.")
        return None

    return feed




def last_documentary():
    '''fetch last updated documentary from selected link, eventualy this function should be connected with telegram bot and bot should send notifications when list is updated'''
    rss_feed =fetch_rss_feed(url)
    if rss_feed == None:
        return "Empty list"
    else:
        first_entry = rss_feed.entries[0].summary
        torrent_link = rss_feed.entries[0].links[1].href
        
        soup = BeautifulSoup(first_entry, 'html.parser')
        result ={
            "title":soup.img["alt"],
            "image":soup.img["src"],
            "torrent_link": torrent_link,
            "website_link":soup.a["href"],
            "id":rss_feed.entries[0].id

        }
        return result
print(last_documentary())
def display_rss():
    d = feedparser.parse(url)
    print(d)

async def async_last_documentary():
    return await asyncio.to_thread(last_documentary)
