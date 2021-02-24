# youtube-api

## Setup
```shell
> git clone https://github.com/sujpac/youtube-api.git
> cd youtube-api
> virtualenv env
> source env/bin/activate
```
Go to the [Google Console](https://console.developers.google.com/projectselector2/apis/dashboard) and create a new project. Go to the Library tab and enable the YouTube Data API v3 API. Then, go to the Credentials tab and do the following:
1. Create OAuth client ID credentials (to be used by `scrape_video_comments.py`) and choose desktop as the application type.
2. Download the client secrets file for the newly created OAuth credentials. Rename it to `client_secret.json`, and move to the `youtube-api` project directory.
```shell
> mv [downloads]/client_secret_10927*.apps.googleusercontent.com.json youtube-api/client_secret.json
```
3. Create API Key credentials (to be used by `get_playlist_duration.py`).
4. Safely store your API key by setting an environment variable in your `.zshrc` (or whatever your shell configuration file is).
```shell
> echo 'export YT_API_KEY="[insert-your-API-key-here]"' >> ~/.zshrc
> source ~/.zshrc
```

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
[...]
[output truncated]
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
