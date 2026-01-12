import requests
import os
import time

# --- Konfiguration ---
# Die URL von der das Bild heruntergeladen wird.
IMAGE_URL = "https://thispersondoesnotexist.com/"
# Das Verzeichnis, in dem die Bilder gespeichert werden sollen.
IMAGE_DIR = os.path.join("backend", "userImages")
# --- Ende der Konfiguration ---

def find_next_filename():
    """
    Findet den nächsten verfügbaren Dateinamen im Zielverzeichnis.
    Die Dateinamen sind fortlaufend nummeriert (1.jpg, 2.jpg, ...).
    """
    # Sicherstellen, dass das Verzeichnis existiert
    os.makedirs(IMAGE_DIR, exist_ok=True)
    
    # Bestehende .jpg-Dateien im Verzeichnis finden
    existing_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.jpg')]
    
    # Die höchste existierende Nummer finden
    highest_number = 0
    for f in existing_files:
        try:
            # Dateiname ohne Erweiterung extrahieren und in eine Zahl umwandeln
            number = int(f.split('.')[0])
            if number > highest_number:
                highest_number = number
        except ValueError:
            # Ignoriert Dateien, die nicht dem erwarteten nummerierten Format entsprechen
            continue
            
    # Die nächste Nummer ist die höchste existierende + 1
    next_file_number = highest_number + 1
    
    return os.path.join(IMAGE_DIR, f"{next_file_number}.jpg")

def download_image(file_path):
    """
    Lädt ein einzelnes Bild von der IMAGE_URL herunter und speichert es unter dem angegebenen file_path.
    """
    try:
        print(f"Lade Bild herunter von: {IMAGE_URL}")
        # Eine GET-Anfrage an die URL senden. Der User-Agent wird gesetzt, um Blockierungen zu vermeiden.
        response = requests.get(IMAGE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        # Überprüft, ob die Anfrage erfolgreich war (Statuscode 200)
        response.raise_for_status()

        # Das Bild im Binärmodus in die Zieldatei schreiben
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Bild erfolgreich als '{file_path}' gespeichert.")
        return True

    except requests.exceptions.RequestException as e:
        # Fängt Fehler ab, die bei der Netzwerkanfrage auftreten können
        print(f"Fehler beim Herunterladen des Bildes: {e}")
        return False

def main():
    """
    Die Hauptfunktion des Skripts. Frägt den Benutzer, wie viele Bilder heruntergeladen werden sollen,
    und führt den Download-Prozess in einer Schleife aus.
    """
    try:
        # Den Benutzer fragen, wie viele Bilder heruntergeladen werden sollen
        num_images_to_download = int(input("Wie viele Bilder möchten Sie herunterladen? "))
        if num_images_to_download <= 0:
            print("Bitte geben Sie eine positive Zahl ein.")
            return
    except ValueError:
        print("Ungültige Eingabe. Bitte geben Sie eine Zahl ein.")
        return

    print(f"\nStarte den Download von {num_images_to_download} Bildern...")
    
    downloaded_count = 0
    for i in range(num_images_to_download):
        print(f"\n--- Bild {i+1}/{num_images_to_download} ---")
        
        # Den nächsten freien Dateinamen ermitteln
        file_path = find_next_filename()
        
        # Das Bild herunterladen
        if download_image(file_path):
            downloaded_count += 1
            # Eine kleine Pause einlegen, um den Server nicht zu überlasten
            time.sleep(1)
        else:
            # Bei einem Fehler den Vorgang abbrechen
            print("Download abgebrochen aufgrund eines Fehlers.")
            break
            
    print(f"\nDownload abgeschlossen. {downloaded_count} von {num_images_to_download} Bildern erfolgreich heruntergeladen.")


# Dieser Block stellt sicher, dass die main()-Funktion nur ausgeführt wird,
# wenn das Skript direkt gestartet wird (nicht wenn es als Modul importiert wird).
if __name__ == "__main__":
    main()
