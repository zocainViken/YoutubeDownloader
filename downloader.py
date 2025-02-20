import re
import yt_dlp


def download_video(url, output_path):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"Téléchargement vidéo terminé : {output_path}")
    except Exception as e:
        print(f"Erreur lors du téléchargement de la vidéo : {e}")

def download_audio(url, output_path):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print(f"Téléchargement terminé : {output_path}")
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")

def download_subtitles(url, subtitle_output_path):
    try:
        ydl_opts = {
            'skip_download': True,  # Ne télécharge pas la vidéo
            'writesubtitles': True,
            'writeautomaticsub': True,  # Inclut les sous-titres générés automatiquement si dispo
            #'subtitleslangs': ['en', 'fr'],  # Langues des sous-titres (ajoute d'autres si nécessaire)
            'subtitleslangs': ['fr'],  # Langues des sous-titres (ajoute d'autres si nécessaire)
            'subtitlesformat': 'srt',
            'outtmpl': subtitle_output_path,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info.get('subtitles') and not info.get('automatic_captions'):
                print("Erreur : Aucun sous-titre disponible pour cette vidéo.")
                return
            
            ydl.download([url])
        
        print(f"Téléchargement des sous-titres terminé : {subtitle_output_path}")
    except Exception as e:
        print(f"Erreur lors du téléchargement des sous-titres : {e}")

def clean_vtt(fichier_vtt, fichier_sortie):
    with open(fichier_vtt, 'r', encoding='utf-8') as file:
        contenu = file.readlines()

    # Supprimer les 3 premières lignes
    contenu = contenu[3:]

    # Joindre les lignes restantes en un seul texte
    contenu = ''.join(contenu)

    # Supprimer les balises de temps (par exemple : 00:00:00.199 --> 00:00:03.889)
    contenu_sans_temps = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', '', contenu)

    # Supprimer les balises de position (par exemple : align:start position:0%)
    contenu_sans_position = re.sub(r'align:[^ \n]+ position:[^ \n]+', '', contenu_sans_temps)

    # Supprimer les balises de style (par exemple : <c>text</c>)
    contenu_sans_style = re.sub(r'<[^>]+>', '', contenu_sans_position)

    # Nettoyer les retours à la ligne inutiles
    contenu_nettoye = re.sub(r'\n+', '\n', contenu_sans_style).strip()

    # Supprimer les lignes en double
    lignes = contenu_nettoye.split('\n')
    lignes_sans_doublons = list(dict.fromkeys(lignes))  # Utilisation d'un dict pour éliminer les doublons

    # Supprimer les lignes sans texte (vides ou composées uniquement d'espaces)
    lignes_filtrees = [ligne for ligne in lignes_sans_doublons if ligne.strip() != '']

    # Joindre à nouveau les lignes filtrées
    contenu_filtre = '\n'.join(lignes_filtrees)

    # Enregistrer le contenu nettoyé dans un fichier texte
    with open(fichier_sortie, 'w', encoding='utf-8') as file:
        file.write(contenu_filtre)

    print(f"Le fichier nettoyé a été enregistré sous : {fichier_sortie}")

def get_video_name(url):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict.get('title', 'Unknown Title')
    except Exception as e:
        print(f"Erreur lors de la récupération du titre : {e}")
        return None






# example Video name usage
url = "https://www.youtube.com/shorts/DGHT-GOARcI"
video_name = get_video_name(url)
print(f"Video name: {video_name}")


# Exemple d'utilisation
url = "https://www.youtube.com/shorts/DGHT-GOARcI"
video_output_path = f"{video_name}.mp4"
# Appels des fonctions
download_video(url, video_output_path)

# download audio examples
url = "https://www.youtube.com/shorts/DGHT-GOARcI"  # Remplace par ton URL
audio_output_path = f"{video_name}"
download_audio(url, audio_output_path)

# download subtitles example
url = "https://www.youtube.com/shorts/DGHT-GOARcI"  # Remplace par ton URL
subtitle_output_path = f"{video_name}"
download_subtitles(url, subtitle_output_path)

# Clean vtt example
input_vtt = f'{video_name}.fr.vtt'  # Remplacer par le chemin du fichier VTT
output_vtt = f'{video_name}_fr_cleaned.txt'  # Nom du fichier texte de sortie
# Appeler la fonction pour nettoyer le fichier et l'enregistrer
clean_vtt(input_vtt, output_vtt)

input_vtt = f'{video_name}.en.vtt'  # Remplacer par le chemin du fichier VTT
output_vtt = f'{video_name}_en_cleaned.txt'  # Nom du fichier texte de sortie
# Appeler la fonction pour nettoyer le fichier et l'enregistrer
clean_vtt(input_vtt, output_vtt)
