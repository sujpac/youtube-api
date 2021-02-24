from googleapiclient.discovery import build
import json
import re
import os


def main(playlist_id=None):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_key = os.environ.get('YT_API_KEY')
    api_service_name = 'youtube'
    api_version = 'v3'

    if not playlist_id:
        # (Hardcoded) example playlist from Khan Academy
        # youtube.com/playlist?list=PLSQl0a2vh4HCNiooUekZDy0LEfhikAu3Z
        playlist_id = 'PLSQl0a2vh4HCNiooUekZDy0LEfhikAu3Z'

    youtube = build(api_service_name, api_version, developerKey=api_key)

    kwargs = {'part': 'snippet,contentDetails', 'playlistId': playlist_id}
    request = youtube.playlistItems().list(**kwargs)
    response = request.execute()

    def pretty_print(x):
        print(json.dumps(x, indent=4, sort_keys=False))

    # pretty_print(response)

    vid_ids = []

    while response:
        vid_ids.extend([item['contentDetails']['videoId']
                        for item in response['items']])

        if 'nextPageToken' not in response:
            break

        kwargs['pageToken'] = response['nextPageToken']
        response = youtube.playlistItems().list(**kwargs).execute()

    kwargs = {'part': 'contentDetails', 'id': ','.join(vid_ids)}
    vid_response = youtube.videos().list(**kwargs).execute()

    # pretty_print(vid_response)

    vid_durations = [item['contentDetails']['duration']
                     for item in vid_response['items']]

    # print(vid_durations)
    # Duration of 'PT7M55S' means 7 minutes & 55 seconds
    # Note that there could be an hours digit with an 'H'

    hours_pattern = re.compile(r'(\d+)H')
    minutes_pattern = re.compile(r'(\d+)M')
    seconds_pattern = re.compile(r'(\d+)S')

    total_second_counts = []

    for duration in vid_durations:
        # print(duration)
        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)
        # print(hours, minutes, seconds)
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0
        # print(hours, minutes, seconds, '\n\n')
        # print(type(minutes))
        total_second_counts.append(hours*3600 + minutes*60 + seconds)

    tsecs = sum(total_second_counts)
    hours, minutes, seconds = tsecs // 3600, (tsecs % 3600) // 60, tsecs % 60
    avg_dur = tsecs // len(vid_ids)

    pl_res = youtube.playlists().list(part='snippet', id=playlist_id).execute()
    pl_title = pl_res['items'][0]['snippet']['title']

    print('Playlist title:', pl_title)
    print('Number of videos:', len(vid_ids))
    print('Total duration:', hours, 'H', minutes, 'M', seconds % 60, 'S')
    print('Average video duration:', avg_dur // 60, 'M', avg_dur % 60, 'S')


if __name__ == '__main__':
    print('Enter a YouTube playlist ID: ', end='')
    playlist_id = input().strip(' ')

    main(playlist_id)
