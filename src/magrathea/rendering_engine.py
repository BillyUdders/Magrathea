import io

import numpy as np
from loguru import logger
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from perlin_noise import PerlinNoise


def generate_heightmap(size, octaves):
    logger.debug(f"Generating heightmap: size={size}, octaves={octaves}")
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


def render_map_to_png(size, octaves, filename):
    logger.info(f"Rendering map to file: {filename} (size={size}, octaves={octaves})")
    heightmap = generate_heightmap(size, octaves)
    fig = create_figure(heightmap)
    FigureCanvasAgg(fig).print_png(filename)
    logger.success(f"Map saved to {filename}")


def render_map_to_buffer(size, octaves):
    logger.info(f"Rendering map to buffer (size={size}, octaves={octaves})")
    heightmap = generate_heightmap(size, octaves)
    fig = create_figure(heightmap)
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    output.seek(0)
    logger.success("Map rendered to buffer")
    return output
