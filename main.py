import matplotlib.pyplot as plt
from time import sleep
import numpy as np
import cv2


from app.reader import Reader


port = Reader.get_ports()

while len(port) == 0:
    sleep(1)
    print("Conecte o dispositivo à porta")
    port = Reader.get_ports()

if len(port) > 1:
    print("Escolha uma porta:")
    for i, p in enumerate(port):
        print(f"\t{i + 1} - {p}")
    choice = int(input("Porta numero: ")) - 1

    port = port[choice]
else:
    port = port[0]

print("Dispositivo conectado em " + port)
reader = Reader(port.split(" ")[0], n_entries=1, input_freq=2000)

signals = "ABCDEFGH"
fig, ax = plt.subplots(figsize=(12,5))
cv2.namedWindow("Osciloscopio", cv2.WINDOW_NORMAL)

while True:
    key = cv2.waitKey(10)

    if key == ord("q"):
        break

    if not reader.has_actualization():
        cv2.imshow("Osciloscopio", image)
        continue

    values, time, periods = reader.get_reading()

    if len(values[0]) == 0:
        continue

    ax.clear()

    for val in values:
        ax.plot(time, val)
    
    values = np.array(values)
    changes = [list() for i in range(values.shape[0])]
    val_pp = [np.max(v) - np.min(v) for v in values]
    zero_passage = values > np.mean(values, axis=0)

    for i in range(zero_passage.shape[1] - 1):
        for j in range(zero_passage.shape[0]):
            if zero_passage[j][i] != zero_passage[j][i+1]:
                changes[j].append(i)
    
    val_rms = list()
    for s, change in enumerate(changes):
        if len(change) < 3:
            rms = values[s, :]
        else:
            rms = values[s, change[0]: change[2]]
        
        rms = np.power(rms, 2)
        rms = np.sqrt(np.mean(rms))

        val_rms.append(rms)

    per = [f"{1 / i :.2f}" if i > 0 else "NA" for i in periods]
    ax.legend([f"Signal {signals[i]}: {per[i]}Hz" for i in range(len(values))])

    label = [f"Signal {signals[i]}:\nVrms: {val_rms[i]:.2f}V\nVpp: {val_pp[i]:.2f}V" for i in range(len(values))]
    label = "\n\n".join(label)
    ax.set_ylabel(label)
    ax.yaxis.label.set(rotation='horizontal', ha='right')

    fig.canvas.draw()

    ncols, nrows = fig.canvas.get_width_height()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8).reshape(nrows, ncols, 3)
    
    cv2.imshow("Osciloscopio", image)

reader.kill()
cv2.destroyAllWindows()
