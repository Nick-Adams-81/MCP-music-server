"""
YouTube service for MCP Music server
This module provides the YouTubeService class for interacting with the YouTube Data API.
"""

import logging
from typing import Any, Dict, List, Optional

from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

class YouTubeService:
    """Service for interacting with YouTube data API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    async def search_music_videos(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for music videos on YouTube"""
        try:
            request = self.youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                videoCategoryId='10',
                maxResults=max_results,
                order='relevance'
            )
            response = request.execute()
            videos = []

            for item in response['items']:
                video = {
                    "id": item['id']['videoId'],
                    "title": item['snippet']['title'],
                    "channel": item['snippet']['channelTitle'],
                    "description": item['snippet']['description'],
                    "published_at": item['snippet']['publishedAt'],
                    "thumbnail": item['snippet']['thumbnails']['high']['url'],
                    "youtube_url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                videos.append(video)
            
            return videos
        except Exception as e:
            logger.error(f"Error searching YouTube music videos: {e}")
            return []
        
    async def search_music_playlists(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for music playlists on YouTube."""
        try:
            request = self.youtube.search().list(
                part='snippet',
                q=query,
                type='playlist',
                maxResults=max_results,
                order='relevance'
            )
            
            response = request.execute()
            playlists = []
            
            for item in response['items']:
                playlist = {
                    "id": item['id']['playlistId'],
                    "title": item['snippet']['title'],
                    "channel": item['snippet']['channelTitle'],
                    "description": item['snippet']['description'],
                    "published_at": item['snippet']['publishedAt'],
                    "thumbnail": item['snippet']['thumbnails']['high']['url'],
                    "youtube_url": f"https://www.youtube.com/playlist?list={item['id']['playlistId']}"
                }
                playlists.append(playlist)
            
            return playlists
        except Exception as e:
            logger.error(f"Error searching YouTube playlists: {e}")
            return []
        
    async def get_video_details(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a YouTube video."""
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=video_id
            )
            
            response = request.execute()
            
            if response['items']:
                item = response['items'][0]
                video = {
                    "id": item['id'],
                    "title": item['snippet']['title'],
                    "channel": item['snippet']['channelTitle'],
                    "description": item['snippet']['description'],
                    "duration": item['contentDetails']['duration'],
                    "view_count": item['statistics']['viewCount'],
                    "like_count": item['statistics'].get('likeCount', 0),
                    "published_at": item['snippet']['publishedAt'],
                    "youtube_url": f"https://www.youtube.com/watch?v={item['id']}"
                }
                return video
            
            return None
        except Exception as e:
            logger.error(f"Error getting YouTube video details: {e}")
            return None 