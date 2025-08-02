import os
from dotenv import load_dotenv
from googleapiclient.discovery import build


class VideoService:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("YOUTUBE_API_KEY")

        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def get_video(self, topic) -> str:
        search_response = self.youtube.search().list(
            q=f"{topic} educational kids",
            part='snippet',
            maxResults=5,
            type='video',
            videoDuration='short',  # Under 4 minutes
            safeSearch='strict',
            relevanceLanguage='en'
        ).execute()

        if search_response['items']:
            video_id = search_response['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"

        return None