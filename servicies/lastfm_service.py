"""
Last.fm Service for MCP Music Server.

This module provides the LastfmService class for interacting 
with the Last.fm API.
"""

import logging
from typing import Any, Dict, List
import httpx

logger = logging.getLogger(__name__)

class LastfmService:
    """Service for interacting with the Last.fm API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://ws.audioscrobbler.com/2.0/"

        async def search_tracks(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
            """Search tracks on Last.fm."""
            try: 
                params = {
                    'method': 'track.search',
                    'track': query,
                    'api_key': self.api_key,
                    'format': 'json',
                    'limit': limit
                }

                async with httpx.AsyncClient() as client:
                    response = await client.get(self.base_url, params=params)

                    if response.status_code == 200:
                        data = response.json()
                        tracks = []

                        if 'results' in data and 'trackmatches' in data['results']:
                            for item in data['results']['trackmatches']['track']:
                                track = {
                                    "name": item['name'],
                                    "artist": item['artist'],
                                    "url": item['url'],
                                    "listeners": item.get('listeners', 0),
                                    "image": item.get('image', []),
                                    "mbid": item.get('mbid', '')
                                }
                                tracks.append(track)
                            return tracks
                    else:
                        logger.error(f"Last.fm API error: {response.status_code}")
            except Exception as e:
                logger.error(f"Error searching Last.fm tracks: {e}")
                return []
            
        async def search_albums(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
            """Search for albums on Last.fm"""
            try:
                params = {
                    'method': 'album.search',
                    'album': query,
                    'api_key': self.api_key,
                    'format': 'json',
                    'limit':limit
                }

                async with httpx.AsyncClient() as client:
                    response = await client.get(self.base_url, params=params)

                    if response.status_code == 200:
                        data = response.json()
                        albums = []

                        if 'results' in data and 'albummatches' in data['results']:
                            for item in data['results']['albummatches']['album']:
                                album = {
                                    "name": item['name'],
                                    "artist": item['artist'],
                                    "url": item['url'],
                                    "image": item.get('image', []),
                                    "mbid": item.get('mbid', '')
                                }
                                albums.append(album)
                        return albums

                    else:
                        logger.error(f"Last.fm API error: {response.status_code}")
                        return []
            except Exception as e:
                logger.error(f"Error searching Last.fm albums: {e}")
                return []
            
        async def search_artists(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
            """Search an artist on Last.fm"""
            try:
                params = {
                    'method': 'artist.search',
                    'artist': query,
                    'api_key': self.api_key,
                    'format': 'json',
                    'limit': limit
                }

                async with httpx.AsyncClient() as client:
                    response = await client.get(self.base_url, params=params)

                    if response.status_code == 200:
                        data = response.json()
                        artists = []

                        if 'results' in data and 'artistmatches' in data['results']:
                            for item in data['results']['artistmatches']['artist']:
                                artist = {
                                    "name": item['name'],
                                    "url": item['url'],
                                    "listeners": item.get('listeners', 0),
                                    "image": item.get('image', []),
                                    "mbid": item.get('mbid', '')
                                }
                                artists.append(artist)
                        return artists
                    else:
                        logger.error(f"Last.fm API error: {response.status_code}")
                        return []

            except Exception as e:
                logger.error(f"Error searching Last.fm artists: {e}")
                return []
            
        async def get_similar_tracks(self, artist: str, track: str, limit: int = 10) -> List[Dict[str, Any]]:
            """Get similar tracks from Last.fm"""
            try:
                params = {
                    'method': 'track.getsimilar',
                    'artist': artist,
                    'track': track,
                    'api_key': self.api_key,
                    'format': 'json',
                    'limit': limit
                }

                async with httpx.AsyncClient() as client:
                    response = await client.get(self.base_url, params=params)

                    if response.status_code == 200:
                        data = response.json()
                        tracks = []

                        if 'similartracks' in data and 'track' in data['similartracks']:
                            for item in data['similartracks']['track']:
                                track = {
                                    "name": item['name'],
                                    "artist": item['artist']['name'],
                                    "url": item['url'],
                                    "match": item.get('match', 0),
                                    "image": item.get('image', 0)
                                }
                                tracks.append(track)
                        return tracks
                    else:
                        logger.error(f"Last.fm API error: {response.status_code}")
                        return []
            except Exception as e:
                logger.error(f"Error getting Last.fm similar tracks: {e}")
                return []
            
        async def get_top_tracks(self, limit: int = 10) -> List[Dict[str,Any]]:
            """Gettop tracks from Last.fm"""
            try:
                params = {
                    'method': 'chart.gettoptracks',
                    'api_key': self.api_key,
                    'format': 'json',
                    'limit': limit
                }

                async with httpx.AsyncClient() as client:
                    response = await client.get(self.base_url, params=params)

                    if response.status_code == 200:
                        data = response.json()
                        tracks = []

                        if 'tracks' in data and 'track' in data['tracks']:
                            for item in data['tracks']['track']:
                                track = {
                                    "name": item['name'],
                                    "artist": item['artist']['name'],
                                    "url": item['url'],
                                    "listeners": item.get('listeners', 0),
                                    "image": item.get('image', [])
                                }
                                tracks.append(track)
                        return tracks
                    else:
                        logger.error(f"Last.fm API error: {response.status_code}")
                        return []
            except Exception as e:
                logger.error(f"Error getting top tracks from Last.fm: {e}")
                return []
            
        async def search_songs(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
            """Search for songs on Last.fm (alias for search_tracks)"""
            return await self.search_tracks(query, limit)

