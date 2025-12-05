import matplotlib.pyplot as plt


def show_map():
    _, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 3, 2])
    plt.show()


if __name__ == "__main__":
    show_map()
