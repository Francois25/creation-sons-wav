import json
import time

from pydub import AudioSegment
from gtts import gTTS
from pathlib import Path

statut = ''
dossier = Path.cwd()
fichier = dossier / "liste.json"
fichier.touch(exist_ok=True)  # création du fichier si pas existant

liste = json.loads(fichier.read_text() or '[]')


def choice_voice():
    while True:
        langue_dispo = {
            1: ["Français", "fr"],
            2: ["Allemand", "de"],
            3: ["Anglais", "en"],
        }
        choix_langue = input('Quelle accent souhaitez-vous utiliser ?\n'
                             f'1: {langue_dispo[1][0]}\n'
                             f'2: {langue_dispo[2][0]}\n'
                             f'3: {langue_dispo[3][0]}\n'
                             '   Votre choix : ')

        if choix_langue.isdigit() and int(choix_langue) in langue_dispo:
            print(f"\nL'accent choisi est '{langue_dispo[int(choix_langue)][0]}'")
            langue = langue_dispo[int(choix_langue)][1]
            generate_sound(langue)
            main_menu()

        else:
            print(50 * '-')
            print("Le choix doit être un chiffre, recommencer.")
            print(50 * '-')
            print('')
            continue


def generate_sound(langue):
    global statut
    # Le texte à convertir en audio
    texte = input("\nQuel texte voulez vous synthétiser ?\n"
                  "   Votre texte : ")

    tts = gTTS(text=texte, lang=langue, slow=False)

    # Générer l'audio et l'enregistrer dans un fichier WAV
    while True:
        file_name = input("   Nom du fichier de sortie (sans l'extention) : ") + ".wav"
        if file_name in liste:
            save = (input('fichier existant, voulez vous écraser le fichier - Y or N ?\n'
                          '   Votre choix :'))
            if save.lower() == "y":
                tts.save(file_name)
                statut = "écrasé"
                break

            elif save.lower() == "n":
                continue

            else:
                print('Vous devez choisir entre Y ou N')
                continue
        else:
            tts.save(file_name)
            statut = "créé"
            break

    audio_convert(file_name)
    liste.append(file_name)

    with open(fichier, "w") as f:
        json.dump(liste, f)

    print('')
    print(70 * '-')
    print(f'fichier {file_name} {statut} dans {fichier.parent}')
    print(70 * '-')


def audio_convert(file_name):
    # Charger le fichier hello_gtts.wav
    audio_gtts = AudioSegment.from_file(file_name)

    # Convertir pour correspondre aux propriétés de hello_base.wav
    audio_gtts_resampled = audio_gtts.set_frame_rate(32000).set_channels(1)

    # Exporter le fichier
    audio_gtts_resampled.export(file_name, format="wav")


def afficher():
    if len(liste) != 0:
        liste_unique = list(set(liste))
        index = 0
        for i in liste_unique:
            print(index + 1, ": ", i)
            index += 1
        print('')
    else:
        print("La liste est vide.")


def suppression_liste():
    print(30 * "-")
    print(f'ATTENTION TOUS LES FICHIERS CONTENU DANS LE DOSSIER\n'
          f'            {dossier.parent}\n'
          f'      SERONT DEFINITIVEMENT SUPPRIMES.')
    print(30 * "-")
    suppression = input(f'Etes vous sûre ? Y pour Yes, autre touche pour annuler\n'
                        f'   Votre choix : ')
    if suppression.lower() == "y":
        for file in liste:
            f = Path.cwd() / file
            if f.exists():
                f.unlink()
        liste.clear()
        print('fichiers écrasés')

    with open(fichier, "w") as f:
        json.dump(liste, f)


def sortie():
    print("Au revoir...")
    time.sleep(2)
    exit()


def main_menu():
    while True:
        propositions = input('\nFaites votre choix parmi les propositions suivantes: \n'
                             '\n'
                             '1: Créer un nouveau son\n'
                             '2: Afficher la liste des sons existants\n'
                             '3: Vider la liste\n'
                             '4: Quitter\n'
                             '   Votre choix : ')
        print('')

        if not propositions.isdigit() or int(propositions) > 4:
            print('\nVotre choix doit être un chiffre entre 1 et 4, recommencez !')
            print(65 * '-')
            print('')
            continue

        else:
            if propositions == "1":
                choice_voice()
            elif propositions == "2":
                afficher()
            elif propositions == "3":
                suppression_liste()
            elif propositions == "4":
                sortie()


main_menu()
