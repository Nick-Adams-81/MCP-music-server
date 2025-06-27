"""
MCP server class for music.
This module contains the MCPServer class that provides the core functionality 
for the music MCP server
"""

import logging
import os
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from servicies.spotify_service import SpotifyService
from servicies.youtube_service import YouTubeService
from servicies.lastfm_service import LastfmService
from orchestrator import MusicDiscoveryOrchestrator

logger = logging.getLogger(__name__)

class AuthConfig(BaseModel):
    """Configuration for authentication across different music servicies"""
    spotify_client_id: Optional[str] = Field(default=None, description="Spotify client ID")
    spotify_client_secret: Optional[str] = Field(default=None, description="Spotify client secret")
    spotify_redirect_uri: Optional[str] = Field(default=None, description="Spotify redirect URI")
    youtube_api_key: Optional[str] = Field(default=None, description="YouTube Data API key")
    lastfm_api_key: Optional[str] = Field(default=None, description="Last.fm API key")

class MCPServer:
    """Main MCP server implementatoin for music server"""

    def __init__(self):
        self.auth_config = AuthConfig(
            spotify_client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            spotify_client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            spotify_redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
            youtube_api_key=os.getenv('YOUTUBE_API_KEY'),
            lastfm_api_key=os.getenv('LASTFM_API_KEY')
        )

        self.spotify_service = None
        self.youtube_service = None
        self.lastfm_service = None
        self.orchestrator = None

        self.initialize_servicies()

    def initialize_servicies(self) -> None:
        """Initialize allmusic servicie connections"""
        try:
            if self.auth_config.spotify_client_id and self.auth_config.spotify_client_secret:
                self.spotify_service = SpotifyService(
                    self.auth_config.spotify_client_id,
                    self.auth_config.spotify_client_secret,
                    self.auth_config.spotify_redirect_uri
                )
                logger.info("Spotify service initialized.")

            if self.auth_config.youtube_api_key:
                self.youtube_service = YouTubeService(
                    self.auth_config.youtube_api_key
                )
                logger.info("YouTube service initialized")

            if self.auth_config.lastfm_api_key:
                self.lastfm_service = LastfmService(
                    self.auth_config.lastfm_api_key
                )
                logger.info("Last.fm service initialized")

            if any([self.spotify_service, self.youtube_service, self.lastfm_service]):
                self.orchestrator = MusicDiscoveryOrchestrator(
                    self.spotify_service, self.youtube_service, self.lastfm_service
                )
                logger.info("Music discovery orchestrator initialized")
        except Exception as e:
            logger.error(f"Error initializing servicies: {e}")

    # Spotify methods
    async def search_spotify_tracks(self, query: str, limit: int = 10) -> List[Dict[str, any]]:
        """Search Tracks on spotify"""
        if not self.spotify_service:
            return [{"Error": "Spotify service unavailable"}]
        return await self.spotify_service.search_tracks(query, limit)
    
    async def search_spotify_artists(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for artists on Spotify"""
        if not self.spotify_service:
            return [{"error": "Spotify service unavailable"}]
        return await self.spotify_service.search_artists(query, limit)
        
    async def search_spotify_albums(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for albums on Spotify"""
        if not self.spotify_service:
            return [{"error": "spotify service unavailable"}]
        return await self.spotify_service.search_albums(query, limit)
    
    async def get_spotify_recommendations(self, seed_tracks: List[str] = None, seed_artists: List[str] = None) -> List[Dict[str, Any]]:
        """Get Spotify recommendations"""
        if not self.spotify_service:
            return [{"error": "Spotify service unavailable"}]
        return await self.spotify_service.get_recommendations(seed_tracks, seed_artists)
    
    # YouTube methods
    async def search_youtube_videos(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search music videos on YouTube"""
        if not self.youtube_service:
            return [{"error": "YouTube service unavailable"}]
        return await self.youtube_service.search_music_videos(query, max_results)
    
    async def search_youtube_playlists(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search YouTube playlists for music"""
        if not self.youtube_service:
            return [{"error": "YouTube service unavailable"}]
        return await self.youtube_service.search_music_playlists(query, max_results)
    
    async def get_youtube_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        if not self.youtube_service:
            return [{"error": "YouTube service unavailable"}]
        return await self.youtube_service.get_video_details(video_id)
    
    # Last.fm methods
    async def search_lastfm_songs(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for songs on Last.fm"""
        if not self.lastfm_service:
            return [{"error": "last.fm service unavailable"}]
        return await self.lastfm_service.search_tracks(query, limit)
    
    async def search_lastfm_albums(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search albums on Last.fm"""
        if not self.lastfm_service:
            return [{"error": "Last.fm service unavailable"}]
        return await self.lastfm_service.search_albums(query, limit)
    
    async def search_lastfm_artists(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search artists on Last.fm"""
        if not self.lastfm_service:
            return [{"error": "Last.fm service unavailable"}]
        return await self.lastfm_service.search_artists(query, limit)
    
    async def get_lastfm_similar_tracks(self, artist: str, track: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Find similar tracks on Last.fm"""
        if not self.lastfm_service:
            return [{"error": "Last.fm service unavailable"}]
        return await self.lastfm_service.get_similar_tracks(artist, track, limit)
    
    async def get_lastfm_top_tracks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top tracks on Last.fm"""
        if not self.lastfm_service:
            return [{"error": "Last.fm service unavailable"}]
        return await self.lastfm_service.get_top_tracks(limit)
    
    # Cross-platform methods
    async def search_all_platforms(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Search all platforms"""
        if not self.orchestrator:
            return [{"error": "Music orchestrator not available"}]
        return await self.orchestrator.search_all_platforms(query, limit)
    
    async def get_music_recommendations(self, seed_tracks: List[str] = None, seed_artists: List[str] = None) -> Dict[str, Any]:
        """Get music recommendations"""
        if not self.orchestrator:
            return [{"error": "Music orchestrator not available"}]
        return await self.orchestrator.get_music_recommendations(seed_tracks, seed_artists)


