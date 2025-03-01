# Deezer2YouTube
Migration de Playlist Deezer vers Youtube

Pour exporter ta playlist de Deezer vers YouTube Music, voici les étapes générales :

Récupérer les titres depuis Deezer : L'API Deezer permet d'extraire une playlist avec son ID.
Chercher et ajouter les titres sur YouTube Music : Utilisation de l'API YouTube Data v3.

Prérequis :
Un compte Deezer avec une clé d'API (obtenue via Deezer Developers).
Un projet Google Cloud avec l'API YouTube Data activée et une clé d'API OAuth.
Je vais te fournir un script Python qui :
✅ Récupère les titres depuis Deezer.
✅ Les recherche sur YouTube Music.
✅ Crée une playlist et y ajoute les morceaux correspondants.

🔹 Instructions :
Remplace TON_ID_PLAYLIST par l'ID de ta playlist Deezer.
Obtiens tes clés OAuth Google et place-les dans client_secret.json.
Installe les dépendances avec 
pip install requests google-auth-oauthlib google-auth google-api-python-client.
Lance le script : python script.py
