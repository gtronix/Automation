from mastodon import Mastodon

# Post a status update
status = "Hello, Mastodon! This is my first post from a Python script."

mastodon = Mastodon(access_token = '.secret/pytooter_usercred.secret')
mastodon.toot(status)

