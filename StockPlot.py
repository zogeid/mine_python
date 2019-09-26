import matplotlib.pyplot as plt


def plot(day_array):
    maximo = []
    for d in day_array:
        maximo.append(d.high)

    plt.plot(maximo)
    plt.show()
