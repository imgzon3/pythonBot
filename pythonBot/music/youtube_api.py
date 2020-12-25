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

    videoId = ''
    search_response = youtube.search().list(
        q=a,
        part="snippet",
        maxResults=5
    ).execute()

    # 채널: id의 kind는 youtube#channel, 주소는 channelId
    # 영상: id의 kind는 youtube#video, 주소는 videoId
    # 플레이 리스트 : id의 kind는 youtube#playlist, 주소는 playlistId
    for search_result in search_response['items']:
        if search_result['id']['kind'] == 'youtube#video':
            videoId = search_result['id']['videoId']
            break
    print('[api]Url Search complete')
    # print("https://youtu.be/"+videoId)
    # print(videoId)

    # 검색결과가 없거나 상위 5개 목록에 영상이 없을 경우
    if videoId == '':
        return ''
    else:
        videoId = "https://youtu.be/"+videoId
        return videoId
