import os
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.http import HttpRequest

# Scopes required for the YouTube Data API
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def is_pickle_file(filepath):
    try:
        with open(filepath, 'rb') as file:
            pickle.load(file)
        return True
    except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError):
        return False


def get_authenticated_service(client_secrets_file:str,client_token_pickle:str|None):
    assert isinstance(client_secrets_file,str)
    assert isinstance(client_token_pickle, (str, type(None)))
    
    creds = None
    is_pickle=is_pickle_file(client_token_pickle)
    # The file token.pickle stores the user's access and refresh tokens
    if isinstance(client_token_pickle, str) and os.path.exists(client_token_pickle) and is_pickle:
        with open(client_token_pickle, 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no valid credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing access token...")
            try:
                creds.refresh(Request())
            except RefreshError:
                print("Refresh token is invalid. Initiating new OAuth flow.")
                creds = None
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            creds = flow.run_local_server(port=0)
        
        # try for pc
        if not creds:
            try:
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file, scopes)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print("Tried Refreshing, but somehow can't establish flow.",e)
                creds = None

            """if not creds:
            try: 
                Flow = Flow.from_client_secrets_file(client_secrets_file, scopes=scopes,redirect_uri='urn:ietf:wg:oauth:2.0:oob')
                auth_url, _ = flow.authorization_url(prompt='consent')
                from subprocess import run as SubProcRun
                
                #print(f"Please visit this URL to authorize the application: {auth_url}")
                SubProcRun(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', auth_url])
                code = input("Enter the authorization code: ")
                flow.fetch_token(code=code)
                creds = flow.credentials
            except Exception e: 
                print("Tried Refreshingusing manual flow, but....",e)
                creds = None
            """
        # Save the credentials for the next run
        with open('secrets/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return googleapiclient.discovery.build('youtube', 'v3', credentials=creds)

def add_video_to_history_playlist(youtube, video_id):
    try:
        # Create a playlistItem resource for the history playlist
        body = {
            "snippet": {
                "playlistId": "HL",  # "HL" is a special playlist ID for Watch History
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }

        # Insert the video into the watch history
        request = youtube.playlistItems().insert(
            part="snippet",
            body=body
        )
        
        # Use the underlying HTTP object to send the request without expecting a response
        http_request = HttpRequest(http=request.http, uri=request.uri, method="POST", body=request.body, headers=request.headers,postproc=request.postproc)
        _ = http_request.execute()

        print(f"Marked video {video_id} as watched")

    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")

def add_playlist_items_to_history_playlist(youtube, playlist_id):
    try:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=550
        )
        response = request.execute()

        for item in response["items"]:
            video_id = item["contentDetails"]["videoId"]
            add_video_to_history_playlist(youtube, video_id)

    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")

# Function to empty a playlist
def empty_playlist(youtube,playlist_id):
    try:
        # Get all playlist items
        request = youtube.playlistItems().list(
            part="id",
            playlistId=playlist_id,
            maxResults=550
        )
        response = request.execute()

        # Delete each item from the playlist
        for item in response["items"]:
            try:
                youtube.playlistItems().delete(
                    id=item["id"]
                ).execute()
                print(f"Removed item {item['id']} from playlist")
            except googleapiclient.errors.HttpError as e:
                if "400" in str(e):
                    print(f"Item {item['id']} seems to have been removed, but an error was returned.")
                else:
                    print(f"Error removing item {item['id']}: {e}")

    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred: {e}")

