import tweepy
import requests
import random
import os

# Twitter API credentials
API_KEY = "your_api_key"
API_SECRET_KEY = "your_api_secret_key"
ACCESS_TOKEN = "your_access_token"
ACCESS_TOKEN_SECRET = "your_access_token_secret"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Function to get random track information from Spotify API
def get_random_track():
    # Replace with your Spotify API credentials
    client_id = "your_spotify_client_id"
    client_secret = "your_spotify_client_secret"
    access_token_url = "https://accounts.spotify.com/api/token"
    api_url = "https://api.spotify.com/v1/playlists/PLAYLIST_ID/tracks"

    # Replace "PLAYLIST_ID" with the ID of the playlist that contains the songs you want to use
    playlist_id = "your_spotify_playlist_id"

    # Request an access token from Spotify API
    response = requests.post(
        access_token_url,
        {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    access_token = response.json().get("access_token")

    if access_token:
        # Fetch the playlist tracks using the access token
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"fields": "items(track(name,artists(name)))", "limit": 100}
        response = requests.get(api_url.replace("PLAYLIST_ID", playlist_id), headers=headers, params=params)

        if response.status_code == 200:
            tracks = response.json().get("items")
            if tracks:
                return random.choice(tracks)["track"]
    return None

# Function to get song lyrics from Genius API
def get_song_lyrics(track_name, artist_name):
    # Replace with your Genius API token
    genius_api_token = "your_genius_api_token"
    genius_api_url = "https://api.genius.com/search"

    # Search for the track on Genius API
    headers = {"Authorization": f"Bearer {genius_api_token}"}
    params = {"q": f"{track_name} {artist_name}"}
    response = requests.get(genius_api_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        hits = data.get("response", {}).get("hits", [])
        for hit in hits:
            result = hit.get("result", {})
            if result.get("title").lower() == track_name.lower():
                return result.get("url")

    return None

# Function to post a tweet with the song lyrics
def tweet_lyrics():
    track = get_random_track()
    if track:
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]

        # Get the song lyrics from Genius API
        lyrics_url = get_song_lyrics(track_name, artist_name)

        if lyrics_url:
            # Compose the tweet
            tweet = f"🎵 {track_name} - {artist_name}\n\nLyrics: {lyrics_url}"

            # Post the tweet
            api.update_status(status=tweet)

if __name__ == "__main__":
    tweet_lyrics()
