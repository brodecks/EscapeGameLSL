import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pylsl import StreamInlet, resolve_byprop

# Configuration initiale
nameLSLFlux = sys.argv[1]
stream = resolve_byprop("name", nameLSLFlux, timeout=2.0)
if not stream:
    print("Flux introuvable")
    sys.exit()

inlet = StreamInlet(stream[0])
nb_channels = inlet.info().channel_count()

# Listes vides qui vont stocker TOUTE la session
x_data = []  # Temps
y_data = [[] for _ in range(nb_channels)]  # Données par canal

fig, ax = plt.subplots()


def animate(i):
    # Récupérer TOUTES les données en attente dans le buffer LSL
    chunk, timestamps = inlet.pull_chunk()

    if timestamps:
        # On ajoute les nouvelles données aux listes existantes sans rien supprimer
        x_data.extend(timestamps)
        for row_index, sample in enumerate(chunk):
            for ch in range(nb_channels):
                y_data[ch].append(sample[ch])

        # Mise à jour du graphique
        ax.clear()
        for ch in range(nb_channels):
            # On trace l'intégralité des listes
            ax.plot(x_data, y_data[ch], label=f"Canal {ch}")

        ax.set_title(f"Enregistrement en direct : {nameLSLFlux}")
        ax.set_xlabel("Temps LSL (s)")
        ax.legend(loc="upper left")

        # Ajustement automatique des axes pour voir toute la progression
        ax.relim()
        ax.autoscale_view()


# Intervalle de 100ms pour une mise à jour fluide
ani = FuncAnimation(fig, animate, interval=100, cache_frame_data=False)

def closeWindow(event):
    fig.savefig("mon_graphique1.png")

fig.canvas.mpl_connect('close_event', closeWindow)

plt.tight_layout()
plt.show()
