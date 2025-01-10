import sqlite3

# Database
db_name = 'rss_feeds.db'

# Function to retrieve and print all RSS feed entries from the database
def print_rss_feeds(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT title, author, url, description, published_date, tags, send FROM rss_feed')
    feeds = cursor.fetchall()
    
    for feed in feeds:
        title, author, url, description, published_date, tags, send = feed
        print(f"Title: {title}")
        print(f"Author: {author}")
        print(f"URL: {url}")
        print(f"Description: {description}")
        print(f"Published Date: {published_date}")
        print(f"Tags: {tags}")
        print("Send:", "yes" if send == 1 else "no")
        print("-" * 40)  # Separator for readability

    conn.close()

# Print the RSS feeds from the database
print_rss_feeds(db_name)

