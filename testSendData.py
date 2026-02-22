from pylsl import StreamInfo, StreamOutlet
import time
import random

# Nom: 'HeartSim', Type: 'HR', Nb canaux: 1, Fréquence: 1Hz, Format: float32
info = StreamInfo('HeartSim', 'HR', 1, 1, 'float32', 'pi-ceinture-001')

outlet = StreamOutlet(info)

print("Diffusion des donnees")

while True:
    #generation d'un faux BPM entre 60 et 100 (changer)
    bpm_virtuel = float(random.randint(60, 100))

    #envoie de la donne sur le reseau
    outlet.push_sample([bpm_virtuel])

    print(f"BPM envoyé : {bpm_virtuel}")
    time.sleep(1)
