"""
Main API endpoint for Kugou widget
Flask serverless function for Vercel
"""
from flask import Flask, Response, request, jsonify
import os
import json
import traceback
import time
import hashlib
import sys

# Add the current directory to path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import Firebase conditionally to prevent crashes
firebase_initialized = False
firebase_admin = None
try:
    import firebase_admin
    from firebase_admin import credentials, db
except ImportError as e:
    print(f"Firebase Admin SDK not available: {e}")

# Import local modules
print("Loading Kugou client and SVG generator...")
try:
    from kugou_client import KugouClient
    from svg_generator import generate_music_svg, generate_default_svg, generate_error_svg
    print("Successfully imported local modules")
except Exception as e:
    print(f"ERROR importing local modules: {e}")
    print(f"Current directory: {os.path.dirname(os.path.abspath(__file__))}")
    print(f"sys.path: {sys.path}")
    raise

print("Creating Flask app...")
app = Flask(__name__)
print(f"Flask app created successfully")

# Demo song data for immediate testing
DEMO_SONGS = [
    {
        'name': '告白气球',
        'artist': '周杰伦',
        'cover': 'https://imge.kugou.com/stdmusic/240/20170418/20170418173403349763.jpg'
    },
    {
        'name': '青花瓷',
        'artist': '周杰伦', 
        'cover': 'https://imge.kugou.com/stdmusic/240/20160818/20160818112845056710.jpg'
    },
    {
        'name': '稻香',
        'artist': '周杰伦',
        'cover': 'https://imge.kugou.com/stdmusic/240/20150719/20150719205742894772.jpg'
    }
]

# Current song index (cycles through demo songs)
current_song_index = 0

# Initialize Firebase (only if credentials are available and firebase_admin is imported)
if firebase_admin and os.getenv("FIREBASE_CREDENTIALS"):
    try:
        firebase_creds = json.loads(os.getenv("FIREBASE_CREDENTIALS"))
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred, {
            'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
        })
        firebase_initialized = True
        print("Firebase initialized successfully")
    except Exception as e:
        print(f"Firebase initialization failed: {e}")
        firebase_initialized = False
else:
    print("Firebase not available or credentials not set - using demo mode only")


def get_song_from_kugou_api(user_id):
    """
    Fetch currently playing song from Node.js KuGouMusicApi
    This provides real-time sync with actual Kugou listening history
    """
    try:
        if not firebase_initialized:
            return None
            
        # Get user's Kugou credentials from Firebase
        ref = db.reference(f'users/{user_id}/kugou_credentials')
        creds = ref.get()
        
        if not creds:
            print(f"No Kugou API credentials found for {user_id}")
            return None
        
        kugou_api_url = creds.get('api_url')
        userid = creds.get('userid')
        token = creds.get('token')
        
        if not kugou_api_url or not userid or not token:
            print("Incomplete Kugou API credentials")
            return None
        
        # Call Node.js KuGouMusicApi for listening history
        print(f"Fetching from KuGouMusicApi: {kugou_api_url}")
        
        import requests
        response = requests.get(
            f"{kugou_api_url}/user/recentListening",
            params={
                'userid': userid,
                'token': token,
                'limit': 1
            },
            timeout=10
        )
        
        data = response.json()
        print(f"KuGouMusicApi response status: {data.get('status')}")
        
        # Check if we got song data
        if data.get('status') == 1 and data.get('data') and len(data['data']) > 0:
            song = data['data'][0]
            
            result = {
                'name': song.get('songname', 'Unknown'),
                'artist': song.get('singername', 'Unknown'),
                'cover': song.get('img', ''),
                'hash': song.get('hash'),
                'source': 'kugou_api_realtime'
            }
            
            print(f"✅ Got real-time song from Kugou: {result['name']} - {result['artist']}")
            
            # Update Firebase cache with latest song
            try:
                song_ref = db.reference(f'users/{user_id}/current_song')
                song_ref.set({
                    'name': result['name'],
                    'artist': result['artist'],
                    'cover': result['cover'],
                    'updated_at': int(time.time()),
                    'source': 'kugou_api'
                })
                print(f"Updated Firebase cache for {user_id}")
            except Exception as cache_error:
                print(f"Cache update failed: {cache_error}")
            
            return result
        else:
            print(f"No songs in KuGouMusicApi response")
            return None
    
    except Exception as e:
        print(f"Error fetching from KuGouMusicApi: {e}")
        print(traceback.format_exc())
        return None


