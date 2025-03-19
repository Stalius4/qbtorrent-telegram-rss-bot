import feedparser
import asyncio
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urlunparse
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







def extract_attribute_from_tag(html_content, tag_name, attribute):
    """
    Extracts a specified attribute from the first occurrence of a given HTML tag.

    Parameters:
    - html_content (str): The raw HTML content.
    - tag_name (str): The name of the HTML tag to search for.
    - attribute (str): The attribute whose value needs to be extracted.

    Returns:
    - str or None: The value of the specified attribute if found, otherwise None.
    """
    soup = BeautifulSoup(html_content, "html.parser")  # Parse the HTML content
    element = getattr(soup, tag_name, None)  # Get the first occurrence of the specified tag

    if element and attribute in element.attrs:
        return element[attribute]  # Return the attribute value if it exists
    
    return None  # Return None if the tag or attribute is not found



def find_trailer_link(url):
    """
    Extracts the first YouTube link from the given webpage and removes extra parameters.

    Parameters:
    - url (str): The webpage URL to scrape.

    Returns:
    - str or None: The cleaned YouTube link (without parameters) or None if not found.
    """
    # Extract main website link first
    website_link = extract_attribute_from_tag(url, "a", "href")

    try:
        # Fetch the webpage content
        response = requests.get(website_link, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Ensure the request was successful

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all links on the page
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "youtube.com" in href or "youtu.be" in href:
                # Clean the YouTube URL (remove parameters)
                parsed_url = urlparse(href)
                clean_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", "", ""))
                return clean_url  # Return the first found and cleaned YouTube link

        return None  # No YouTube link found

    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None
    
    

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
            "id":rss_feed.entries[0].id,
            "trailer":find_trailer_link(first_entry)
        }
        return result

def display_rss():
    d = feedparser.parse(url)
    print(d)

async def async_last_documentary():
    return await asyncio.to_thread(last_documentary)
