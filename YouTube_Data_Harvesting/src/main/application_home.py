
import streamlit as st
from ui_feature_1 import FeatureOneUI 
from ui_feature_2 import FeatureTwoUI
from  application_impl import ApplicationImpl

class ApplicationHome:
    def __init__(self):
        st.set_page_config(page_title="YouTube Data Harvesting and Warehousing", layout="wide")
        # Page navigation
        st.sidebar.title("Navigation")
        self.page = st.sidebar.radio("Go to", ["Home", "Feature 1", "Feature 2"])
        self.appImpl = ApplicationImpl('config.ini')
        

    # Function to display the home page
    def show_home(self):
        st.title("Welcome to the YouTube Data Harvesting and Warehousing")
        st.markdown("""
            ## Problem Statement
            Application that allows users to access and analyze data from multiple YouTube channels. The application should have the following features:
            
            ### Features
            -  1: Ability to input a YouTube channel ID and retrieve all the relevant data (Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of each video) using Google API.
            -  2: Ability to search and retrieve data from the database using different search options, including joining tables to get channel detail
            -  3: Ability to collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button.
            -  4: Ability to retrieve data from the data lake and display it in a table.
        """
        )

    def main(self):
        feature_1 = FeatureOneUI(self.appImpl)
        feature_2 = FeatureTwoUI(self.appImpl)
        if self.page == "Home":
            self.show_home()
        if self.page == "Feature 1":
            feature_1.show_feature()
        elif self.page == "Feature 2":
            feature_2.show_feature()


if __name__ == "__main__":
    app = ApplicationHome()
    app.main()

    
