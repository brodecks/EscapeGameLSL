import sys
from pylsl import StreamInlet, resolve_streams, resolve_byprop
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

nameLSLFlux = sys.argv[1]
typeFlux = sys.argv[2]
FLUX_AVAILABLE = resolve_streams(wait_time=2.0)

print("Flux disponibles : ")
for flux in FLUX_AVAILABLE:
    inletTemp = StreamInlet(flux)
    print(inletTemp.info().name())

stream = resolve_byprop("name", nameLSLFlux)
inlet = StreamInlet(stream[0])
nb_channels = inlet.channel_count

if typeFlux == "chunk":
    while True:
        chunk, timestamp = inlet.pull_chunk()
        print(f"{timestamp} : {chunk}")

elif typeFlux == "sample":
    sample, timestamp = inlet.pull_sample()
    print(type(sample))
    print(f"{timestamp} : {sample}")

    # while True:
    #     sample, timestamp = inlet.pull_sample()
    #     print(type(sample))
    #     print(f"{timestamp} : {sample}")

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

xar = [[] for _ in range(nb_channels)]
yar = []
limitSize = 5


def animate(i):
    if typeFlux == "sample":
        samples, timestamp = inlet.pull_sample()
        for i in range(len(samples)):
            xar[i].append(samples[i])
            if len(xar[i]) > limitSize:
                xar[i].pop(0)
        yar.append(timestamp)
        if len(yar) > limitSize:
            yar.pop(0)

        ax1.clear()
        ax1.plot(yar, xar[0])


ani = FuncAnimation(fig, animate, interval=1000)
plt.show()
fig.savefig("mon_graphique.png")
print("Graphique sauvegardé sous mon_graphique.png")