import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import time

# Configuration YouTube OAuth2
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
YOUTUBE_PLAYLIST_TITLE = "Coups de coeur"

def youtube_auth():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES
    )
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    return youtube

def get_playlist_id(youtube, title):
    request = youtube.playlists().list(part="snippet", mine=True, maxResults=50)
    response = request.execute()
    for playlist in response.get("items", []):
        if playlist["snippet"]["title"] == title:
            return playlist["id"]
    return None

def get_playlist_videos(youtube, playlist_id):
    videos = []
    video_titles = {}
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet", playlistId=playlist_id, maxResults=50, pageToken=next_page_token
        )
        response = request.execute()
        
        for item in response.get("items", []):
            video_id = item["id"]
            title = item["snippet"]["title"].lower()
            if title in video_titles:
                videos.append((video_id, title))  # Marque comme doublon
            else:
                video_titles[title] = video_id
        
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    
    return videos

def remove_duplicates(youtube, playlist_id):
    duplicates = get_playlist_videos(youtube, playlist_id)
    
    if not duplicates:
        print("Aucun doublon trouvé.")
        return
    
    for video_id, title in duplicates:
        try:
            youtube.playlistItems().delete(id=video_id).execute()
            print(f"Supprimé : {title}")
            time.sleep(1)  # Evite les dépassements de quota
        except googleapiclient.errors.HttpError as e:
            print(f"Erreur lors de la suppression de {title} : {e}")
            time.sleep(5)


def main():
    youtube = youtube_auth()
    playlist_id = get_playlist_id(youtube, YOUTUBE_PLAYLIST_TITLE)
    if not playlist_id:
        print("Playlist introuvable !")
        return
    remove_duplicates(youtube, playlist_id)
    print("Nettoyage terminé !")

if __name__ == "__main__":
    main()
