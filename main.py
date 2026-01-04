import matplotlib.pyplot as plt
import numpy as np
from perlin_noise import PerlinNoise


def generate_heightmap(size, octaves):
    noise = PerlinNoise(octaves=octaves)
    data = np.zeros((size, size))

    for y in range(size):
        for x in range(size):
            nx = x / size
            ny = y / size
            data[y][x] = noise([nx, ny])  # Perlin noise value

    return data


def plot_map(heightmap):
    plt.figure(figsize=(6, 6))

    plt.title("Perlin Noise Heightmap")
    plt.imshow(heightmap, cmap="terrain", interpolation="nearest")
    plt.colorbar(label="Height")
    plt.axis("off")


def show_map():
    heightmap = generate_heightmap(128, 4)
    plot_map(heightmap)
    plt.show()


def render_map_to_png(size, octaves, filename):
    heightmap = generate_heightmap(size, octaves)
    plot_map(heightmap)
    plt.savefig(filename)
    plt.close()


if __name__ == "__main__":
    show_map()
