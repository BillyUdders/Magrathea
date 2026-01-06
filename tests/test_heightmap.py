import numpy as np

from magrathea.maps.rendering_engine import generate_heightmap


def test_heightmap_shape() -> None:
    size = 64
    hm = generate_heightmap(size, 2)
    assert hm.shape == (size, size)


def test_heightmap_range() -> None:
    size = 64
    hm = generate_heightmap(size, 2)
    # The output should be roughly within 0..1 due to masking and normalization
    assert np.all(hm >= 0.0)
    assert np.all(hm <= 1.0)


def test_heightmap_determinism() -> None:
    size = 32
    octaves = 2
    seed = 42

    hm1 = generate_heightmap(size, octaves, seed=seed)
    hm2 = generate_heightmap(size, octaves, seed=seed)

    assert np.array_equal(hm1, hm2), "Heightmaps with same seed should be identical"


def test_heightmap_variability() -> None:
    size = 32
    octaves = 2

    hm1 = generate_heightmap(size, octaves, seed=1)
    hm2 = generate_heightmap(size, octaves, seed=2)

    assert not np.array_equal(hm1, hm2), "Heightmaps with different seeds should differ"


def test_heightmap_density() -> None:
    size = 64
    octaves = 2
    seed = 100

    hm_low = generate_heightmap(size, octaves, seed=seed, island_density=-0.5)
    hm_high = generate_heightmap(size, octaves, seed=seed, island_density=0.5)

    # Higher density should generally result in higher average elevation
    # (masked areas are 0 though)
    # We should look at the center where mask is 1

    center = size // 2
    val_low = hm_low[center, center]
    val_high = hm_high[center, center]

    assert val_high > val_low, "Higher density should increase elevation"