@app.route('/')
def now_playing():
    """Main endpoint that returns SVG widget - now with KuGouMusicApi integration!"""
    try:
        # Get query parameters
        user_id = request.args.get('user_id')
        theme = request.args.get('theme', 'light')
        width = int(request.args.get('width', 400))
        height = int(request.args.get('height', 120))
        show_album = request.args.get('show_album', 'true').lower() != 'false'
        
        song_data = None
        
        # PRIORITY 1: Try KuGouMusicApi for real-time data (non-demo users only)
        if user_id and user_id != 'demo':
            song_data = get_song_from_kugou_api(user_id)
            if song_data:
                print(f"✅ Using real-time KuGouMusicApi data")
        
        # PRIORITY 2: Try to get cached song from Firebase
        if not song_data and firebase_initialized and user_id:
            try:
                ref = db.reference(f'users/{user_id}/current_song')
                song_data = ref.get()
                if song_data:
                    print(f"Using cached Firebase data for {user_id}")
            except Exception as e:
                print(f"Firebase lookup failed: {e}")
        
        # PRIORITY 3: Demo mode or fallback
        if not song_data:
            if user_id == 'demo' or not user_id:
                # Demo mode - cycle through demo songs
                global current_song_index
                song_data = DEMO_SONGS[current_song_index % len(DEMO_SONGS)]
                current_song_index = (current_song_index + 1) % len(DEMO_SONGS)
                print("Using demo song data")
            else:
                # Try old KugouClient method (fallback)
                if firebase_initialized:
                    try:
                        ref = db.reference(f'users/{user_id}')
                        user_data = ref.get()
                        if user_data and user_data.get('userid') and user_data.get('token'):
                            print("Trying legacy KugouClient...")
                            client = KugouClient(
                                userid=user_data.get('userid'),
                                token=user_data.get('token'),
                                dfid=user_data.get('dfid'),
                                mid=user_data.get('mid'),
                                uuid=user_data.get('uuid')
                            )
                            song_data = client.get_user_listening_history()
                    except Exception as e:
                        print(f"Legacy Kugou API call failed: {e}")
                
                # Final fallback to demo
                if not song_data:
                    song_data = DEMO_SONGS[0]
                    print("Using fallback demo song")
        
        # Generate SVG with song data
        if song_data:
            svg = generate_music_svg(
                song_name=song_data.get('name', song_data.get('song_name', 'Unknown')),
                artist_name=song_data.get('artist', song_data.get('author_name', 'Unknown')),
                album_cover_url=song_data.get('cover', song_data.get('img', '')),
                theme=theme,
                width=width,
                height=height,
                show_album=show_album
            )
        else:
            svg = generate_default_svg(theme, width, height)
        
        return Response(svg, mimetype='image/svg+xml', headers={
            'Cache-Control': 'public, max-age=60',
            'Access-Control-Allow-Origin': '*'
        })
        
    except Exception as e:
        print(f"Error in now_playing: {e}")
        print(traceback.format_exc())
        
        # Get dimensions for error SVG
        try:
            width = int(request.args.get('width', 400))
            height = int(request.args.get('height', 120))
            theme = request.args.get('theme', 'light')
        except:
            width, height, theme = 400, 120, 'light'
        
        svg = generate_error_svg("Service temporarily unavailable", theme, width, height)
        return Response(svg, mimetype='image/svg+xml', headers={
            'Cache-Control': 'public, max-age=30',
            'Access-Control-Allow-Origin': '*'
        })


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "firebase_connected": firebase_initialized,
        "version": "1.0.0"
    })


