
import time
import pandas as pd
import streamlit as st
from application_impl import ApplicationImpl
from util.yt_exception import YouTubeException

class FeatureOneUI:
    def __init__(self, appImpl):
        self.app = appImpl

    # Function to display the about page
    def show_feature(self):
        st.markdown("""
            ## Feature 1
            Ability to input a YouTube channel ID and retrieve all the relevant data (Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of each video) using Google API.
            
        """)
        st.markdown(f"""
        <style>
        .stButton>button {{
            background-color: green;
            color: white;
            border: none;
            padding: 10px 24px;
            text-align: center;
            text-decoration: none;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }}
        .stButton>button:hover {{
            background-color: darkgreen;
            color: white;
        }}
        .stTextInput>div>div>text_input {{
                background-color: #f0f230f0; 
                color: #000000;
                border: 10px solid #ccc;
            }}
        </style>
        """, unsafe_allow_html=True)

        # Input field with a caption
        user_input_chennel_id = st.text_input("Enter Channel ID", placeholder="Channel ID...")
        if "button_submit_clicked" not in st.session_state:
            st.session_state.button_save_clicked = True
            st.session_state.button_submit_clicked = False
            

        if "button_save_clicked" not in st.session_state:
            st.session_state.button_submit_clicked = True
            st.session_state.button_save_clicked = False

        if "channel_df" not in st.session_state:
            st.session_state.channel_df =  None
        
        if "play_list_df" not in st.session_state:
            st.session_state.play_list_df =  None
        
        if "video_df" not in st.session_state:
            st.session_state.video_df =  None
        
        if "comments_df" not in st.session_state:
            st.session_state.comments_df =  None

        channel_df =  None
        play_list_df = None
        play_list_items_df = None
        video_df = None
        comments_df = None

        
        message_placeholder = st.empty()

        # Submit button
        if st.session_state.button_save_clicked:
            
            if st.button("Submit", icon=":material/done:"):
                exception = False
                if user_input_chennel_id:
                    with message_placeholder:
                        st.success(f"Processing... Please wait....")
                        st.session_state.button_submit_clicked = True
                        st.session_state.button_save_clicked = False 
                    self.app.load_config()
                    channel_ids = user_input_chennel_id.split(',')
                    try:
                        channel_df_list =[self.app.process_channel_info(channel_id) for channel_id in channel_ids]
                        channel_df = pd.concat(channel_df_list,ignore_index=True)
                        st.session_state.channel_df = channel_df
                        print(f"channel_df: {channel_df}")
                    except YouTubeException as e:
                        exception = True
                        with message_placeholder:
                            st.error(f"Unable to get the Channel info with Channel ID : '{user_input_chennel_id}': {str(e.args[0])}")
                    if not exception:
                        try:
                            playlist_df_list = [self.app.process_playlist_info(channel_id) for channel_id in channel_ids]
                            play_list_df = pd.concat(playlist_df_list,ignore_index=True)
                            st.session_state.play_list_df = play_list_df
                            print(f"play_list_df: {play_list_df}")
                        except YouTubeException as e:
                            with message_placeholder:
                                st.error(f"Unable to get the Playlist info with Channel ID : '{user_input_chennel_id}': {str(e.args[0])}")
                                st.session_state.button_save_clicked = True
                        
                        try:
                            play_list_items_list = [self.app.process_playlist_item_info(playlist_id) for playlist_id in play_list_df['playlist_id']]
                            play_list_items_df = pd.concat(play_list_items_list,ignore_index=True)
                            video_df = pd.merge(play_list_items_df, self.app.process_video_info(play_list_items_df['video_id'].tolist()), how='inner', on='video_id')
                            video_df["published_date"] = pd.to_datetime(video_df["published_date"], format="%Y-%m-%dT%H:%M:%SZ").dt.strftime("%Y-%m-%d %H:%M:%S")
                            st.session_state.video_df = video_df
                            
                        except YouTubeException as e:
                            with message_placeholder:
                                st.error(f"Unable to get the Video info with Channel ID : '{user_input_chennel_id}' : {str(e.args[0])}")
                        
                        try:
                            comments_list = [self.app.process_comments_info(vid_id) for vid_id in video_df['video_id']]
                            comments_df = pd.concat(comments_list,ignore_index=True)
                            comments_df["comment_published_date"] = pd.to_datetime(comments_df["comment_published_date"], format="%Y-%m-%dT%H:%M:%SZ").dt.strftime("%Y-%m-%d %H:%M:%S")
                            st.session_state.comments_df = comments_df
                        except YouTubeException as e:
                            with message_placeholder:
                                st.error(f"Unable to get the Comments info with Channel ID : '{user_input_chennel_id}': {str(e.args[0])}")
                       
                    
                else:
                    with message_placeholder:
                        st.error("Please enter a value before submitting.")

        # Save button
        if st.session_state.button_submit_clicked:
            
            with message_placeholder:
                st.success("Data fetched successfully")
                st.session_state.button_save_clicked = True
            if st.button("Save Below Details",icon=":material/save:"):
                if st.session_state.channel_df is not None:
                    channel_df = st.session_state.channel_df
                    self.app.save_data(channel_df, "Channels")

                if st.session_state.play_list_df is not None:
                    play_list_df = st.session_state.play_list_df
                    self.app.save_data(play_list_df, "Playlists")

                if st.session_state.video_df is not None:
                    video_df = st.session_state.video_df
                    self.app.save_data(video_df, "Videos")

                if st.session_state.comments_df is not None:
                    comments_df = st.session_state.comments_df
                    self.app.save_data(comments_df, "Comments")

                with message_placeholder:
                    st.success("Data Saved Successfully")
                st.session_state.button_submit_clicked = False 
                

        if channel_df is not None:
            st.markdown(
                '<p style="color:darkblue;">Channel Details</p>',
                unsafe_allow_html=True
            )
            st.dataframe(channel_df, width=1100)
            st.session_state.button_save_clicked = True

        if play_list_df is not None:
            st.markdown(f'<p style="color:darkblue;">PlayList Count: <span style="color:blue;">{len(play_list_df)}</span></p>', unsafe_allow_html=True)
            st.dataframe(play_list_df, width=1100, height=200)

        if video_df is not None:
            st.markdown(f'<p style="color:darkblue;">Video Count: <span style="color:blue;">{len(video_df)}</span></p>', unsafe_allow_html=True)
            st.dataframe(video_df, width=1100, height=300)

        if comments_df is not None:
            st.markdown(f'<p style="color:darkblue;">Comments Count: <span style="color:blue;">{len(comments_df)}</span></p>', unsafe_allow_html=True)
            st.dataframe(comments_df, width=1100, height=300)
        
