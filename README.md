Deezer to YouTube Playlist Sync
===============================

Ce script permet d'importer une playlist Deezer vers une playlist YouTube en utilisant l'API Deezer et l'API YouTube Data v3.

Prérequis
---------

### 1\. API YouTube

Vous devez créer un projet sur Google Cloud et activer l'API YouTube Data v3. Ensuite, téléchargez le fichier client\_secret.json contenant vos identifiants OAuth2.

### 2\. Dépendances Python

Installez les bibliothèques nécessaires avec la commande suivante :

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install requests google-auth-oauthlib google-auth-httplib2 google-auth google-auth-oauthlib google-auth-httplib2 googleapiclient   `

Configuration
-------------

Modifiez les variables suivantes dans le script Deezer\_To\_Youtube.py :

*   DEEZER\_PLAYLIST\_ID : l'ID de la playlist Deezer à importer.
    
*   YOUTUBE\_PLAYLIST\_TITLE : le nom de la playlist YouTube de destination.
    
*   CLIENT\_SECRETS\_FILE : le fichier JSON contenant vos identifiants OAuth2.
    

Utilisation
-----------

1.  Exécutez le script avec Python :
    

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python Deezer_To_Youtube.py   `

1.  Une fenêtre de connexion OAuth s'ouvrira pour vous permettre d'autoriser l'accès à votre compte YouTube.
    
2.  Le script recherchera les titres de la playlist Deezer sur YouTube et les ajoutera à la playlist YouTube.
    

Gestion du quota YouTube
------------------------

Le script est optimisé pour minimiser l'utilisation du quota de l'API YouTube :

*   Les titres déjà présents dans la playlist YouTube ne sont pas recherchés à nouveau.
    
*   Une pause est ajoutée après chaque ajout pour éviter les limitations.
    
*   Si le quota est dépassé, les titres restants sont sauvegardés pour un ajout ultérieur (pending\_tracks.txt).
    

Fichiers générés
----------------

*   not\_found\_tracks.txt : Liste des titres non trouvés sur YouTube.
    
*   pending\_tracks.txt : Liste des titres à ajouter ultérieurement si le quota est atteint.
    

Avertissement
-------------

L'utilisation de l'API YouTube est soumise à des quotas. Assurez-vous de surveiller votre consommation et de ne pas dépasser les limites imposées par Google.
