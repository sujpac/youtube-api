from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow

import os


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_key = os.environ.get('YT_API_KEY')
    api_service_name = 'youtube'
    api_version = 'v3'
    # print(api_key)
    channel_id = 'UCTw-cD-yziryZbvajczbx9A'

    # flow = InstalledAppFlow
    youtube = build(api_service_name, api_version, developerKey=api_key)

    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_id,
    )
    response = request.execute()

    print(response)


if __name__ == '__main__':
    main()
