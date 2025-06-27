"""
Music Orchestrator for MCP music server
This module provides the MusicDiscoveryOrchestrator class for coordinating
searches across multiple platforms.
"""

import asyncio
import logging
from typing import Any, Dict, List

from servicies.spotify_service import SpotifyService
from servicies.youtube_service import YouTubeService
from servicies.lastfm_service import LastfmService

logger = logging.getLogger(__name__)

class MusicDiscoveryOrchestrator:
    """Orchestrates music discovery across multiple platforms."""

    def __init__(self,
                 spotify_service: SpotifyService,
                 youtube_service: YouTubeService, 
                 lastfm_service: LastfmService):
        self.spotify = spotify_service
        self.youtube = youtube_service
        self.lastfm = lastfm_service

    async def search_all_platforms(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Search for music across all platforms"""
        try:
            # Search all platforms concurrently
            spotify_tasks = [
                self.spotify.search_tracks(query, limit),
                self.spotify.search_artists(query, limit),
                self.spotify.search_albums(query, limit)
            ]

            youtube_tasks = [
                self.youtube.search_music_playlists(query, limit),
                self.youtube.search_music_videos(query, limit)
            ]

            lastfm_tasks = [
                self.lastfm.search_tracks(query, limit),
                self.lastfm.search_artists(query, limit),
                self.lastfm.search_albums(query, limit)
            ]

            # Execute all searches
            spotify_results = await asyncio.gather(*spotify_tasks, return_exceptions=True)
            youtube_results = await asyncio.gather(*youtube_tasks, return_exceptions=True)
            lastfm_results = await asyncio.gather(*lastfm_tasks, return_exceptions=True)

            return {
                "query": query,
                "spotify": {
                    "tracks": spotify_results[0] if not isinstance(spotify_results[0], Exception) else [],
                    "artists": spotify_results[1] if not isinstance(spotify_results[1], Exception) else [],
                    "albums": spotify_results[2] if not isinstance(spotify_results[2], Exception) else []
                },
                "youtube": {
                    "videos": youtube_results[0] if not isinstance(youtube_results[0], Exception) else [],
                    "playlists": youtube_results[1] if not isinstance(youtube_results[1], Exception) else []
                },
                "lastfm": {
                    "tracks": lastfm_results[0] if not isinstance(lastfm_results[0], Exception) else [],
                    "artists": lastfm_results[1] if not isinstance(lastfm_results[1], Exception) else [],
                    "albums": lastfm_results[2] if not isinstance(lastfm_results[2], Exception) else []
                },
                "status": "success"
            }
        except Exception as e:
            logger.error(f"Error in cross-platform search: {e}")
            return {"status": "error", "message": str(e)}
        
    async def get_music_recommendations(self,
                                        seed_tracks: List[str] = None,
                                        seed_artists: List[str] = None) -> Dict[str, Any]:
        """Get music recommendations from Spotify"""
        try:
            recommendations = await self.spotify.get_recommendations(
                seed_tracks=seed_tracks,
                seed_artists=seed_artists,
                limit=10
            )
            return {
                "recommendations": recommendations,
                "status": "success"
            }
        
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            return {"status": "error", "message": str(e)}
