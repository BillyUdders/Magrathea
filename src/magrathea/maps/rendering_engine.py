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

    # The noise library doesn't handle seeds directly in pnoise2 in a thread-safe
    # standardized way for all versions, but shifting coordinates by a large random
    # offset is a common trick. However, pnoise2 'base' parameter is often available.
    # Let's use coordinate offsets for robustness.

    if seed is None:
        seed = random.randint(0, 10000)

    random.seed(seed)
    offset_x = random.randint(0, 100000)
    offset_y = random.randint(0, 100000)

    # Secondary offsets for domain warping
    warp_offset_x = random.randint(0, 100000)
    warp_offset_y = random.randint(0, 100000)

    data = np.zeros((size, size))

    # For archipelagos, we want slightly higher frequency (smaller features)
    # so we reduce the effective scale.
    eff_scale = scale * 0.5

    # Adjust scale relative to size to keep features looking similar across resolutions
    # A larger scale value in pnoise2 means "zoomed in" (larger features)
    # Actually pnoise2(x/scale) -> larger scale = lower frequency = larger features.
    for y in range(size):
        for x in range(size):
            # Domain Warping:
            # 1. Get a low-frequency noise value to act as a coordinate displacement
            # We use a larger scale (lower freq) for the warp field
            warp_nx = (x + warp_offset_x) / (eff_scale * 2)
            warp_ny = (y + warp_offset_y) / (eff_scale * 2)

            q = pnoise2(warp_nx, warp_ny, octaves=2, persistence=0.5, base=0)

            # 2. Apply displacement to the main noise coordinates
            # The factor '4.0 * q' determines how strong the swirl/warp is.
            nx = (x + offset_x) / eff_scale + (4.0 * q)
            ny = (y + offset_y) / eff_scale + (4.0 * q)

            # 3. Main Terrain Noise
            val = pnoise2(
                nx,
                ny,
                octaves=octaves,
                persistence=0.55,
                lacunarity=2.1,
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

    ax.set_title("Archipelago Map")
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
