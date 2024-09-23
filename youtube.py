import streamlit as st
import time
import streamlit_option_menu
from streamlit_option_menu import option_menu
from googleapiclient.discovery import build
import isodate
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.graph_objects as go



#API CONNECTION KEY

import googleapiclient.discovery
api_service_name = "youtube"
api_version = "v3"
api_key='AIzaSyBYzLJKBL5myPnNPUj8OCrr6RlsWM2P20s'
youtube = googleapiclient.discovery.build(api_service_name, api_version,developerKey=api_key)



#MYSQL DATABASE
import mysql.connector         
mydb = mysql.connector.connect(host="localhost",user="root",password="",)
print(mydb)
mycursor = mydb.cursor(buffered=True)


#TABLE CREATIONS:

#CHANNEL DETAILS TABLE
mycursor.execute('CREATE TABLE IF NOT EXISTS youtube.channel_data(channel_id VARCHAR(50) PRIMARY KEY ,channel_name VARCHAR(50),channel_des VARCHAR(50),channel_pid VARCHAR(50),channel_sub VARCHAR(50),channel_vc VARCHAR(50),channel_vic VARCHAR(50))')

#VIDEO DETAILS TABLE
mycursor.execute('CREATE TABLE IF NOT EXISTS youtube.videos_data(channel_Name VARCHAR(100),channel_id VARCHAR(50),video_Id VARCHAR(50),Title VARCHAR(50),Thumbnail VARCHAR(255),Description TEXT, published_date DATETIME, Views INT,Likes INT,Dislikes INT,viewcount BIGINT,likecount BIGINT,CommentCount BIGINT,Definition VARCHAR(255),Caption_Status VARCHAR(255),Duration VARCHAR(255),Duration_Seconds VARCHAR(255))')

#COMMENT DETAILS TABLE
mycursor.execute('CREATE TABLE IF NOT EXISTS youtube.comment_detail(Comment_Id VARCHAR(100),Video_Id VARCHAR(100),Comment_text TEXT,Comment_Auth TEXT,Comment_publishedAt TEXT)')



#GET CHANNEL DETAILS

