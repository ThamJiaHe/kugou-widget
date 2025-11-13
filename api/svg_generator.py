"""
SVG Generator
Generates SVG widgets for displaying now playing information
"""
from typing import Optional, Dict, Any
import html


def generate_music_svg(
    song_name: str,
    artist_name: str,
    album_cover_url: str = "",
    theme: str = "light",
    width: int = 400,
    height: int = 120,
    show_album: bool = True
) -> str:
    """Generate SVG widget for currently playing song"""
    
    # Escape HTML to prevent XSS
    song_name = html.escape(song_name or "Unknown Song")
    artist_name = html.escape(artist_name or "Unknown Artist")
    
    # Truncate long names
    if len(song_name) > 30:
        song_name = song_name[:27] + "..."
    if len(artist_name) > 30:
        artist_name = artist_name[:27] + "..."
    
    # Theme colors
    if theme == "dark":
        bg_color = "#1a1a1a"
        text_color = "#ffffff"
        secondary_color = "#b3b3b3"
        accent_color = "#1ED760"
    else:
        bg_color = "#ffffff"
        text_color = "#000000"
        secondary_color = "#666666"
        accent_color = "#1DB954"
    
    # Default album cover if none provided
    if not album_cover_url:
        album_cover_url = "https://via.placeholder.com/100x100/333333/ffffff?text=♪"
    
    # Calculate positions
    album_x = 10 if show_album else 0
    text_x = 120 if show_album else 20
    
    svg_content = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .bg {{ fill: {bg_color}; }}
            .title {{ fill: {text_color}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif; font-size: 16px; font-weight: bold; }}
            .artist {{ fill: {secondary_color}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif; font-size: 14px; }}
            .brand {{ fill: {accent_color}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif; font-size: 12px; }}
            .playing-icon {{ fill: {accent_color}; }}
        </style>
    </defs>
    
    <!-- Background -->
    <rect width="{width}" height="{height}" class="bg" rx="10" ry="10"/>
    
    <!-- Border -->
    <rect width="{width-2}" height="{height-2}" x="1" y="1" 
          fill="none" stroke="{secondary_color}" stroke-width="1" rx="9" ry="9" opacity="0.2"/>'''
    
    if show_album:
        svg_content += f'''
    
    <!-- Album Cover -->
    <image x="{album_x}" y="10" width="100" height="100" 
           href="{album_cover_url}" rx="5" ry="5"/>'''
    
    svg_content += f'''
    
    <!-- Playing indicator -->
    <circle cx="{text_x + 5}" cy="25" r="3" class="playing-icon"/>
    <text x="{text_x + 15}" y="29" class="brand">Now Playing</text>
    
    <!-- Song Info -->
    <text x="{text_x}" y="50" class="title">{song_name}</text>
    <text x="{text_x}" y="70" class="artist">by {artist_name}</text>
    
    <!-- Kugou Branding -->
    <text x="{text_x}" y="95" class="brand">♪ Playing on Kugou Music</text>
    
</svg>'''
    
    return svg_content


def generate_default_svg(theme: str = "light", width: int = 400, height: int = 120) -> str:
    """Generate default SVG when no music is playing"""
    
    if theme == "dark":
        bg_color = "#1a1a1a"
        text_color = "#ffffff"
        secondary_color = "#b3b3b3"
    else:
        bg_color = "#ffffff"
        text_color = "#000000"
        secondary_color = "#666666"
    
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .bg {{ fill: {bg_color}; }}
            .title {{ fill: {text_color}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif; font-size: 18px; font-weight: bold; }}
            .subtitle {{ fill: {secondary_color}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif; font-size: 14px; }}
        </style>
    </defs>
    
    <rect width="{width}" height="{height}" class="bg" rx="10" ry="10"/>
    <rect width="{width-2}" height="{height-2}" x="1" y="1" 
          fill="none" stroke="{secondary_color}" stroke-width="1" rx="9" ry="9" opacity="0.2"/>
    
    <!-- Music note icon -->
    <text x="{width//2}" y="{height//2 - 10}" class="title" text-anchor="middle">♪</text>
    <text x="{width//2}" y="{height//2 + 10}" class="title" text-anchor="middle">Not Playing</text>
    <text x="{width//2}" y="{height//2 + 30}" class="subtitle" text-anchor="middle">No music currently playing</text>
</svg>'''
    
    return svg


def generate_error_svg(error_message: str = "Error loading widget", theme: str = "light", width: int = 400, height: int = 120) -> str:
    """Generate SVG widget for error state"""
    
    error_message = html.escape(error_message)
    
    if theme == "dark":
        bg_color = "#1a1a1a"
        text_color = "#ff4444"
        secondary_color = "#b3b3b3"
    else:
        bg_color = "#ffffff"
        text_color = "#cc0000"
        secondary_color = "#666666"
    
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <style>
            .bg {{ fill: {bg_color}; }}
            .error {{ fill: {text_color}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif; font-size: 14px; font-weight: bold; }}
            .subtitle {{ fill: {secondary_color}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', 'Arial', sans-serif; font-size: 12px; }}
        </style>
    </defs>
    
    <rect width="{width}" height="{height}" class="bg" rx="10" ry="10"/>
    <rect width="{width-2}" height="{height-2}" x="1" y="1" 
          fill="none" stroke="{text_color}" stroke-width="1" rx="9" ry="9" opacity="0.3"/>
    
    <text x="{width//2}" y="{height//2 - 5}" class="error" text-anchor="middle">⚠ {error_message}</text>
    <text x="{width//2}" y="{height//2 + 15}" class="subtitle" text-anchor="middle">Please check your configuration</text>
</svg>'''
    
    return svg


class SVGGenerator:
    """Legacy class for backwards compatibility"""
    
    def __init__(self, width: int = 400, height: int = 120):
        self.width = width
        self.height = height
    
    def generate_now_playing_widget(
        self,
        track_name: Optional[str] = None,
        artist_name: Optional[str] = None,
        album_name: Optional[str] = None,
        is_playing: bool = False,
        theme: str = "light"
    ) -> str:
        """Legacy method for generating widgets"""
        if is_playing and track_name and artist_name:
            return generate_music_svg(
                song_name=track_name,
                artist_name=artist_name,
                theme=theme,
                width=self.width,
                height=self.height
            )
        else:
            return generate_default_svg(
                theme=theme,
                width=self.width,
                height=self.height
            )
    
    def generate_error_widget(self, error_message: str = "Error loading widget", theme: str = "light") -> str:
        """Legacy method for error widgets"""
        return generate_error_svg(
            error_message=error_message,
            theme=theme,
            width=self.width,
            height=self.height
        )