@app.route('/update', methods=['POST'])
def update_now_playing():
    """Manually update current song"""
    try:
        if not firebase_initialized:
            return jsonify({"error": "Firebase not configured"}), 500
        
        data = request.get_json()
        user_id = data.get('user_id')
        song_name = data.get('song_name')
        artist_name = data.get('artist_name')
        cover_url = data.get('cover_url', '')
        
        if not all([user_id, song_name, artist_name]):
            return jsonify({"error": "Missing required fields: user_id, song_name, artist_name"}), 400
        
        # Update current song in Firebase
        ref = db.reference(f'users/{user_id}/current_song')
        ref.set({
            'name': song_name,
            'artist': artist_name,
            'cover': cover_url,
            'updated_at': int(time.time())
        })
        
        return jsonify({
            "success": True,
            "message": f"Updated current song for {user_id}",
            "widget_url": f"{request.host_url}?user_id={user_id}"
        })
        
    except Exception as e:
        print(f"Error in update: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/setup-kugou', methods=['POST'])
def setup_kugou():
    """
    Setup Kugou API credentials for real-time sync
    POST body:
    {
        "user_id": "your_github_username",
        "api_url": "https://your-kugou-api.vercel.app",
        "userid": "123456",
        "token": "abc123..."
    }
    """
    try:
        if not firebase_initialized:
            return jsonify({"error": "Firebase not configured"}), 500
        
        data = request.get_json()
        user_id = data.get('user_id')
        api_url = data.get('api_url')
        userid = data.get('userid')
        token = data.get('token')
        
        if not all([user_id, api_url, userid, token]):
            return jsonify({
                "error": "Missing required fields",
                "required": ["user_id", "api_url", "userid", "token"]
            }), 400
        
        # Save credentials to Firebase
        creds = {
            'api_url': api_url,
            'userid': userid,
            'token': token,
            'setup_at': int(time.time())
        }
        
        ref = db.reference(f'users/{user_id}/kugou_credentials')
        ref.set(creds)
        
        return jsonify({
            "success": True,
            "message": "Kugou API credentials saved successfully!",
            "user_id": user_id,
            "widget_url": f"{request.host_url}?user_id={user_id}&theme=dark",
            "next_steps": [
                "Your widget will now show real-time listening history from Kugou",
                "Add to your GitHub README to see it in action",
                "Songs update automatically when you play on Kugou"
            ]
        })
        
    except Exception as e:
        print(f"Error in setup_kugou: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/login')
def login_guide():
    """Login guidance endpoint"""
    return jsonify({
        "message": "Kugou widget setup options",
        "options": {
            "demo": {
                "description": "Use demo data (works immediately)",
                "url": f"{request.host_url}?user_id=demo&theme=dark",
                "instructions": "Just use user_id=demo in your URL"
            },
            "manual_update": {
                "description": "Manual song updates via API",
                "url": f"{request.host_url}/update",
                "method": "POST",
                "body": {
                    "user_id": "your_id",
                    "song_name": "Song Name", 
                    "artist_name": "Artist Name",
                    "cover_url": "https://image.url"
                }
            },
            "full_api": {
                "description": "Extract Kugou credentials (advanced)",
                "instructions": [
                    "1. Extract userid, token, dfid, mid, uuid from Kugou app",
                    "2. Store in Firebase: users/{user_id}/",
                    "3. Widget will auto-fetch from Kugou API"
                ]
            }
        }
    })


@app.route('/refresh_tokens', methods=['POST'])
def refresh_tokens():
    """Refresh expired Kugou tokens"""
    try:
        if not firebase_initialized:
            return jsonify({"error": "Firebase not configured"}), 500
        
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400
        
        # Get existing user data
        ref = db.reference(f'users/{user_id}')
        user_data = ref.get()
        
        if not user_data:
            return jsonify({"error": "User not found"}), 404
        
        # Check if token needs refresh
        expires_at = user_data.get('expires_at', 0)
        current_time = int(time.time() * 1000)
        
        if current_time < expires_at:
            return jsonify({
                "message": "Token still valid",
                "expires_at": expires_at,
                "current_time": current_time
            })
        
        # Attempt token refresh (this would need actual Kugou refresh endpoint)
        client = KugouClient(
            userid=user_data.get('userid'),
            token=user_data.get('token'),
            dfid=user_data.get('dfid'),
            mid=user_data.get('mid'),
            uuid=user_data.get('uuid')
        )
        
        # In a real implementation, call actual refresh API
        # For now, just extend the expiration
        new_expires_at = current_time + (7 * 24 * 60 * 60 * 1000)  # 7 days
        
        ref.update({
            'expires_at': new_expires_at,
            'last_refresh': current_time
        })
        
        return jsonify({
            "success": True,
            "message": "Token refresh attempted",
            "expires_at": new_expires_at
        })
        
    except Exception as e:
        print(f"Error in refresh_tokens: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/user/<user_id>', methods=['GET'])
def get_user_info(user_id):
    """Get user configuration and current song info"""
    try:
        if not firebase_initialized:
            return jsonify({
                "user_id": user_id,
                "mode": "demo" if user_id == "demo" else "no_firebase",
                "firebase_connected": False
            })
        
        ref = db.reference(f'users/{user_id}')
        user_data = ref.get()
        
        if not user_data:
            return jsonify({
                "user_id": user_id,
                "mode": "not_configured",
                "message": "User not found in database"
            })
        
        # Check token expiration
        expires_at = user_data.get('expires_at', 0)
        current_time = int(time.time() * 1000)
        is_expired = current_time >= expires_at
        
        # Get current song
        current_song = None
        song_ref = db.reference(f'users/{user_id}/current_song')
        current_song = song_ref.get()
        
        response = {
            "user_id": user_id,
            "mode": "configured",
            "has_credentials": bool(user_data.get('userid') and user_data.get('token')),
            "token_expired": is_expired,
            "expires_at": expires_at,
            "current_time": current_time,
            "current_song": current_song,
            "last_updated": current_song.get('updated_at') if current_song else None
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in get_user_info: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/test')
def test_widget():
    """Test endpoint with sample data"""
    theme = request.args.get('theme', 'light')
    width = int(request.args.get('width', 400))
    height = int(request.args.get('height', 120))
    
    svg = generate_music_svg(
        song_name="Test Song - 测试歌曲",
        artist_name="Test Artist - 测试歌手",
        album_cover_url="https://via.placeholder.com/300x300/1ED760/ffffff?text=♪",
        theme=theme,
        width=width,
        height=height
    )
    
    return Response(svg, mimetype='image/svg+xml', headers={
        'Cache-Control': 'no-cache',
        'Access-Control-Allow-Origin': '*'
    })


# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)
