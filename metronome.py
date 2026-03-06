import time
from pylsl import StreamInfo, StreamOutlet
import threading

#config
info = StreamInfo('Metronome', 'Marker', 1, 0, 'int32', 'metronome_001')
outlet = StreamOutlet(info)

# Variable globale pour le rythme
bpm_metronome = 60


def metronome_loop():
    print(f"Métronome lancé à {bpm_metronome} BPM")
    while True:
        outlet.push_sample([bpm_metronome])
        # Calculer l'attente en fonction du BPM choisi
        intervalle = 60.0 / bpm_metronome
        time.sleep(intervalle)


#On utilise un thread pour pouvoir changer de bpm avec un input de lutilisateur
thread = threading.Thread(target=metronome_loop, daemon=True)
thread.start()

while True:
    try:
        nouveau_bpm = input("Entrez un nouveau BPM : ")
        bpm_metronome = int(nouveau_bpm)
        print(f"Rythme modifié : {bpm_metronome} BPM")
    except ValueError:
        print("Veuillez entrer un nombre entier.")