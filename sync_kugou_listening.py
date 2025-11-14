#!/usr/bin/env python3
"""
Sync Kugou Listening History to Firebase Cache

This script periodically fetches your latest listening history from KuGouMusicApi
and updates the Firebase cache. Run it on a schedule (e.g., every 5 minutes) to
keep your GitHub widget always up-to-date.

Usage:
    export WIDGET_URL="https://your-widget-url.vercel.app"
    export USER_ID="your_github_username"
    ./sync_kugou_listening.py

Cron Example (every 5 minutes):
    */5 * * * * cd /path/to/kugou-widget && WIDGET_URL="..." USER_ID="..." ./sync_kugou_listening.py >> /tmp/kugou-sync.log 2>&1
"""

import requests
import os
import sys
from datetime import datetime

# Configuration from environment variables
WIDGET_URL = os.getenv('WIDGET_URL', 'https://kugou-widget.vercel.app')
USER_ID = os.getenv('USER_ID', 'your_github_username')

# Optional: Slack/Discord webhook for notifications
WEBHOOK_URL = os.getenv('NOTIFICATION_WEBHOOK', '')

def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def send_notification(message):
    """Send notification to webhook (if configured)"""
    if not WEBHOOK_URL:
        return
    
    try:
        payload = {"text": message}
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        log(f"Failed to send notification: {e}")

def sync_listening_history():
    """
    Trigger widget to fetch from KuGouMusicApi and update cache
    Returns: (success: bool, song_info: dict or None)
    """
    try:
        log(f"Syncing listening history for user: {USER_ID}")
        
        # Access the now-playing endpoint to trigger sync
        url = f"{WIDGET_URL}/now-playing?user_id={USER_ID}"
        
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            # Try to extract song info from SVG response
            svg_content = response.text
            
            # Simple parsing (SVG contains song info in text elements)
            song_name = None
            artist_name = None
            
            # Look for song name in SVG
            if 'Now Playing:' in svg_content:
                lines = svg_content.split('\n')
                for i, line in enumerate(lines):
                    if 'Now Playing:' in line and i + 1 < len(lines):
                        # Next line usually has the song name
                        if '<text' in lines[i+1]:
                            # Extract text between > and <
                            text = lines[i+1].split('>')[1].split('<')[0] if '>' in lines[i+1] else None
                            if text and text.strip():
                                song_name = text.strip()
                    if song_name and 'by' in line:
                        # Extract artist
                        text = line.split('>')[1].split('<')[0] if '>' in line else None
                        if text and text.strip():
                            artist_name = text.strip().replace('by ', '')
                        break
            
            if song_name:
                log(f"✓ Synced successfully: {song_name}" + (f" - {artist_name}" if artist_name else ""))
                return True, {'song': song_name, 'artist': artist_name}
            else:
                log(f"✓ Sync completed (HTTP 200)")
                return True, None
        
        else:
            log(f"✗ Sync failed: HTTP {response.status_code}")
            log(f"Response: {response.text[:200]}")
            return False, None
            
    except requests.Timeout:
        log(f"✗ Sync timeout: No response from {WIDGET_URL}")
        return False, None
    except requests.RequestException as e:
        log(f"✗ Request error: {e}")
        return False, None
    except Exception as e:
        log(f"✗ Unexpected error: {e}")
        return False, None

def check_kugou_api_status():
    """Check if KuGou API credentials are configured"""
    try:
        url = f"{WIDGET_URL}/test?user_id={USER_ID}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            kugou_status = data.get('kugou_api', 'Unknown')
            
            if 'Configured' in str(kugou_status):
                log("✓ KuGou API credentials: Configured")
                return True
            else:
                log(f"⚠ KuGou API credentials: {kugou_status}")
                log("Run: curl -X POST {}/setup-kugou to configure".format(WIDGET_URL))
                return False
        else:
            log(f"⚠ Cannot check API status: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        log(f"⚠ Error checking API status: {e}")
        return False

def main():
    """Main sync routine"""
    log("=" * 60)
    log("Kugou Listening History Sync")
    log("=" * 60)
    log(f"Widget URL: {WIDGET_URL}")
    log(f"User ID: {USER_ID}")
    log("")
    
    # Validate configuration
    if USER_ID == 'your_github_username':
        log("✗ Error: Please set USER_ID environment variable")
        log("Example: export USER_ID='your_github_username'")
        return 1
    
    # Check API configuration
    check_kugou_api_status()
    
    # Perform sync
    log("")
    success, song_info = sync_listening_history()
    
    # Send notification on failure
    if not success:
        send_notification(f"⚠️ Kugou widget sync failed for {USER_ID}")
    elif song_info and song_info.get('song'):
        # Optional: notify on song change
        send_notification(f"🎵 Now playing: {song_info['song']} - {song_info.get('artist', 'Unknown')}")
    
    log("=" * 60)
    log("")
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
