import feedparser
from bs4 import BeautifulSoup

# Read RSS feed URLs from a text file
with open('rss_feeds.txt', 'r') as file:
    rss_urls = file.readlines()

# Strip whitespace characters like `\n` at the end of each line
rss_urls = [url.strip() for url in rss_urls]

# Specify the base URL you want to check against
base_url = 'https://pivot.quebec/'  # Replace with the specific base URL

# Loop through each URL and parse the feed
for rss_url in rss_urls:
    print(f"Fetching feed from: {rss_url}")
    feed = feedparser.parse(rss_url)

    # Access feed attributes
    print(f"Feed Title: {feed.feed.title}\n")

    # Access entry attributes
    for entry in feed.entries:
        print(f"Title: {entry.title}")
        print(f"Link: {entry.link}")
        
        # Check if author information is available and print it
        if 'author' in entry:
           print(f"Author: {entry.author}")
        
        print(f"Published: {entry.published}")

        # Check if the entry link starts with the specific base URL
        if entry.link.startswith(base_url):
            # Parse the entry description with BeautifulSoup
            soup = BeautifulSoup(entry.description, 'html.parser')
            
            # Find the first <p> tag
            first_paragraph = soup.find('p')
            
            # Check if a <p> tag was found and print it
            if first_paragraph:
                print(f"First Paragraph: {first_paragraph.get_text()}\n")
            else:
                print("No <p> tag found in the description.\n")
        else:
            print(f"Description: {entry.description}\n")
