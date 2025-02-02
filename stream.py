import requests
from bs4 import BeautifulSoup
import vlc
import time
import yt_dlp

def get_youtube_url():
    # Get the webpage content
    response = requests.get("https://www.hojoanaheim.com/webcam/")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the YouTube video ID from the iframe
    iframe = soup.find('iframe')
    if iframe and 'src' in iframe.attrs:
        video_url = iframe['src']
        # Extract direct stream URL using yt-dlp
        ydl_opts = {
            'format': 'best',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return info['url']
    return None

def play_stream(url):
    # Create a VLC instance
    instance = vlc.Instance('--fullscreen')
    player = instance.media_player_new()
    
    # Create and set media
    media = instance.media_new(url)
    player.set_media(media)
    
    # Set fullscreen and play
    player.set_fullscreen(True)
    player.play()
    
    # Keep the stream running
    while True:
        time.sleep(1)

def main():
    try:
        youtube_url = get_youtube_url()
        if youtube_url:
            print(f"Found stream URL: {youtube_url}")
            play_stream(youtube_url)
        else:
            print("Could not find YouTube stream URL")
    except KeyboardInterrupt:
        print("\nStopping stream...")

if __name__ == "__main__":
    main()
