import time
from pylsl import StreamInfo, StreamOutlet
from pynput import keyboard

#config
info = StreamInfo('Metronome', 'Marker', 1, 0, 'int32', 'metronome_001')
outlet = StreamOutlet(info)

print("Appuie sur ESPACE pour envoyer un marqueur LSL !")
print("Appuie sur ECHAP pour quitter.")


#fonction qui traite l'input de la touche espace
def touche_entree(key):
    try:
        if key == keyboard.Key.space:
            # On envoie le marqueur 99 sur LSL
            outlet.push_sample([99])
            print(" [ESPACE] -> Marqueur 99 envoyé à LSL")
        elif key == keyboard.Key.ctrl_l:
            outlet.push_sample([80])
            print(" [ctrl gauche] -> Marqueur 80 envoyé à LSL")

        if key == keyboard.Key.esc:
            # Arrêter l'écouteur
            return False
    except AttributeError:
        pass


with keyboard.Listener(on_press=touche_entree) as listener:
    listener.join()