def channel_data(channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()

    data= {     
                'channel_id': response['items'][0]['id'],
                'channel_name':response['items'][0]['snippet']['title'],

                'channel_des':response['items'][0]['snippet']['description'],

                'channel_pid':response['items'][0]['contentDetails']['relatedPlaylists']['uploads'],

                'channel_sub':response['items'][0]['statistics']['subscriberCount'],


                'channel_vc':response['items'][0]['statistics']['viewCount'],
            
                'channel_vic':response['items'][0]['statistics']['videoCount']


    }
    return data


#VIDEO IDS
def get_video_ids(channel_id):
        video_ids=[]
        response = youtube.channels().list(id=channel_id,
                        part="contentDetails").execute()
        

        channel_pid=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        

        next_page_token=None
        
        while True:
                response1= youtube.playlistItems().list(
                        part="snippet",
                        playlistId=channel_pid,
                        maxResults=50,
                        pageToken=next_page_token).execute()
        
        

                for i in range (len(response1['items'])):
                     video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
                next_page_token=response1.get('nextPageToken')

                if next_page_token is None:
                    break
                
        return video_ids


#VIDEO DETAILS
#get video data
import datetime
import isodate

def get_video_info(video_ids):
    video_data = []

    for video_id in video_ids:
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        for item in response['items']:
            try:
                published_at = datetime.datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                published_at = None  # Handle invalid date format

            data = {
                'channel_Name': item['snippet']['channelTitle'],
                'channel_id': item['snippet']['channelId'],
                'video_Id': item['id'],
                'Title': item['snippet']['title'],
                'Thumbnail': item['snippet']['thumbnails']['default']['url'],  
                'Description': item['snippet'].get('description'),
                "published_date":item['snippet']['publishedAt'],
                'Views': int(item['statistics'].get('viewCount',0)),
                'Likes': int(item['statistics'].get('likeCount', 0)),
                'Dislikes': int(item['statistics'].get('dislikeCount', 0)),
                'viewcount':item['statistics'].get('viewCount',0),
                'likecount':item['statistics'].get('likeCount',0),
                'CommentCount': item['statistics'].get('commentCount', 0),
                'Definition': item['contentDetails']['definition'],
                'Caption_Status': item['contentDetails']['caption'],
                'Duration': item['contentDetails']['duration'], 
                'Duration_Seconds': duration_to_seconds(item['contentDetails']['duration'])
            }
            video_data.append(data)
    return video_data
def duration_to_seconds(duration):
    duration = isodate.parse_duration(duration)
    hours = duration.days * 24 + duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds




#GET COMMENT DETAILS

#get video info
def get_comment_info(video_ids):
    Comment_data=[]

    try:
            for video_id in video_ids:

                request = youtube.commentThreads().list(
                    part="snippet",
                    maxResults=100,
                    videoId=video_id
                )
            response = request.execute()

            for item in response['items']:
                data=dict(Comment_Id=item['snippet']['topLevelComment']['id'],
                        Video_Id=item['snippet']['topLevelComment']['snippet']['videoId'], 
                        Comment_text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                        Comment_Auth=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        Comment_publishedAt=item['snippet']['topLevelComment']['snippet']['publishedAt']
                        )
                Comment_data.append(data)
    except:
        pass
    return Comment_data

        


#STREAMLIT PART
with st.sidebar:
        selected = option_menu(None,["HOME","FETCH DATA","VIEW"], 
                                icons=["house-door-fill","tools","card-text"],
                                default_index=0,
                                orientation="vertical",
                                styles={"nav-link": {"font-size": "20px", "text-align": "centre", "margin": "0px", 
                                        "--hover-color": "#C80101"},
                                        "icon": {"font-size": "20px"},
                                        "container" : {"max-width": "4000px"},
                                        "nav-link-selected": {"background-color": "#C80101"}})
        

if selected == 'HOME':
        st.title(':red[YOUTUBE DATA HARVESTING]')
        

        st.title(':blue[OVERVIEW]')
        st.write("Youtube Data harvesting is to collect the data from the Youtube API and store it in a SQL database. It enables users to search for channel details and join tables to view data in the Streamlit app.")

        st.title(':yellow[TECHNOLOGIES]')
        st.write("The project utilizes various technologies including YouTube API for data retrieval, Python Scripting to fetch the particular data through documents, Streamlit for creating the user interface, Pandas for data manipulation, MySQL for database management, and API integration for connecting to external services.")


# Fetch Data from Database and calling the function

def main():

        if selected=='FETCH DATA':

                channel_id = st.text_input("Enter your channel id here:")

                if st.button("Click Me ") and channel_id:
                        try:
                                
                                
                                c1 =channel_data(channel_id)
                                channel_df=pd.DataFrame(c1,index=[0])
                                channel_data_query = "INSERT INTO youtube.channel_data (channel_id, channel_name,channel_des,channel_pid, channel_sub, channel_vc, channel_vic) VALUES (%s, %s, %s, %s, %s,%s,%s)"
                                c1_tuple= tuple(c1.values())
                                mycursor.execute(channel_data_query, c1_tuple)
                                mydb.commit()
                                st.write(channel_df)
                        
                                #fetch video_id
                                video_Ids= get_video_ids(channel_id)
                                
                                # Fetch video details
                                video_details = get_video_info(video_Ids)
                                video_df=pd.DataFrame(video_details)
                                
                                for row in video_details:
                                        vd=(' INSERT INTO youtube.videos_data (channel_Name,channel_id,video_Id,Title,Thumbnail,Description,published_Date,Views,Likes,Dislikes,viewcount,likecount,CommentCount,Definition,Caption_Status,Duration,Duration_Seconds) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
                                        values= tuple(row.values())
                                        mycursor.execute( vd, values)
                                        mydb.commit()

                                #fetch comment details
                                comment_details=get_comment_info(video_Ids)
                                comments_df=pd.DataFrame(comment_details)

                                for row in comment_details:
                                        t = ('INSERT INTO youtube.comment_detail(Comment_Id,Video_Id ,Comment_text,Comment_Auth,Comment_publishedAt) VALUES(%s,%s,%s,%s,%s)')
                                        values=tuple(row.values())
                                        mycursor.execute(t,values)
                                        mydb.commit()


                                with st.spinner('Wait for it...'):
                                        time.sleep(5)
                                
                                st.success('Data was migrated and fetched successfully', icon="✅")
                        except:
                                st.warning(' channel dat already exists')
if __name__ == "__main__":
        main()

if selected=='VIEW':

        st.write("## :RED[QUESTIONS FOR STREAMLIT]")

        mycursor.execute("use youtube")


        Question = st.selectbox('Choose any one of the Questions',('---Select any Question----',
        '1.What are the names of all the videos and their corresponding channels?',
        '2.Which channels have the most number of videos, and how many videos do they have?',
        '3.What are the top 10 most viewed videos and their respective channels?',
        '4.How many comments were made on each video, and what are their corresponding video names?',
        '5.Which videos have the highest number of likes, and what are their corresponding channel names?',
        '6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
        '7.What is the total number of views for each channel, and what are their corresponding channel names?',
        '8.What are the names of all the channels that have published videos in the year 2022?',
        '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?',
        '10.Which videos have the highest number of comments, and what are their corresponding channel names?'))

        if Question=='1.What are the names of all the videos and their corresponding channels?':
                mycursor.execute('SELECT videos_data.title AS VideoTitle, channel_data.channel_name AS ChannelName FROM videos_data INNER JOIN channel_data ON videos_data.channel_id = channel_data.channel_id;')
                qn1=mycursor.fetchall()
                df1=pd.DataFrame(qn1,columns=["VideoName","ChannelName"])
                st.write(df1)
                fig = go.Figure(data=[go.Bar(x=df1['VideoName'], y=df1['ChannelName'], text=df1['ChannelName'],
                                        marker=dict(color='yellow'),
                                        hovertemplate='%{x}<br>Video Count: %{y}')])
                fig.update_layout(title='Corresponding Channels', xaxis_title='VideoName', yaxis_title='VideoName')
                st.plotly_chart(fig)
        
        elif Question=='2.Which channels have the most number of videos, and how many videos do they have?':
                mycursor.execute("""SELECT channel_name as ChannelName,channel_vic as VideoCount FROM channel_data ORDER BY VideoCount DESC""")
                qn2=mycursor.fetchall()
                df2=pd.DataFrame(qn2,columns=["ChannelName","VideoCount"])
                st.write(df2)
                fig = go.Figure(data=[go.Bar(x=df2['ChannelName'], y=df2['VideoCount'], text=df2['ChannelName'],
                                        marker=dict(color='red'),
                                        hovertemplate='%{x}<br>Video Count: %{y}')])
                fig.update_layout(title='Top Channels by Video Count', xaxis_title='Channel Name', yaxis_title='Video Count')
                st.plotly_chart(fig)

        elif Question=='3.What are the top 10 most viewed videos and their respective channels?':
                mycursor.execute(''' SELECT videos_data.Title AS VideoTitle,videos_data.viewcount AS VideoViewCount,channel_data.channel_name AS ChannelName FROM videos_data JOIN channel_data ON videos_data.Channel_id = channel_data.channel_id ORDER BY videos_data.viewcount DESC LIMIT 10;''')
                qn3=mycursor.fetchall() 
                df3=pd.DataFrame(qn3,columns=["VideoTitle","VideoViewCount","ChannelName"])
                st.write(df3)
                fig = go.Figure(data=[go.Bar( x=df3['VideoTitle'],y=df3['VideoViewCount'],text=df3['VideoTitle'],
                        marker=dict(color='orange'),
                        hovertemplate='%{x}<br>Video Count: %{y}')])
                fig.update_layout(title='top 10 most viewed videos and their respective channels', xaxis_title='VideoTitle', yaxis_title='VideoViewCount')
                st.plotly_chart(fig)

        
        elif Question=='4.How many comments were made on each video, and what are their corresponding video names?':
                mycursor.execute("""SELECT videos_data.CommentCount AS CommentCount,videos_data.Title as VideoName FROM videos_data ORDER BY CommentCount desc""")
                qn4=mycursor.fetchall()
                df4=pd.DataFrame(qn4,columns=["CommentCount","VideoName"])
                st.write(df4)
                fig = go.Figure(data=[go.Bar(x=df4['CommentCount'], y=df4['VideoName'], text=df4['CommentCount'],
                                        marker=dict(color='brown'),
                                        hovertemplate='%{x}<br>Video Count: %{y}')])
                fig.update_layout(title='their corresponding video names', xaxis_title='CommentCount', yaxis_title='VideoName')
                st.plotly_chart(fig)
                


        elif Question=='5.Which videos have the highest number of likes, and what are their corresponding channel names?':

                mycursor.execute("""SELECT Title AS ChannelName, MAX(likecount) AS VideoLikeCount 
                FROM videos_data INNER JOIN channel_data ON channel_data.channel_id = videos_data.channel_id GROUP BY channel_data.channel_name ORDER BY VideoLikeCount DESC;""")
                qn5=mycursor.fetchall()
                df5=pd.DataFrame(qn5,columns=["ChannelName","VideoLikeCount"])
                st.write(df5)
                fig = go.Figure(data=[go.Bar(x=df5['ChannelName'], y=df5['VideoLikeCount'], text=df5['ChannelName'],
                                        marker=dict(color='red'),
                                        hovertemplate='%{x}<br>VideoLikeCount: %{y}')])
                fig.update_layout(title='Top Channels by Video Count', xaxis_title='Channel Name', yaxis_title='VideoLikeCount')
                st.plotly_chart(fig)


        elif Question=='6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
                mycursor.execute("""SELECT Title as VideoNames, likecount AS TotalLikes FROM videos_data ORDER BY TotalLikes DESC;""")
                qn6=mycursor.fetchall()
                df6=pd.DataFrame(qn6,columns=["VideoNames","TotalLikes"])
                st.write(df6)
                fig = go.Figure(data=[go.Bar(x=df6['VideoNames'], y=df6['TotalLikes'], text=df6['TotalLikes'],
                                        marker=dict(color='pink'),
                                        hovertemplate='%{x}<br>TotalLikes: %{y}')])
                fig.update_layout(title='Channels likes and dislikes', xaxis_title='VideoNames', yaxis_title='TotalLikes')
                st.plotly_chart(fig)

        elif Question=='7.What is the total number of views for each channel, and what are their corresponding channel names?':
                mycursor.execute("""SELECT channel_name as ChannelNames, channel_vc AS Total_Views FROM channel_data ORDER BY Total_Views DESC;""")
                qn7=mycursor.fetchall()
                df7=pd.DataFrame(qn7,columns=["ChannelName","Total_Views"])
                st.write(df7)
                fig = go.Figure(data=[go.Bar(x=df7['ChannelName'], y=df7['Total_Views'], text=df7['Total_Views'],
                                        marker=dict(color='yellow'),
                                        hovertemplate='%{x}<br>Total_Views: %{y}')])
                fig.update_layout(title='Views of Corresponding Channels', xaxis_title='ChannelName', yaxis_title='Total_Views')
                st.plotly_chart(fig)

        elif Question=='8.What are the names of all the channels that have published videos in the year 2022?':
                mycursor.execute("""SELECT channel_data.channel_name AS ChannelName,videos_data.published_date AS VideoPublishDate 
                FROM videos_data JOIN channel_data ON channel_data.channel_id = videos_data.channel_id WHERE YEAR(videos_data.published_date) = 2022""")
                qn8=mycursor.fetchall()
                df8=pd.DataFrame(qn8,columns=["ChannelName","VideoPublishDate"])
                st.write(df8)
                fig = go.Figure(data=[go.Bar(x=df8['ChannelName'], y=df8['VideoPublishDate'], text=df8['VideoPublishDate'],
                                        marker=dict(color='violet'),
                                        hovertemplate='%{x}<br>VideoPublishDate: %{y}')])
                fig.update_layout(title='videos of channels that published in given year', xaxis_title='ChannelName', yaxis_title='VideoPublishDate')
                st.plotly_chart(fig)

        elif Question=='9.What is the average duration of all videos in each channel, and what are their corresponding channel names?':
                mycursor.execute("""SELECT channel_data.Channel_name, AVG(videos_data.Duration_Seconds) AS VideoDurationSeconds FROM videos_data JOIN channel_data ON channel_data.channel_id = videos_data.channel_id GROUP BY channel_name""")
                qn9=mycursor.fetchall()
                df9=pd.DataFrame(qn9,columns=["ChannelName","VideoDurationSeconds"])
                st.write(df9)
                fig = go.Figure(data=[go.Bar(x=df9['ChannelName'], y=df9['VideoDurationSeconds'], text=df9['VideoDurationSeconds'],
                                        marker=dict(color='greenyellow'),
                                        hovertemplate='%{x}<br>VideoDurationSeconds: %{y}')])
                fig.update_layout(title='Average duration  of channels that published in given year', xaxis_title='ChannelName', yaxis_title='VideoDurationSeconds')
                st.plotly_chart(fig)

        elif Question=='10.Which videos have the highest number of comments, and what are their corresponding channel names?':
                mycursor.execute("SELECT channel_data.channel_name AS ChannelName, MAX(videos_data.Commentcount)AS VideoCommentCount FROM channel_data JOIN videos_data ON channel_data.channel_id = videos_data.channel_id GROUP BY channelName ORDER BY VideoCommentCount DESC")
                qn10=mycursor.fetchall()   
                df10=pd.DataFrame(qn10,columns=["ChannelName","VideoCommentCount"])
                st.write(df10)
                fig = go.Figure(data=[go.Bar(x=df10['ChannelName'], y=df10['VideoCommentCount'], text=df10['VideoCommentCount'],
                                        marker=dict(color=' thistle'),
                                        hovertemplate='%{x}<br>VideoCommentCount: %{y}')])
                fig.update_layout(title='Average duration  of channels that published in given year', xaxis_title='ChannelName', yaxis_title='VideoCommentCount')
                st.plotly_chart(fig)