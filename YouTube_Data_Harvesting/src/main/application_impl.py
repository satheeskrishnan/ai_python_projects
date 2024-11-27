import os
import sys
import traceback
import pandas as pd
from config_parser import ConfigParserWrapper
from youtube_api import YouTubeAPI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from util.db_util import MySqlDBUtil
from util.yt_exception import YouTubeException

class ConfigurationData:
    def __init__(self, filename='config.ini'):
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script
        config_path = os.path.abspath(os.path.join(current_dir, '..', '..', 'resource', filename))
        self.config = ConfigParserWrapper(config_path)

    def load_config(self):
        self.resync_all = self.config.get_boolean('globlal', 'reSyncAll')
        self.developer_key = self.config.get('globlal', 'developerKey')

        self.db_host = self.config.get('database', 'host')
        self.db_user = self.config.get('database', 'user')
        self.db_password = self.config.get('database', 'password')
        self.db_name = self.config.get('database', 'dbName')

        self.channel_Ids = self.config.get_list('channel', 'channelIds')
        self.channel_parts = self.config.get('channel', 'parts')
        self.channel_coloumns_renames= self.config.get_dict('channel', 'propertiesRenameAndFilter')
        self.channel_coloumns_filters = self.config.get_list_from_key_value_pairs('channel', 'propertiesRenameAndFilter',1)

        self.playList_parts = self.config.get('playList', 'parts')
        self.playList_coloumns_renames= self.config.get_dict('playList', 'propertiesRenameAndFilter')
        self.playList_coloumns_filters = self.config.get_list_from_key_value_pairs('playList', 'propertiesRenameAndFilter',1)

        self.playListItem_parts = self.config.get('playListItems', 'parts')
        self.playListItem_coloumns_renames= self.config.get_dict('playListItems', 'propertiesRenameAndFilter')
        self.playListItem_coloumns_filters = self.config.get_list_from_key_value_pairs('playListItems', 'propertiesRenameAndFilter',1)

        self.videos_parts = self.config.get('videos', 'parts')
        self.videos_coloumns_renames= self.config.get_dict('videos', 'propertiesRenameAndFilter')
        self.videos_coloumns_filters = self.config.get_list_from_key_value_pairs('videos', 'propertiesRenameAndFilter',1)

        self.comments_parts = self.config.get('comments', 'parts')
        self.comments_coloumns_renames= self.config.get_dict('comments', 'propertiesRenameAndFilter')
        self.comments_coloumns_filters = self.config.get_list_from_key_value_pairs('comments', 'propertiesRenameAndFilter',1)
        self.comments_max_results = self.config.get_int('comments', 'maxResults')

class ApplicationImpl(ConfigurationData):
    def __init__(self, filename='config.ini'): 
        super().__init__(filename)
        self.load_config()
        self.yt_api = YouTubeAPI(self.developer_key)

    def main(self):
        channel_df = pd.DataFrame()
        chennel_response_list = []
        for channel_id in self.channel_Ids:
            chennal_response = self.yt_api.get_channel_details(channel_id, self.channel_parts)
            filtered_df = self.filter_response(chennal_response, self.channel_coloumns_renames, self.channel_coloumns_filters)
            chennel_response_list.append(filtered_df)
        channel_df = pd.concat(chennel_response_list)
        return channel_df
        
    def process_channel_info(self, channel_id):
        response = self.yt_api.get_channel_details(channel_id, self.channel_parts)
        filtered_df = self.filter_response(response, self.channel_coloumns_renames, self.channel_coloumns_filters)
        return filtered_df
    
    def process_playlist_info(self, channel_id):
        response = self.yt_api.get_playlist_details(channel_id, self.playList_parts)
        filtered_df = self.filter_response(response, self.playList_coloumns_renames, self.playList_coloumns_filters)
        return filtered_df
    
    def process_playlist_item_info(self, playlist_id):
        response = self.yt_api.get_playlist_items_details(playlist_id, self.playListItem_parts)
        filtered_df = self.filter_response(response, self.playListItem_coloumns_renames, self.playListItem_coloumns_filters)
        return filtered_df
    
    def process_video_info(self, video_ids):
        response = self.yt_api.get_video_details(video_ids, self.videos_parts)
        filtered_df = self.filter_response(response, self.videos_coloumns_renames, self.videos_coloumns_filters)
        return filtered_df 
    
    def process_comments_info(self, video_id):
        response = self.yt_api.get_comments_details(video_id, self.comments_parts, self.comments_max_results)
        filtered_df = self.filter_response(response, self.comments_coloumns_renames, self.comments_coloumns_filters)
        return filtered_df
    
    def filter_response(self, response,columns,filtered_columns):
        try:
            
            df = pd.json_normalize(response,['items'], errors='ignore')
            df = df.rename(columns=columns)
            filtered_df = df[filtered_columns]
            return filtered_df
        except Exception:
            raise YouTubeException("Invalid input",400)
    
    def get_data(self, query):
        pre_defined_queries = {
            "option_1": "select C.channel_name, V.video_name from Channels C join Playlists P  ON C.channel_id = P.channel_id join Videos V ON P.playlist_id = V.playlist_id ORDER BY C.channel_name, V.video_name;",
            "option_2": "select C.channel_name, COUNT(V.video_id) AS video_count from Channels C join Playlists P  ON C.channel_id = P.channel_id join Videos V ON P.playlist_id = V.playlist_id GROUP BY C.channel_name ORDER BY video_count DESC LIMIT 1;",
            "option_3": "select C.channel_name, V.video_id, V.view_count from Channels C join Playlists P ON C.channel_id = P.channel_id join Videos V ON P.playlist_id = V.playlist_id ORDER BY V.view_count DESC LIMIT 10;"
            }
        
        db = MySqlDBUtil(self.db_host, self.db_user, self.db_password, self.db_name)
        data = db.execute_select(pre_defined_queries[query])
        return data
    def save_data(self, data, table_name):
        db = MySqlDBUtil(self.db_host, self.db_user, self.db_password, self.db_name)
        db.insert_or_update(data, table_name)
