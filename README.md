# youtube-api

## Setup
```shell
git clone https://github.com/sujpac/youtube-api.git
cd youtube-api
python3 -m venv env
source env/bin/activate
```
Go to the [Google Console](https://console.developers.google.com/projectselector2/apis/dashboard) and create a new project. Enable the YouTube Data API v3. Then, do the following:
1. Create OAuth client ID credentials (for the `scrape_video_comments.py` script), choosing desktop for the application type.
2. Download the client secrets file, rename it to `client_secret.json`, and move it to the top-level `youtube-api` project directory.
3. Create API Key credentials (for the `get_playlist_duration.py` script).
4. Securely store your API key through setting an environment variable. Add the line `export YT_API_KEY="replace-7FP-fake-ApI-key-f0r-exampl3"` to `.bashrc`, `.zshrc`, or whatever your shell configuration file is.

## Dependencies
```shell
> pip install google-api-python-client
> pip install google-auth google-auth-oauthlib google-auth-httplib2
```

## Usage

### Scrape comments of videos found by keyword search
```shell
> python scrape_video_comments.py
Enter a keyword: async python

> cat comments.csv
VideoID,Title,Comment
sBVb4IB3O_U,"Let&#39;s Build a Fast, Modern Python API with FastAPI",Thank you for sharing
sBVb4IB3O_U,"Let&#39;s Build a Fast, Modern Python API with FastAPI",23:06 Paul Everitt has the goofiest serious face I've ever seen
sBVb4IB3O_U,"Let&#39;s Build a Fast, Modern Python API with FastAPI",20:05 that's a good idea
[output continued in comments.csv]
```

### Compute the total duration of a playlist
```shell
> python get_playlist_duration.py
Enter a YouTube playlist ID: PLSQl0a2vh4HCNiooUekZDy0LEfhikAu3Z
Playlist title: Rise to world power (1890-1945) | US History | Khan Academy
Number of videos: 16
Total duration: 2hrs 11mins 59secs
Average video duration: 8mins 14secs
```

## License
This project is under the MIT License. See the [LICENSE](https://github.com/sujpac/youtube-api/blob/main/LICENSE) file for the full license text.
