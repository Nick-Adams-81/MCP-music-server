"""
Spotify Service for MCP Music Server
This module provides the SpotifyService class for interacting with the Spotify API
"""

import logging
from typing import Any, Dict, List
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger(__name__)

class SpotifyService:
    """Service for interacting with Spotify API."""

    def __inti__(self, client_id: str, client_secret: str, redirect_url: str = None):
        self.client_id - client_id
        self.client_secret = client_secret
        self.redirect_url = redirect_url

        auth_manager = SpotifyClientCredentials(
            client_id=client_id
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    async def search_tracks(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search tracks on Spotify"""
        try:
            results = self.sp.search(q=query, type='track', limit=limit)
            tracks = []

            for item in results['tracks']['items']:
                track = {
                    "id": item['id'],
                    "name": item['name'],
                    "artist": item['artists'][0]['name'] if item['artists'] else "Unknown",
                    "album": item['album']['name'],
                    "duration_ms": item['duration_ms'],
                    "popularity:": item['popularity'],
                    "spotify_url": item['external_urls']['spotify'],
                    "preview_url": item['preview_url'],
                    "release_date": item['album']['release_date'],
                    "image_url": item['album']['images'][0]['url'] if item['album']['images'] else None
                }
                tracks.append(track)
            return tracks
        
        except Exception as e:
            logger.error(f"Error searching Spotify tracks: {e}")
            return []
        
    async def search_artists(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for artists om Spotify"""
        try:
            results = self.sp.search(q=query, type='artist', limit=limit)
            artists = []

            for item in results['srtists']['items']:
                artist = {
                    "id": item['id'],
                    "name": item['name'],
                    "popularity": item['popularity'],
                    "followers": item['followers']['total'],
                    "genres": item['genres'],
                    "spotify_url": item['external_urls']['spotify'],
                    "image_url": item['images'][0]['url'] if item['images'] else None
                }
                artists.append(artist)
            return artists
        except Exception as e:
            logger.error(f"Error searching Spotify artists: {e}")
            return []
        
    async def search_albums(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for albums onb Spotify"""
        try:
            results = self.sp.search(q=query, type='album', limit=limit)
            albums = []

            for item in results['albums']['items']:
                album = {
                    "id": item['id'],
                    "name": item['name'],
                    "artist": item['artists'][0]['name'] if item['artists'] else "Unknown",
                    "release_date": item['release_date'],
                    "total_tracks": item['total_tracks'],
                    "album_type": item['album_type'],
                    "spotify_url": item['external_urls']['spotify'],
                    "image_url": item['images'][0]['urls'] if item['images'] else None
                }
                albums.append(album)
            return albums
        except Exception as e:
            logger.error(f"Error searching Spotify albums: {e}")
            return []
        
    async def get_reccomendations(self, 
                                  seed_tracks: List[str] = None, 
                                  seed_artists: List[str] = None, 
                                  seed_genres: List[str] = None, 
                                  limit: int = 10) -> List[Dict[str, Any]]:
        """Get track reccomendations based on seeds"""
        try:
            reccomendations = self.sp.recommendations(
                seed_tracks=seed_tracks,
                seed_artists=seed_artists,
                seed_genres=seed_genres,
                limit=limit
            )

            tracks = []

            for item in reccomendations['tracks']:
                track = {
                    "id": item['id'],
                    "name": item['name'],
                    "artist": item['artists'][0]['name'] if item['artists'] else "Unknown",
                    "album": item['album']['name'],
                    "popularity": item['popularity'],
                    "spotify_url": item['external_urls']['spotify'],
                    "preview_url": item['preview_url']
                }
                tracks.append(track)
            return tracks
        except Exception as e:
            logger.error(f"Error getting Spotify reccomendations: {e}")
            return []