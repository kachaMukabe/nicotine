# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
from environs import Env

import googleapiclient.discovery

api_service_name = "youtube"
api_version = "v3"
env = Env()
env.read_env()
DEVELOPER_KEY = os.environ["YOUTUBE_API_KEY"]

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

def get_channel_uploads_id(channel_id):
    

    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response = request.execute()
    
    if response["pageInfo"]["resultsPerPage"] >= 1:
        return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    else:
        return None

def get_uploads(uploads_id, num_of_videos=1):
    request = youtube.playlistItems().list(
        part="snippet,contentDetails,status",
        playlistId=uploads_id,
        maxResults=num_of_videos
    )
    response = request.execute()
    videos = []
    for upload in response["items"]:
        videos.append({
            "title": upload["snippet"]["title"],
            "videoId": upload["contentDetails"]["videoId"]
        })
    return videos

def get_channel_details(channel_id):
    request = youtube.channels().list(
        part="contentDetails, snippet",
        id=channel_id
    )
    response = request.execute()
    if response["pageInfo"]["resultsPerPage"] >= 1:
        return response["items"][0]
    else:
        return None

def get_videos(channel_id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    uploads_id = get_channel_uploads_id(channel_id)
    uploads = get_uploads(uploads_id)
    return uploads
    