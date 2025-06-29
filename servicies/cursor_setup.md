# Cursor MCP Music Discovery Server Setup

This guide will help you configure the MCP music discovery server to work with Cursor.

## 🚀 Quick Setup

1. **Run the setup script:**
   ```bash
   ./setup_cursor.sh
   ```

2. **Add your API keys to `.env` file**
3. **Configure Cursor (see steps below)**
4. **Test the integration**

## 📋 Manual Setup Steps

### 1. Install Dependencies

```bash
pip install mcp spotipy google-api-python-client requests python-dotenv
```

### 2. Set Up API Keys

Create a `.env` file in the project root:

```bash
# Spotify API (https://developer.spotify.com/dashboard)
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

# YouTube Data API (https://console.cloud.google.com/)
YOUTUBE_API_KEY=your_youtube_api_key_here

# Last.fm API (https://www.last.fm/api/account/create)
LASTFM_API_KEY=your_lastfm_api_key_here
```

### 3. Configure Cursor

#### Option A: Using Cursor Settings UI
1. Open Cursor
2. Go to **Settings** (Cmd/Ctrl + ,)
3. Search for "MCP" or go to **Extensions > MCP**
4. Click **Add Server**
5. Configure with these settings:
   - **Name**: `music-discovery`
   - **Command**: `python`
   - **Arguments**: `["mcp_server.py"]`
   - **Working Directory**: `/Users/nicholasadams/Code/mcp-test-project`

#### Option B: Using Settings JSON
1. Open Cursor Settings (Cmd/Ctrl + Shift + P → "Preferences: Open Settings (JSON)")
2. Add this configuration:

```json
{
  "mcp.servers": {
    "music-discovery": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/Users/nicholasadams/Code/mcp-test-project"
    }
  }
}
```

### 4. Test the Setup

1. **Restart Cursor**
2. **Test locally first:**
   ```bash
   python evaluator.py
   ```
3. **Test with Cursor:**
   - Open a new chat in Cursor
   - Ask: "Search for jazz tracks on Spotify"
   - Cursor should use the MCP server to fetch results

## 🎵 Available Tools

Once configured, you can ask Cursor to:

### Spotify Tools
- "Search for jazz tracks on Spotify"
- "Find artists like Queen on Spotify"
- "Get album recommendations from Spotify"

### YouTube Tools
- "Find music videos for Bohemian Rhapsody on YouTube"
- "Search for rock playlists on YouTube"

### Last.fm Tools
- "Get similar tracks to Bohemian Rhapsody from Last.fm"
- "Show me top tracks from Last.fm charts"

### Cross-Platform Tools
- "Search for rock music across all platforms"
- "Get music recommendations"

## 🔧 Troubleshooting

### Server Won't Start
- Check that all dependencies are installed
- Verify your `.env` file has the correct API keys
- Run `python mcp_server.py` manually to see error messages

### Cursor Can't Find the Server
- Verify the working directory path is correct
- Make sure the `mcp_server.py` file exists in the specified directory
- Check that Cursor has permission to execute Python

### API Errors
- Verify your API keys are correct
- Check that you have the necessary API quotas/permissions
- Test individual services using the evaluator

### No Tools Available
- Restart Cursor after configuration
- Check the Cursor console for MCP-related errors
- Verify the server is running and responding

## 📁 File Structure

```
mcp-test-project/
├── mcp_server.py              # Main MCP server
├── mcp_server_class.py        # MCPServer class
├── evaluator.py               # Testing framework
├── services/                  # API service classes
├── .env                       # API keys (create this)
├── .cursorrules              # Cursor project rules
├── cursor_mcp_config.json    # MCP configuration
├── setup_cursor.sh           # Setup script
└── CURSOR_SETUP.md           # This file
```

## 🎯 Example Usage

Here are some example prompts you can try in Cursor:

1. **"Search for jazz tracks on Spotify and show me the top 5 results"**
2. **"Find music videos for Queen's Bohemian Rhapsody on YouTube"**
3. **"Get similar tracks to Hotel California from Last.fm"**
4. **"Search for rock music across all platforms and compare the results"**
5. **"Get Spotify recommendations based on my favorite artists"**

## 🔄 Updating Configuration

If you need to update the MCP server configuration:

1. Stop Cursor
2. Update the configuration in Settings
3. Restart Cursor
4. Test with a simple query

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run the evaluator to test individual components
3. Check Cursor's console for error messages
4. Verify your API keys and permissions

---

**Happy music discovering with Cursor! 🎵** 