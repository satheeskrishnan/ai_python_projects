import streamlit as st
from application_impl import ApplicationImpl

class FeatureTwoUI:
    def __init__(self, appImpl):
        self.app = appImpl
    def show_feature(self):
        st.markdown("""
            ## Feature 2
            Ability to search and retrieve data from the database using different search options, including joining tables to get channel detail.
        """)
        options = [
            "--Select the query--",
            "1. What are the names of all the videos and their corresponding channels?", 
            "2. Which channels have the most number of videos, and how many videos do they have?", 
            "3. What are the top 10 most viewed videos and their respective channels ?",
            "4. How many comments were made on each video, and what are their corresponding video ids?",
            "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
            "6. What is the total number of likes and dislikes for each video, and what are their corresponding video ids?",
            "7. What is the total number of views for each channel, and what are their corresponding channel names?",
            "8. What are the names of all the channels that have published videos in the year 2022?",
            "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
            "10.Which videos have the highest number of comments, and what are their corresponding channel names?"
        ]

        # Create a dropdown
        selected_option = st.selectbox("Choose an option:", options)

        # "On-select" event: Perform an action based on the selection
        if selected_option == "1. What are the names of all the videos and their corresponding channels?":
            st.write("1. What are the names of all the videos and their corresponding channels?")
            st.dataframe(self.app.get_data("option_1"), width=800)
        elif selected_option == "2. Which channels have the most number of videos, and how many videos do they have?":
            st.dataframe(self.app.get_data("option_2"), width=800)
        elif selected_option == "3. What are the top 10 most viewed videos and their respective channels ?":
            st.dataframe(self.app.get_data("option_3"), width=800)
        elif selected_option == "4. How many comments were made on each video, and what are their corresponding video ids?":    
            st.write("4. How many comments were made on each video, and what are their corresponding video ids?")
        elif selected_option == "5. Which videos have the highest number of likes, and what are their corresponding channel names?":
            st.write("5. Which videos have the highest number of likes, and what are their corresponding channel names?")
        elif selected_option == "6. What is the total number of likes and dislikes for each video, and what are their corresponding video ids?":
            st.write("6. What is the total number of likes and dislikes for each video, and what are their corresponding video ids?")
        elif selected_option == "7. What is the total number of views for each channel, and what are their corresponding channel names?":
            st.write("7. What is the total number of views for each channel, and what are their corresponding channel names?")
        elif selected_option == "8. What are the names of all the channels that have published videos in the year 2022?":
            st.write("8. What are the names of all the channels that have published videos in the year 2022?")
        elif selected_option == "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?":
            st.write("9. What is the average duration of all videos in each channel, and what are their corresponding channel names?")
        elif selected_option == "10.Which videos have the highest number of comments, and what are their corresponding channel names?":
            st.write("10.Which videos have the highest number of comments, and what are their corresponding channel names?")
        else:
            st.write("select any one option")