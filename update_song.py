#!/usr/bin/env python3
"""
Quick script to update your now playing song on Kugou Widget
Usage: python update_song.py "Song Name" "Artist Name" [album_cover_url]
"""
import requests
import sys
import json

# YOUR CONFIG - EDIT THESE VALUES
VERCEL_URL = "https://kugou-widget-miuc8u8lw-cv4tkg1uav-gmailcoms-projects.vercel.app"
USER_ID = "YOUR_GITHUB_USERNAME"  # Change this to your GitHub username

def update_song(song_name, artist_name, cover_url=None):
    """Update the song on your widget"""
    
    if not cover_url:
        # Default Kugou album art
        cover_url = "https://imge.kugou.com/stdmusic/240/default.jpg"
    
    payload = {
        "user_id": USER_ID,
        "song_name": song_name,
        "artist_name": artist_name,
        "cover_url": cover_url
    }
    
    print(f"📤 Updating song to: {song_name} - {artist_name}")
    print(f"🔗 Using URL: {VERCEL_URL}/update")
    
    try:
        response = requests.post(
            f"{VERCEL_URL}/update",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! {result.get('message', 'Updated successfully')}")
            print(f"🎵 Widget URL: {result.get('widget_url', f'{VERCEL_URL}?user_id={USER_ID}')}")
            print(f"📸 View on GitHub: https://github.com/{USER_ID}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Check your internet connection.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def show_usage():
    """Show usage examples"""
    print("""
🎵 Kugou Widget Song Updater

Usage:
    python update_song.py "Song Name" "Artist Name" [album_cover_url]

Examples:
    # Update with song and artist only
    python update_song.py "晴天" "周杰伦"
    
    # Update with custom album art
    python update_song.py "告白气球" "周杰伦" "https://imge.kugou.com/stdmusic/240/20170418/20170418173403349763.jpg"
    
    # English songs work too
    python update_song.py "Shape of You" "Ed Sheeran"

Popular Jay Chou Songs:
    python update_song.py "晴天" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150718/20150718120613556308.jpg"
    python update_song.py "告白气球" "周杰伦" "https://imge.kugou.com/stdmusic/240/20170418/20170418173403349763.jpg"
    python update_song.py "青花瓷" "周杰伦" "https://imge.kugou.com/stdmusic/240/20161118/20161118102139558324.jpg"
    python update_song.py "稻香" "周杰伦" "https://imge.kugou.com/stdmusic/240/20150719/20150719205742894772.jpg"

⚠️  Remember to:
    1. Edit VERCEL_URL and USER_ID at the top of this file
    2. Setup Firebase with your user_id
    3. Install requests: pip install requests
""")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        show_usage()
        sys.exit(1)
    
    # Check if user hasn't configured the script
    if USER_ID == "YOUR_GITHUB_USERNAME":
        print("⚠️  Warning: You haven't configured your USER_ID yet!")
        print("Edit this file and change USER_ID to your GitHub username.\n")
    
    song = sys.argv[1]
    artist = sys.argv[2]
    cover = sys.argv[3] if len(sys.argv) > 3 else None
    
    update_song(song, artist, cover)
