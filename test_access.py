#!/usr/bin/env python3
"""
Test script to check if the music services are accessible
"""

import asyncio
from mcp_server_class import MCPServer

async def test_music_services():
    """Test accessing the music services"""
    print("Testing MCP Music Server access...")
    
    # Initialize the server
    server = MCPServer()
    
    # Test Spotify
    print("\n1. Testing Spotify search...")
    try:
        spotify_results = await server.search_spotify_tracks("Bohemian Rhapsody", 2)
        if spotify_results and not isinstance(spotify_results[0], dict) or "error" not in spotify_results[0]:
            print(f"✅ Spotify working! Found {len(spotify_results)} tracks")
            for track in spotify_results[:2]:
                print(f"   - {track.get('name', 'Unknown')} by {track.get('artist', 'Unknown')}")
        else:
            print(f"❌ Spotify error: {spotify_results}")
    except Exception as e:
        print(f"❌ Spotify failed: {e}")
    
    # Test YouTube
    print("\n2. Testing YouTube search...")
    try:
        youtube_results = await server.search_youtube_videos("Imagine", 2)
        if youtube_results and not isinstance(youtube_results[0], dict) or "error" not in youtube_results[0]:
            print(f"✅ YouTube working! Found {len(youtube_results)} videos")
            for video in youtube_results[:2]:
                print(f"   - {video.get('title', 'Unknown')}")
        else:
            print(f"❌ YouTube error: {youtube_results}")
    except Exception as e:
        print(f"❌ YouTube failed: {e}")
    
    # Test Last.fm
    print("\n3. Testing Last.fm search...")
    try:
        lastfm_results = await server.search_lastfm_songs("Hotel California", 2)
        if lastfm_results and not isinstance(lastfm_results[0], dict) or "error" not in lastfm_results[0]:
            print(f"✅ Last.fm working! Found {len(lastfm_results)} songs")
            for song in lastfm_results[:2]:
                print(f"   - {song.get('name', 'Unknown')} by {song.get('artist', 'Unknown')}")
        else:
            print(f"❌ Last.fm error: {lastfm_results}")
    except Exception as e:
        print(f"❌ Last.fm failed: {e}")
    
    # Test cross-platform search
    print("\n4. Testing cross-platform search...")
    try:
        cross_results = await server.search_all_platforms("jazz", 2)
        if cross_results and "status" in cross_results and cross_results["status"] == "success":
            print("✅ Cross-platform search working!")
            print(f"   Spotify: {len(cross_results.get('spotify', {}).get('tracks', []))} tracks")
            print(f"   YouTube: {len(cross_results.get('youtube', {}).get('videos', []))} videos")
            print(f"   Last.fm: {len(cross_results.get('lastfm', {}).get('tracks', []))} tracks")
        else:
            print(f"❌ Cross-platform error: {cross_results}")
    except Exception as e:
        print(f"❌ Cross-platform failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_music_services()) 