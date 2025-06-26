"""
Services package for MCP Music Server.

This package contains all the music service classes for inteacting
with various music APIs, such as Spotify, YpuTube, and Last.fm.
"""

from .spotify_service import SpotifyService
from .youtube_service import YouTubeService
from .lastfm_service import LastfmService

__all__ = ["SpotifyService", "YouTubeService", "LastfmService"]