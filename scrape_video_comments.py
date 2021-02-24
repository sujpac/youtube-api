import os
import pickle
import csv
# import httplib2

# import google.oauth2.credentials
from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# from google.auth.transport.requests import requests
from google.auth.exceptions import RefreshError

CLIENT_SECRETS_FILE = "client_secret.json"

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # Refresh the saved credentials if it's expired
    if credentials and credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
        except RefreshError:
            credentials = None
            os.unlink('token.pickle')

    # Check if credentials don't exist
    if not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                                         SCOPES)
        credentials = flow.run_console()

    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(credentials, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def get_videos(service, max_pages=3, **kwargs):
    results = service.search().list(**kwargs).execute()
    final_results = []
    page_number = 1

    while results and page_number <= max_pages:
        final_results.extend(results['items'])
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.search().list(**kwargs).execute()
            page_number += 1
        else:
            break

    return final_results


def get_video_comments(service, **kwargs):
    results = service.commentThreads().list(**kwargs).execute()
    comments = []

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append(comment)

        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break

    # print(comments[0])
    # print(len(comments))
    return comments


def search_videos_by_keyword(service, **kwargs):
    results = get_videos(service, **kwargs)
    final_results = []

    # print('video search results length: ', len(results))
    for item in results:
        video_id = item['id']['videoId']
        title = item['snippet']['title']

        comments = get_video_comments(service,
                                      part='snippet,replies',
                                      videoId=video_id,
                                      textFormat='plainText')
        comments = [comment['textDisplay'] for comment in comments]

        final_results.extend([(video_id, title, cmnt) for cmnt in comments])

    write_to_csv(final_results)


def write_to_csv(comments):
    with open('comments.csv', 'w') as comments_file:
        comments_writer = csv.writer(comments_file,
                                     delimiter=',',
                                     quotechar='"',
                                     quoting=csv.QUOTE_MINIMAL)
        comments_writer.writerow(['VideoID', 'Title', 'Comment'])
        for row in comments:
            comments_writer.writerow(list(row))


def main():
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    keyword = input('Enter a keyword: ')
    search_videos_by_keyword(service, q=keyword, part='id,snippet',
                             eventType='completed', type='video')


if __name__ == '__main__':
    main()
