import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from googleapiclient.discovery import build
import pandas as pd
from util.yt_exception import YouTubeException


class YouTubeAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def get_channel_details(self, channel_id, configured_part):
        request = self.youtube.channels().list(
            part=configured_part,
            id=channel_id
        )
        response = request.execute()
        return response

    def get_playlist_details(self, channel_id, configured_part):
        request = self.youtube.playlists().list(
            part=configured_part,
            channelId=channel_id
        )
        response = request.execute()
        return response
    
    def get_playlist_items_details(self, playlist_id, configured_part):
        request = self.youtube.playlistItems().list(
            part=configured_part,
            playlistId=playlist_id
        )
        response = request.execute()
        return response
    
    def get_video_details(self, video_ids, configured_part):
        str_video_ids = ','.join(list(map(str, video_ids)))
        request = self.youtube.videos().list(
            part=configured_part,
            id=str(str_video_ids)
        )
        response = request.execute()
        return response
    
    def get_comments_details(self, video_id, configured_part, max_results):
        request = self.youtube.commentThreads().list(
            part=configured_part,
            videoId=video_id,
            maxResults=max_results
        )
        response = request.execute()
        return response