#!/usr/bin/env python3
"""
Web interface for the MCP Music Server
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from mcp_server_class import MCPServer

app = FastAPI(title="MCP Music Server", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the music server
music_server = MCPServer()

@app.get("/")
async def root():
    return {"message": "MCP Music Server API", "status": "running"}

@app.get("/search/spotify/{query}")
async def search_spotify_tracks(query: str, limit: int = 10):
    """Search Spotify tracks"""
    try:
        results = await music_server.search_spotify_tracks(query, limit)
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/youtube/{query}")
async def search_youtube_videos(query: str, max_results: int = 10):
    """Search YouTube videos"""
    try:
        results = await music_server.search_youtube_videos(query, max_results)
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/lastfm/{query}")
async def search_lastfm_songs(query: str, limit: int = 10):
    """Search Last.fm songs"""
    try:
        results = await music_server.search_lastfm_songs(query, limit)
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/all/{query}")
async def search_all_platforms(query: str, limit: int = 5):
    """Search across all platforms"""
    try:
        results = await music_server.search_all_platforms(query, limit)
        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 