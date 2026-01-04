import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
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


def create_figure(heightmap):
    fig = Figure(figsize=(6, 6))
    ax = fig.subplots()
    
    ax.set_title("Perlin Noise Heightmap")
    ax.imshow(heightmap, cmap="terrain", interpolation="nearest")
    # Add colorbar to the figure, targeting the specific axis
    fig.colorbar(ax.images[0], ax=ax, label="Height")
    ax.axis("off")
    return fig


def show_map():
    heightmap = generate_heightmap(128, 4)
    # For interactive display, we can still use pyplot but we'll use our figure creator logic
    # Re-implementing essentially what create_figure does but with pyplot for windowed display
    plt.figure(figsize=(6, 6))
    plt.title("Perlin Noise Heightmap")
    plt.imshow(heightmap, cmap="terrain", interpolation="nearest")
    plt.colorbar(label="Height")
    plt.axis("off")
    plt.show()


def render_map_to_png(size, octaves, filename):
    heightmap = generate_heightmap(size, octaves)
    fig = create_figure(heightmap)
    FigureCanvasAgg(fig).print_png(filename)


def render_map_to_buffer(size, octaves):
    heightmap = generate_heightmap(size, octaves)
    fig = create_figure(heightmap)
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    output.seek(0)
    return output


if __name__ == "__main__":
    show_map()
