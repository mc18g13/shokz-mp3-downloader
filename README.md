# Spotify Downloader

A small utility to download Spotify playlists and convert them into MP3 files (e.g. for use with Shokz headphones).

## Get Started

Full run, from scratch:

```bash
# one-time setup
sudo apt install ffmpeg atomicparsley
uv sync
yarn install
cp freyr-config/conf.default.json freyr-config/conf.json
# edit freyr-config/conf.json — add your Spotify clientId/clientSecret
# (see "Spotify API Setup" below)

# download a playlist
uv run invoke get-playlist --playlist-id=https://open.spotify.com/playlist/<id>

# convert m4a → mp3
uv run invoke convert-all-m4a --directory=./data

# copy to your device (adjust mount path)
uv run invoke copy-all-mp3 --dest-dir=/path/to/your/device
```

## Requirements

- Python 3.12+ (use [`uv`](https://docs.astral.sh/uv/) to manage)  
- [ffmpeg](https://ffmpeg.org/)  
- [AtomicParsley](https://github.com/wez/AtomicParsley) (metadata embedding, used by freyr)  
- [Node.js](https://nodejs.org/) (with `yarn`)  
- [freyr-js](https://github.com/miraclx/freyr-js)  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (YouTube downloader backend used by freyr)

## Setup

### Install `uv` (if missing)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install dependencies
```bash
uv sync
yarn install
```

`uv sync` creates `.venv` and installs Python dependencies automatically. Run tasks with `uv run invoke ...` — no manual venv activation needed.

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
     "services": {
       "spotify": {
         "clientId": "YOUR_CLIENT_ID",
         "clientSecret": "YOUR_CLIENT_SECRET"
       }
     }
   }
   ```

5. Save the file. This token is required for Freyr to work.

## Usage

### Download a playlist
```bash
uv run invoke get-playlist --playlist-id=https://open.spotify.com/playlist/<id>
```

### Convert `.m4a` to `.mp3`
```bash
uv run invoke convert-all-m4a ./data
```

### Copy all MP3s to your device
```bash
uv run invoke copy-all-mp3 --dest-dir=/path/to/your/device
```

## Troubleshooting

- **no audio-formats available**
  ```
  yarn remove freyr
  yarn remove youtube-dl-exec
  yarn remove yt-search
  yarn add freyr
  ```