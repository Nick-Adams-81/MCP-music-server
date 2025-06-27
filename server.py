"""
MCP Server for Music
This server connects to Spotify, YouTube, and Last.fm APIs to provide
comprehensive music search and discovery capabilities.
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from dotenv import load_dotenv
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from pydantic import BaseModel, Field

# MCP server class
from mcp_server_class import MCPServer

# Service classes
from servicies.spotify_service import SpotifyService
from servicies.lastfm_service import LastfmService
from servicies.youtube_service import YouTubeService

# Load environment variables
load_dotenv()

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_environment() -> Dict[str, bool]:
    """Validate required environment variables are set."""
    required_variables = {
        'spotify': ['SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET'],
        'youtube': ['YOUTUBE_API_KEY'],
        'lastfm': ['LASTFM_API_KEY']
    }

    validation_results = {}

    for service, variables_list in required_variables.items():
        missing_variables = []
        for variable in variables_list:
            if not os.getenv(variable):
                missing_variables.append(variable)
        if missing_variables:
            logger.warning(f"{service.upper()} service will be disabled. Missing: {', '.join(missing_variables)}")
            validation_results[service] = False
        else:
            logger.info(f"{service.upper()} credentials found.")
            validation_results[service] = True
    return validation_results

async def main():
    """Main entry point for the MCP server"""
    logger.info("Validating environment configuration....")
    validation_results = validate_environment()

    available_servicies = [service for service, available in validation_results.items() if available]
    if not available_servicies:
        logger.error("No music servicies configured! Please set up your API credentials")
        logger.info("See env_example.txt for configuration instructions")
    else:
        logger.info(f"Available servicies: {', '.join(available_servicies)}")

    server = Server("music-server")
    mcp_server = MCPServer()

    @server.list_tools()
    async def handle_list_tools() -> List[Dict[str, Any]]:
        """List available music tools"""
        return [
            #Spotify tools
            {
                "name": "search_spotify_tracks",
                "description": "Search for tracks on Spotify",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for tracks"},
                        "limit": {"type": "integer", "description": "Max number of results (default: 10)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "search_spotify_artists",
                "description": "Search for artists on Spotify",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for artists"},
                        "limit": {"type": "integer", "description": "Max number of results (default: 10)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "search_spotify_albums",
                "description": "Search for albums on Spotify",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for albums"},
                        "limit": {"type": "integer", "description": "Max number of results (default: 10)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_spotify_recommendations",
                "description": "Get track reommendations from Spotify",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "seed_tracks": {"type": "array", "items": {"type": "string"},"description": "List of Spotify track IDs"},
                        "seed_artists": {"type": "array", "items": {"type": "string"}, "description": "List of Spotify artist ID"}
                    },
                    "required": []
                }
            },
            # YouTube Tools
            {
                "name": "search_youtube_videos",
                "description": "Search for music videos in YouTube",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search for music videos on YouTube"},
                        "max_results": {"type": "integer", "description": "Max number of results (default: 10)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "search_youtube_video_details",
                "description": "Get detailed information about a YouTube video",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "video_id": {"type": "string", "description": "YouTube video ID"}
                    },
                    "required": ["video_id"]
                }
            },
            # Last.fm tools
            {
                "name": "search_lastfm_songs",
                "description": "Search for songs on Last.fm",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for Last.fm"},
                        "limit": {"type": "integer", "description": "Max number of results (default: 10)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "search_lastfm_artists",
                "description": "search Last.fm for artists",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description" : "Search query for artists"},
                        "limit": {"type": "integer", "description": "Max number of results (default: 10)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "search_lastfm_albums",
                "description": "Search Last.fm for albums",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search Last.fm for albums"},
                        "limit": {"type": "integer", "description": "Max number of results (default: 10)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_lastfm_top_tracks",
                "description": "Get top tracks from Last.fm charts",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Max number of results (default: 5)"}
                    },
                    "required": []
                }
            },
            # Cross-platform tools
            {
                "name": "search_all_platforms",
                "description": "Search music across all platforms (Spotify, YouTube, Last.fm)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for music"},
                        "limit": {"type": "integer", "description": "Max number of results (default: 5)"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_music_recommendations",
                "description": "Get music recommendations based on seeds",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "seed_tracks": {"type": "array", "items": {"type": "string"}, "description": "List of Spotify track IDs"},
                        "seed_artists": {"type": "array", "items": {"type": "string"}, "description": "List of Spotify artist IDs"}
                    },
                    "required": []
                }
            }
        ]
    
    @server.call_tool()
    async def handle_call_tool(name: str, args: Dict[str, any]) -> Dict[str, Any]:
        """Handle music discovery tool calls"""
        try:
            if name == "search_spotify_tracks":
                result = await mcp_server.search_spotify_tracks(
                    args.get("query"),
                    args.get("limit", 10)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

            elif name == "search_spotify_artists":
                result = await mcp_server.search_spotify_artists(
                    args.get("query"),
                    args.get("limit", 10)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

            elif name == "search_spotify_albums":
                result = await mcp_server.search_spotify_albums(
                    args.get("query"),
                    args.get("limit", 10)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "get_spotify_recommendations":
                result = await mcp_server.get_spotify_recommendations(
                    args.get("query"),
                    args.get("limit", 10)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "search_youtube_videos":
                result = await mcp_server.search_youtube_videos(
                    args.get("query"),
                    args.get("max_results", 10)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "search_youtube_playlists":
                result = await mcp_server.search_youtube_playlists(
                    args.get("query"),
                    args.get("max_results", 10)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "get_youtube_video_details":
                result = await mcp_server.get_youtube_video_details(
                    args.get("video_id")
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "search_lastfm_songs":
                result = await mcp_server.search_lastfm_songs(
                    args.get("query"),
                    args.get("limit", 10)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "search_lastfm_albums":
                result = await mcp_server.search_lastfm_albums(
                    args.get("query"),
                    args.get("limit", 10)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "search_lastfm_artists":
                result = await mcp_server.search_lastfm_artists(
                    args.get("query"),
                    args.get("limit", 10)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "get_lastfm_similar_tracks":
                result = await mcp_server.get_lastfm_similar_tracks(
                    args.get("artist"),
                    args.get("track"),
                    args.get("limit", 10)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "get_lastfm_top_tracks":
                result = await mcp_server.get_lastfm_top_tracks(
                    args.get("limit", 10)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "search_all_platforms":
                result = await mcp_server.search_all_platforms(
                    args.get("query"),
                    args.get("limit", 5)
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            elif name == "get_music_recommendations":
                result = await mcp_server.get_music_recommendations(
                    args.get("seed_tracks"),
                    args.get("seed_artists")
                )
                return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}
            
            else :
                return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}]}
        except Exception as e:
            logger.error(f"Error in tool call {name}: {e}")
            return {"content": [{"type": "text", "text": f"Error: {str(e)}"}]}
        
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="music-discovery-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())


