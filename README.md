# Spotify Downloader

A small utility to download Spotify playlists and convert them into MP3 files (e.g. for use with Shokz headphones).

## Requirements

- Python 3.12+ (use [`uv`](https://docs.astral.sh/uv/) to manage)  
- [ffmpeg](https://ffmpeg.org/)  
- [Node.js](https://nodejs.org/) (with `yarn`)  
- [freyr-js](https://github.com/miraclx/freyr-js)  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (YouTube downloader backend used by freyr)

## Python Setup with `uv`

[`uv`](https://docs.astral.sh/uv/) makes Python version management simple.

### Install `uv`
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Create a virtual environment with Python 3.12
```bash
uv venv venv --python 3.12
source venv/bin/activate
```

(Use `uv python list` to see available versions, `uv python install 3.12` to install if missing.)

### Install dependencies
```bash
pip install invoke
yarn install
```

## Configuration

1. Copy the default config:  
   ```bash
   cp freyr-config/conf.default.json freyr-config/conf.json
   ```
2. Add your Spotify API secrets to `freyr-config/conf.json`.  
   (`conf.json` is gitignored, so your secrets stay local.)

## Spotify API Setup

Freyr requires a Spotify Developer API client to fetch playlists.

1. Go to [Spotify for Developers Dashboard](https://developer.spotify.com/dashboard).  
2. Log in and create a new **App**.  
3. Copy the **Client ID** and **Client Secret**.  
4. Edit your local `freyr-config/conf.json` and update it like this:

   ```json
   {
     "spotify": {
       "clientId": "YOUR_CLIENT_ID",
       "clientSecret": "YOUR_CLIENT_SECRET"
     }
   }
   ```

5. Save the file. This token is required for Freyr to work.

## Usage

### Download a playlist
```bash
invoke get-playlist --playlist-id=https://open.spotify.com/playlist/<id>
```

### Convert `.m4a` to `.mp3`
```bash
invoke convert-all-m4a ./data
```

### Copy all MP3s to your device
```bash
invoke copy-all-mp3 --dest-dir=/path/to/your/device
```

## Troubleshooting

- **yt-dlp ImportError: unsupported Python**  
  Ensure your virtual environment is Python **3.9 or above** (this project expects 3.12).  
  Check with:  
  ```bash
  python -V
  ```
  If incorrect, recreate the venv with `uv` using Python 3.12.

