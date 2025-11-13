"""
Main API endpoint for Kugou widget
Vercel serverless function handler
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Optional
import os

from kugou_client import KugouClient
from svg_generator import SVGGenerator


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            # Parse query parameters
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Get user_id from query parameters
            user_id = query_params.get('user_id', [None])[0]
            
            if not user_id:
                self._send_error_response("Missing user_id parameter")
                return
            
            # Get optional parameters
            width = int(query_params.get('width', [400])[0])
            height = int(query_params.get('height', [120])[0])
            
            # Initialize clients
            kugou_client = KugouClient()
            svg_generator = SVGGenerator(width=width, height=height)
            
            # Fetch now playing data
            now_playing = kugou_client.get_now_playing(user_id)
            
            if now_playing:
                # Extract track information
                track_name = now_playing.get('track_name')
                artist_name = now_playing.get('artist_name')
                album_name = now_playing.get('album_name')
                is_playing = now_playing.get('is_playing', False)
                
                # Generate SVG
                svg_content = svg_generator.generate_now_playing_widget(
                    track_name=track_name,
                    artist_name=artist_name,
                    album_name=album_name,
                    is_playing=is_playing
                )
            else:
                # Show not playing state
                svg_content = svg_generator.generate_now_playing_widget()
            
            # Send response
            self._send_svg_response(svg_content)
            
        except Exception as e:
            print(f"Error handling request: {e}")
            svg_generator = SVGGenerator()
            svg_content = svg_generator.generate_error_widget(f"Error: {str(e)}")
            self._send_svg_response(svg_content)
    
    def _send_svg_response(self, svg_content: str):
        """Send SVG response"""
        self.send_response(200)
        self.send_header('Content-Type', 'image/svg+xml')
        self.send_header('Cache-Control', 'public, max-age=60')
        self.end_headers()
        self.wfile.write(svg_content.encode('utf-8'))
    
    def _send_error_response(self, error_message: str):
        """Send error response"""
        svg_generator = SVGGenerator()
        svg_content = svg_generator.generate_error_widget(error_message)
        self._send_svg_response(svg_content)
