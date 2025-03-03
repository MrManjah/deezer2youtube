import requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json
import time

# Configuration Deezer
DEEZER_PLAYLIST_ID = "195667401"
DEEZER_API_URL = f"https://api.deezer.com/playlist/{DEEZER_PLAYLIST_ID}/tracks"

# Configuration YouTube OAuth2
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Nom de la playlist YouTube cible
YOUTUBE_PLAYLIST_TITLE = "Coups de coeur"

def get_deezer_tracks():
    tracks = []
    url = DEEZER_API_URL

    while url:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                tracks.extend((track["title"].lower(), track["artist"]["name"].lower()) for track in data["data"])
                url = data.get("next")
            else:
                print("Erreur : Clé 'data' absente dans la réponse JSON")
                return []
        else:
            print(f"Erreur {response.status_code} lors de la récupération des titres Deezer")
            return []

    print(f"Nombre total de titres récupérés : {len(tracks)}")
    return tracks

def youtube_auth():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES
    )
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    return youtube

def get_existing_playlist(youtube):
    request = youtube.playlists().list(part="snippet", mine=True, maxResults=50)
    response = request.execute()
    for playlist in response.get("items", []):
        if playlist["snippet"]["title"] == YOUTUBE_PLAYLIST_TITLE:
            return playlist["id"]
    return None

def create_youtube_playlist(youtube):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": YOUTUBE_PLAYLIST_TITLE, "description": "Playlist importée depuis Deezer"},
            "status": {"privacyStatus": "private"},
        },
    )
    response = request.execute()
    return response["id"]

def get_existing_videos(youtube, playlist_id):
    existing_videos = set()
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part="snippet", playlistId=playlist_id, maxResults=50, pageToken=next_page_token
        )
        response = request.execute()
        for item in response.get("items", []):
            title = item["snippet"]["title"].lower()
            existing_videos.add(title)
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return existing_videos

def search_and_add_tracks(youtube, playlist_id, tracks):
    existing_videos = get_existing_videos(youtube, playlist_id)
    not_found_tracks = []
    pending_tracks = []
    search_cache = {}

    for title, artist in tracks:
        track_key = f"{title} {artist}"
        if any(title in video or track_key in video for video in existing_videos):
            print(f"Déjà présent : {track_key}")
            continue
        
        try:
            if track_key in search_cache:
                video_id = search_cache[track_key]
            else:
                search_request = youtube.search().list(q=track_key, part="snippet", maxResults=1, type="video")
                search_response = search_request.execute()
                if search_response["items"]:
                    video_id = search_response["items"][0]["id"]["videoId"]
                    search_cache[track_key] = video_id
                else:
                    print(f"Non trouvé : {track_key}")
                    not_found_tracks.append(track_key)
                    continue
            
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": video_id},
                    }
                },
            ).execute()
            print(f"Ajouté : {track_key}")
            time.sleep(2)
        
        except googleapiclient.errors.HttpError as e:
            error_msg = str(e)
            if "quotaExceeded" in error_msg:
                print("Quota dépassé, enregistrement des titres restants et arrêt du script.")
                pending_tracks.extend(tracks[tracks.index((title, artist)):])
                break
            print(f"Erreur lors de l'ajout de {track_key} : {e}")
            time.sleep(5)

    if not_found_tracks:
        with open("not_found_tracks.txt", "w", encoding="utf-8") as file:
            for track in not_found_tracks:
                file.write(track + "\n")
        print("Liste des titres introuvables sauvegardée dans 'not_found_tracks.txt'")
    
    if pending_tracks:
        with open("pending_tracks.txt", "w", encoding="utf-8") as file:
            for track in pending_tracks:
                file.write(track + "\n")
        print("Liste des titres en attente sauvegardée dans 'pending_tracks.txt', relance demain.")

def main():
    tracks = get_deezer_tracks()
    if not tracks:
        return
    youtube = youtube_auth()
    playlist_id = get_existing_playlist(youtube)
    if not playlist_id:
        playlist_id = create_youtube_playlist(youtube)
    search_and_add_tracks(youtube, playlist_id, tracks)
    print(f"Import terminé dans la playlist '{YOUTUBE_PLAYLIST_TITLE}' !")

if __name__ == "__main__":
    main()
