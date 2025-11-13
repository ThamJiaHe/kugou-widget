"""
SVG Generator
Generates SVG widgets for displaying now playing information
"""
from typing import Optional, Dict, Any
import html


class SVGGenerator:
    """Generator for creating SVG widgets"""
    
    def __init__(self, width: int = 400, height: int = 120):
        self.width = width
        self.height = height
    
    def generate_now_playing_widget(
        self,
        track_name: Optional[str] = None,
        artist_name: Optional[str] = None,
        album_name: Optional[str] = None,
        is_playing: bool = False
    ) -> str:
        """
        Generate SVG widget for now playing information
        
        Args:
            track_name: Name of the track
            artist_name: Name of the artist
            album_name: Name of the album
            is_playing: Whether music is currently playing
            
        Returns:
            SVG string
        """
        # Escape HTML to prevent XSS
        track_name = html.escape(track_name or "Not Playing")
        artist_name = html.escape(artist_name or "Unknown Artist")
        album_name = html.escape(album_name or "Unknown Album")
        
        status_color = "#1DB954" if is_playing else "#535353"
        status_text = "Now Playing" if is_playing else "Last Played"
        
        svg = f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .header {{ fill: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif; font-size: 14px; font-weight: 600; }}
    .track {{ fill: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif; font-size: 20px; font-weight: 700; }}
    .info {{ fill: #b3b3b3; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif; font-size: 14px; }}
    .status {{ fill: {status_color}; }}
  </style>
  
  <rect width="{self.width}" height="{self.height}" fill="#181818" rx="8"/>
  
  <!-- Status indicator -->
  <circle cx="20" cy="20" r="5" class="status"/>
  <text x="30" y="24" class="header">{status_text}</text>
  
  <!-- Track name -->
  <text x="20" y="55" class="track">{track_name}</text>
  
  <!-- Artist and Album -->
  <text x="20" y="80" class="info">{artist_name}</text>
  <text x="20" y="100" class="info">{album_name}</text>
</svg>'''
        
        return svg
    
    def generate_error_widget(self, error_message: str = "Error loading widget") -> str:
        """
        Generate SVG widget for error state
        
        Args:
            error_message: Error message to display
            
        Returns:
            SVG string
        """
        error_message = html.escape(error_message)
        
        svg = f'''<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .error {{ fill: #ffffff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif; font-size: 16px; }}
  </style>
  
  <rect width="{self.width}" height="{self.height}" fill="#181818" rx="8"/>
  <text x="{self.width // 2}" y="{self.height // 2}" class="error" text-anchor="middle">{error_message}</text>
</svg>'''
        
        return svg
