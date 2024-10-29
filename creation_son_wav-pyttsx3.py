
#
# REPRENDRE LE FICHIER GTTS ET MODIFIER LA DEFINITION DE GENERATION DU SON
#

import pyttsx3
import json
from pathlib import Path

dossier = Path.cwd()
fichier = dossier / "liste.json"
fichier.touch(exist_ok=True)  # création du fichier si pas existant

liste = json.loads(fichier.read_text() or '[]')

# Initialiser le moteur de synthèse vocale
engine = pyttsx3.init()
# Obtenir la liste des voix disponibles
voices = engine.getProperty('voices')


def generate_sound(choix_voix):
    print(dossier)
    # Exemple : Sélectionner la voix numéro 1 (ou une autre selon la liste obtenue)
    engine.setProperty('voice', voices[choix_voix].id)

    # Configurer la vitesse et le volume de la voix
    engine.setProperty('rate', 160)  # Vitesse de la voix
    engine.setProperty('volume', 1)  # Volume (0.0 à 1.0)

    # Le texte à convertir en audio
    texte = input("Quel texte voulez vous synthétiser ?\n"
                  "   Votre texte : ")

    # Générer l'audio et l'enregistrer dans un fichier WAV
    while True:
        file_name = input("nom du fichier de sortie sans l'extention : ") + '.wav'
        if file_name in liste:
            save = (input('fichier existant, voulez vous écraser le fichier - Y or N ?\n'
                          '   Votre choix :'))
            if save.lower() == "y" or "n":
                if save.lower() == "y":
                    tts.save(file_name + ".wav")
                    engine.save_to_file(texte, dossier)
                    print('fichier écrasé')
                    break
                elif save.lower() == "n":
                    continue
            else:
                print('Vous devez choisir entre Y ou N')
                continue
        else:
            engine.save_to_file(texte, file_name)
            liste.append(file_name)
            break

    engine.save_to_file(texte, file_name)

    # Lancer la conversion
    engine.runAndWait()

    liste.append(file_name)
    with open(fichier, "w") as f:
        json.dump(liste, f)
    print(30 * '-')
    print(f'fichier {file_name} créé dans {fichier.parent}')
    print(30 * '-')


def choice_voice():
    while True:
        # Afficher les informations de chaque voix
        for i, voice in enumerate(voices):
            print(f"Voix {i}: ")
            print(f" - Nom: {voice.name}")
            print(f" - ID: {voice.id}")
            print(f" - Langue: {voice.languages}")
            print(f" - Sexe: {voice.gender}")
            print(f" - Âge: {voice.age}")
            print("-" * 30)
            print("")

        choix = input('Quelle voix souhaitez-vous utiliser ?\n'
                      'Mon choix : ')

        if choix.isdigit():
            if int(choix) in range(1):
                generate_sound(int(choix))
                main_menu()
            else:
                print(30 * '-')
                print("Le choix doit être un chiffre dans la plage des voix énumérées, veuillez recommencer.")
                print(30 * '-')
                continue

        else:
            print(30 * '-')
            print("Le choix doit être un chiffre correspondant aux voix énumérées, veuillez recommencer.")
            print(30 * '-')
            print('')
            continue


def afficher():
    if len(liste) != 0:
        index = 0
        for i in liste:
            print(index + 1, ": ", i)
            index += 1
        print('')
    else:
        print("\nLa liste est vide.\n")


def sortie():
    print("Au revoir...")
    exit()


def suppression_liste(liste):
    print(30 * "-")
    print(f'ATTENTION TOUS LES FICHIERS CONTENU DANS LE DOSSIER\n'
          f'            {dossier.parent}\n'
          f'      SERONT DEFINITIVEMENT SUPPRIMES.')
    print(30 * "-")
    suppression = input(f'Etes vous sûre ? Y pour Yes, autre touche pour annuler\n'
                        f'   Votre choix : ')
    if suppression.lower() == "y":
        for file in liste:
            rep = dossier / file
            rep.unlink()
        liste.clear()
        print('fichiers écrasés')

    with open(fichier, "w") as f:
        json.dump(liste, f)


def main_menu():
    while True:
        propositions = input('Faites votre choix parmi les propositions suivantes: \n'
                             '\n'
                             '1: Créer un nouveau son\n'
                             '2: Afficher la liste des sons existants\n'
                             '3: Vider lite\n'
                             '4: Quitter\n'
                             '   Votre choix : ')
        print('')

        if not propositions.isdigit() or int(propositions) > 4:
            print('\nVotre choix doit être un chiffre entre 1 et 4, recommencez !')
            print(30 * '-')
            print('')
            continue

        else:
            if propositions == "1":
                choice_voice()
            elif propositions == "2":
                afficher()
            elif propositions == "3":
                suppression_liste(liste)
            elif propositions == "4":
                sortie()


main_menu()
