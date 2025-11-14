"""
Kugou API Client
Handles communication with Kugou music service API with proper encryption and signature
"""
import requests
import hashlib
import base64
import json
import time
import uuid as uuid_lib
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from typing import Optional, Dict, Any


class KugouClient:
    """Client for interacting with Kugou music API with proper authentication"""
    
    def __init__(self, userid: str = None, token: str = None, dfid: str = None, mid: str = None, uuid: str = None):
        self.userid = userid
        self.token = token
        self.dfid = dfid or self._generate_dfid()
        self.mid = mid or self._generate_mid()
        self.uuid = uuid or self._generate_uuid()
        
        # Known Kugou endpoints
        self.mobile_url = "http://mobilecdnbj.kugou.com"
        self.web_url = "http://www.kugou.com"
        self.gateway_url = "http://gateway.kugou.com"
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'KuGou2012-8275-web_browser_event_handler',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
    
    def _generate_dfid(self) -> str:
        """Generate device fingerprint ID"""
        return hashlib.md5(str(uuid_lib.uuid4()).encode()).hexdigest().upper()[:16]
    
    def _generate_mid(self) -> str:
        """Generate machine ID"""
        return hashlib.md5(str(uuid_lib.uuid4()).encode()).hexdigest().upper()
    
    def _generate_uuid(self) -> str:
        """Generate UUID"""
        return str(uuid_lib.uuid4()).upper()
    
    def _generate_signature(self, params: dict) -> str:
        """
        Generate MD5 signature for API requests
        This is reverse-engineered from KugouMusicApi
        """
        # Remove signature from params if present
        if 'signature' in params:
            del params['signature']
        
        # Sort parameters alphabetically by key
        sorted_params = sorted(params.items())
        
        # Create parameter string
        param_string = ''.join([f"{k}={v}" for k, v in sorted_params])
        
        # Add Kugou secret key (reverse-engineered)
        secret_key = "NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt"
        sign_string = param_string + secret_key
        
        # Generate MD5 signature
        return hashlib.md5(sign_string.encode()).hexdigest().upper()
    
    def _get_common_params(self) -> dict:
        """Get common parameters needed for most API calls"""
        return {
            'clienttime': int(time.time() * 1000),
            'mid': self.mid,
            'dfid': self.dfid,
            'clientver': '20000',
            'platid': '4',
            'userid': self.userid or '0',
            'token': self.token or '',
            'uuid': self.uuid
        }
    
    def get_user_listening_history(self) -> Optional[Dict[str, Any]]:
        """
        Attempt to get listening history
        NOTE: This endpoint may not exist - using best guess based on patterns
        """
        if not self.userid or not self.token:
            return None
            
        try:
            # Try multiple possible endpoints
            endpoints_to_try = [
                "/api/v3/user/listen",
                "/api/v5/user/listen", 
                "/api/v3/user/recent",
                "/api/v5/user/recent"
            ]
            
            for endpoint in endpoints_to_try:
                try:
                    params = self._get_common_params()
                    params.update({
                        'page': 1,
                        'pagesize': 1
                    })
                    
                    # Generate signature
                    params['signature'] = self._generate_signature(params.copy())
                    
                    response = self.session.get(f"{self.mobile_url}{endpoint}", params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("status") == 1 and data.get("data"):
                            return data["data"][0] if isinstance(data["data"], list) else data["data"]
                    
                except Exception as e:
                    print(f"Failed endpoint {endpoint}: {e}")
                    continue
                    
            return None
            
        except Exception as e:
            print(f"Error fetching listening history: {e}")
            return None
    
    def get_song_details(self, hash_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed song info by hash ID"""
        try:
            params = {
                'r': 'play/getdata',
                'hash': hash_id,
                'platid': 4,
                'album_id': '0'
            }
            
            response = self.session.get(f"{self.web_url}/yy/index.php", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == 1:
                    return data.get("data")
            
            return None
            
        except Exception as e:
            print(f"Error fetching song details: {e}")
            return None
    
    def search_songs(self, keyword: str, page: int = 1) -> Optional[Dict[str, Any]]:
        """Search for songs"""
        try:
            params = self._get_common_params()
            params.update({
                'keyword': keyword,
                'page': page,
                'pagesize': 20,
                'bitrate': 0,
                'isfuzzy': 0,
                'tag': 'em',
                'inputtype': 0,
                'platform': 'WebFilter'
            })
            
            # Generate signature
            params['signature'] = self._generate_signature(params.copy())
            
            response = self.session.get(f"{self.mobile_url}/api/v3/search/song", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == 1:
                    return data.get("data")
            
            return None
            
        except Exception as e:
            print(f"Error searching songs: {e}")
            return None
    
    def get_now_playing_fallback(self, user_id: str = None) -> Optional[Dict[str, Any]]:
        """
        Fallback method - returns demo data
        In a real implementation, this could try alternative methods
        """
        return {
            "song_name": "青花瓷 (Demo)",
            "author_name": "周杰伦",
            "album_name": "我很忙",
            "img": "https://imge.kugou.com/stdmusic/240/20160818/20160818112845056710.jpg",
            "hash": "demo_hash"
        }
    
    def test_connection(self) -> bool:
        """Test if we can connect to Kugou API"""
        try:
            # Try a simple search to test connection
            result = self.search_songs("test")
            return result is not None
        except:
            return False
