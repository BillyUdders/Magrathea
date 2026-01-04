import io
import random

import numpy as np
from loguru import logger
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from noise import pnoise2


def generate_island_mask(size: int) -> np.ndarray:
    """Creates a circular gradient mask to force island generation."""

    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    xx, yy = np.meshgrid(x, y)
    d = np.sqrt(xx**2 + yy**2)

    # Create a smooth falloff: 1 at center, 0 at edges
    # We use a cubic hermite curve (smoothstep-like) for nicer transitions

    mask = 1 - np.clip(d, 0, 1)
    mask = mask * mask * (3 - 2 * mask)

    return mask


def generate_heightmap(
    size: int,
    octaves: int,
    scale: float = 100.0,
    seed: int | None = None,
    island_density: float = 0.0,
) -> np.ndarray:
    logger.debug(
        f"Generating heightmap: size={size}, octaves={octaves}, seed={seed}, "
        f"density={island_density}"
    )

    if seed is None:
        seed = random.randint(0, 10000)

    random.seed(seed)
    offset_x = random.randint(0, 100000)
    offset_y = random.randint(0, 100000)

    data = np.zeros((size, size))

    # Adjust scale relative to size to keep features looking similar across resolutions
    # A larger scale value in pnoise2 means "zoomed in" (larger features)
    # Actually pnoise2(x/scale) -> larger scale = lower frequency = larger features.
    for y in range(size):
        for x in range(size):
            # Generate Perlin noise
            # We map 0..size to coordinates.
            nx = (x + offset_x) / scale
            ny = (y + offset_y) / scale

            # Fetch noise value (typically -1.0 to 1.0)
            val = pnoise2(
                nx,
                ny,
                octaves=octaves,
                persistence=0.5,
                lacunarity=2.0,
                repeatx=1024,
                repeaty=1024,
                base=0,
            )

            # Normalize roughly to 0..1 (pnoise is -1..1)
            # Add island_density to shift the landmass up or down
            data[y][x] = (val + 1 + island_density) / 2

    # Apply Island Mask
    mask = generate_island_mask(size)

    # Combine: Map = Noise * Mask
    # This ensures the edges are always low (water) and center is high (land)
    data = data * mask

    return data


def create_figure(heightmap: np.ndarray) -> Figure:
    fig = Figure(figsize=(6, 6))
    ax = fig.subplots()

    ax.set_title("Island Map")
    # 'terrain' colormap works well: Blue -> Green -> Brown -> White
    # We assume < 0.2 is deep water, < 0.4 shallow water, > 0.4 land
    ax.imshow(heightmap, cmap="terrain", interpolation="bilinear", vmin=0, vmax=1)
    fig.colorbar(ax.images[0], ax=ax, label="Elevation")
    ax.axis("off")
    return fig


def render_map_to_png(
    size: int,
    octaves: int,
    filename: str,
    seed: int | None = None,
    island_density: float = 0.0,
) -> None:
    logger.info(
        f"Rendering map to file: {filename} (size={size}, octaves={octaves}, "
        f"seed={seed}, density={island_density})"
    )
    heightmap = generate_heightmap(
        size, octaves, scale=size / 4, seed=seed, island_density=island_density
    )
    fig = create_figure(heightmap)
    FigureCanvasAgg(fig).print_png(filename)
    logger.success(f"Map saved to {filename}")


def render_map_to_buffer(
    size: int,
    octaves: int,
    seed: int | None = None,
    island_density: float = 0.0,
) -> io.BytesIO:
    logger.info(
        f"Rendering map to buffer (size={size}, octaves={octaves}, "
        f"seed={seed}, density={island_density})"
    )
    heightmap = generate_heightmap(
        size, octaves, scale=size / 4, seed=seed, island_density=island_density
    )
    fig = create_figure(heightmap)
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    output.seek(0)
    logger.success("Map rendered to buffer")
    return output
