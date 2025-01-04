import sqlite3
import feedparser
from bs4 import BeautifulSoup

# Database
db_name = 'rss_feeds.db'

# Function to create a SQLite database and a table
def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rss_feed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT,
            description TEXT,
            published_date TEXT,
            send INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert feed entry into the database
def insert_feed_entry(db_name, title, url, description, published_date, send):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO rss_feed (title, url, description, published_date, send)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, url, description, published_date, send))
    conn.commit()
    conn.close()

# Read RSS feed URLs from a text file
with open('rss_feeds.txt', 'r') as file:
    rss_urls = file.readlines()

# Strip whitespace characters like `\n` at the end of each line
rss_urls = [url.strip() for url in rss_urls]

# Specify the base URL you want to check against
base_url = 'https://pivot.quebec/'  # Replace with the specific base URL

# Create the database and table
create_database(db_name)

# Loop through each URL and parse the feed
for rss_url in rss_urls:
    feed = feedparser.parse(rss_url)

    # Access entry attributes
    for entry in feed.entries:
        # Get the author and published date, with defaults if not present
        author = entry.get('author', 'Unknown Author')
        published_date = entry.get('published', 'No Date Provided')

        # Check if the entry link starts with the specific base URL
        if entry.link.startswith(base_url):
            # Parse the entry description with BeautifulSoup
            soup = BeautifulSoup(entry.description, 'html.parser')

            # Find the first <p> tag
            first_paragraph = soup.find('p')

            # Use the first paragraph as the description if found, otherwise use the full description
            description = first_paragraph.get_text() if first_paragraph else entry.description
        else:
            description = entry.description

        # Insert the feed entry into the database
        insert_feed_entry(db_name, entry.title, entry.link, description, published_date, 0)  # Assuming 'send' is 0 for new entries

