import io
import random
from typing import cast

import numpy as np
from loguru import logger
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from opensimplex import OpenSimplex


# Candidate for garbage, this whole file needs TLC
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

    print("Hello Acheron")

    return cast(np.ndarray, mask)


def generate_heightmap(
    size: int,
    octaves: int,
    scale: float = 100.0,
    seed: int | None = None,
    island_density: float = 0.0,
    # float: water_level = 0.4
) -> np.ndarray:
    logger.debug(
        f"Generating heightmap: size={size}, octaves={octaves}, seed={seed}, "
        f"density={island_density}"
    )

    if seed is None:
        seed = random.randint(0, 10000)

    # Use a separate random generator for offsets to allow reproducible maps
    # independent of global random state if seed is provided.
    rng = random.Random(seed)
    offset_x = rng.randint(0, 100000)
    offset_y = rng.randint(0, 100000)

    # Initialize OpenSimplex with the seed
    gen = OpenSimplex(seed=seed)

    # Prepare coordinate arrays
    # 0..size -> scaled coordinates
    x_idx = np.arange(size)
    y_idx = np.arange(size)

    # Apply offsets and base scale
    # Matches original logic: nx = (x + offset_x) / scale + 20
    nx = (x_idx + offset_x) / scale + 20
    ny = (y_idx + offset_y) / scale

    heightmap = np.zeros((size, size))
    amplitude = 1.0
    frequency = 1.0
    max_value = 0.0

    # Fractal Brownian Motion (FBM)
    persistence = 0.5
    lacunarity = 2.0

    for _ in range(octaves):
        # noise2array takes (x_array, y_array) and returns (len(y), len(x))
        # We pass the scaled coordinates for this octave
        noise_layer = gen.noise2array(nx * frequency, ny * frequency)

        heightmap += noise_layer * amplitude
        max_value += amplitude

        amplitude *= persistence
        frequency *= lacunarity

    # Normalize roughly to -1..1
    if max_value > 0:
        heightmap /= max_value

    # Shift and normalize to 0..1 range with density adjustment
    # Original logic: (val + 1 + island_density) / 2
    heightmap = (heightmap + 1 + island_density) / 2

    heightmap = np.round(heightmap / 0.05) * 0.05

    # Apply Island Mask
    # mask = generate_island_mask(size)

    # Combine: Map = Noise * Mask
    data = heightmap

    return cast(np.ndarray, data)


def create_figure(heightmap: np.ndarray) -> Figure:
    fig = Figure(figsize=(6, 6))
    ax = fig.subplots()

    ax.set_title("Island Map")

    colors = [
        (0.0, "#1f4fff"),  # blue (deep water)
        (0.4, "#1f4fff"),  # blue (deep water)
        (0.5, "#f5e663"),  # yellow (sand)
        (0.55, "#4caf50"),  # green (grass)
        (0.8, "#0b3d0b"),  # dark green (dense forest)
        (1.0, "#0b3d0b"),  # dark green (dense forest)
    ]

    sea_sand_grass = LinearSegmentedColormap.from_list("sea_sand_grass", colors, N=256)

    # 'terrain' colormap works well: Blue -> Green -> Brown -> White
    # We assume < 0.2 is deep water, < 0.4 shallow water, > 0.4 land
    ax.imshow(heightmap, cmap=sea_sand_grass, interpolation="bilinear", vmin=0, vmax=1)
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
