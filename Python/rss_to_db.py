import sqlite3
import feedparser
import re
from datetime import datetime
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
            author TEXT,
            url TEXT,
            description TEXT,
            published_date TEXT,
            tags TEXT,
            send INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert feed entry into the database
def insert_feed_entry(db_name, title, author, url, description, published_date, tags, send):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO rss_feed (title, author, url, description, published_date, tags, send)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, author, url, description, published_date, tags, send))
    conn.commit()
    conn.close()

# Function to update feed entry in the database if the URL exists
def update_feed_entry(db_name, title, author, url, description, published_date, tags):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Check if the URL exists
    cursor.execute('''
        SELECT id FROM rss_feed WHERE url = ?
    ''', (url,))
    
    result = cursor.fetchone()
    
    if result:
        # If the URL exists, update the entry
        entry_id = result[0]  # Get the id of the existing entry
        cursor.execute('''
            UPDATE rss_feed
            SET title = ?, author = ?, description = ?, published_date = ?, tags = ?
            WHERE id = ?
        ''', (title, author, url, description, published_date, tags))
        conn.commit()
        print("Entry updated.")
    else:
        print("No entry found with the given URL.")
    
    conn.close()

# Function to check if a URL already exists in the database
def url_exists(db_name, url):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM rss_feed WHERE url = ?', (url,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def truncate_text(text, max_length=250):
    # Split the text into sentences using regex to match punctuation
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    # Initialize an empty list to hold the selected sentences
    selected_sentences = []
    current_length = 0
    
    # Iterate through the sentences in reverse order
    for sentence in sentences:
        # Check if adding this sentence would exceed the max length
        if current_length + len(sentence) <= max_length:
            selected_sentences.append(sentence)
            current_length += len(sentence)
        else:
            break  # Stop if we exceed the max length
    
    # Reverse the selected sentences to maintain original order and join them
    return ' '.join(reversed(selected_sentences)).strip()


# Function to check if any keywords are in the description and return matching tags
def extract_tags(title, description, keywords):
    found_tags = [keyword for keyword in keywords if keyword.lower() in title.lower() or keyword.lower() in description.lower()]
    return ', '.join(found_tags) if found_tags else None

# Read RSS feed URLs from a text file
with open('rss_feeds.txt', 'r') as file:
    rss_urls = file.readlines()

# Strip whitespace characters like `\n` at the end of each line
rss_urls = [url.strip() for url in rss_urls]

# Specify the base URL you want to check against
with open('special_urls.txt', 'r') as file:
    base_url = [line.strip() for line in file.readlines()]

# Read RSS feed keywords from a text file
with open('tags.txt', 'r') as file:
    keywords = [line.strip() for line in file.readlines()]

# Create the database and table
create_database(db_name)

# Loop through each URL and parse the feed
for rss_url in rss_urls:
    feed = feedparser.parse(rss_url)

    # Access entry attributes
    for entry in feed.entries:
        # Get the author and published date, with defaults if not present
        author = entry.get('author', 'Unknown Author')
        
        # Modify published date
        date_string = entry.get('published', None )

        if date_string:
            date_without_timezone = date_string.rsplit(' ', 1)[0]
            parsed_date = datetime.strptime(date_without_timezone, "%a, %d %b %Y %H:%M:%S")
            published_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            published_date = 'No Date Provided'


        # Check if the entry link starts with the specific base URL
        if entry.link.startswith(tuple(base_url)):
            # Parse the entry description with BeautifulSoup
            soup = BeautifulSoup(entry.description, 'html.parser')

            # Find the first <p> tag
            first_paragraph = soup.find('p')

            # Use the first paragraph as the description if found, otherwise use the full description
            raw_description = first_paragraph.get_text() if first_paragraph else entry.description
        else:
            # Clean the full description if the base URL does not match
            soup = BeautifulSoup(entry.description, 'html.parser')
            raw_description = soup.get_text(strip=True)

        description = truncate_text(raw_description)

        title = entry.title

        # Extract tags based on keywords
        tags = extract_tags(title, description, keywords)

        if tags:
            # Check if the URL already exists in the database
            if url_exists(db_name, entry.link):
                # Insert the feed entry into the database
                update_feed_entry(db_name, title, author, entry.link, description, published_date, tags)  # Assuming 'send' is 0 for new entries
                print(f"Update entry in the database: {entry.title} {tags}")
            if not url_exists(db_name, entry.link):
                # Insert the feed entry into the database
                insert_feed_entry(db_name, title, author, entry.link, description, published_date, tags, 0)  # Assuming 'send' is 0 for new entries
                print(f"New entry in the database: {entry.title} {tags}")
