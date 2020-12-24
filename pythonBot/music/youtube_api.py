from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def search_youtube(a):
    file = open("../../../privateStuff/youtube_api.txt", 'r')

    lines = file.readlines()
    DEVELOPER_KEY = lines[0]  # 토큰 값

    file.close()

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    print('[api]Searching url...')

    search_response = youtube.search().list(
        q=a,
        order="date",
        part="snippet",
        maxResults=1
    ).execute()

    for search_result in search_response['items']:
        videoId = search_result['id']['videoId']
    print('[api]Url Search complete')
    # print("https://youtu.be/"+videoId)
    # print(videoId)
    return "https://youtu.be/"+videoId
