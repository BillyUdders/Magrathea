BIOMES = {
    (1, 1, 1): "Ocean",
    (4, 4, 4): "RAINFOREST",
}


class NoiseMap:
    def __init__(self, seed: int) -> None:
        self.octaves = 4
        self.seed = seed


class WorldMap:
    def __init__(
        self,
        size: int = 256,
        seed_height: int = 0,
        seed_heat: int = 0,
        seed_wet: int = 0,
    ) -> None:
        self.size = size
        self.heightmap = self.generate_map(seed=seed_height)
        self.heat_map = self.generate_map(seed=seed_heat)
        self.wet_map = self.generate_map(seed=seed_wet)
        self.levels: dict = {"height": [], "heat": [], "wet": []}

    def generate_map(self, seed: int) -> NoiseMap:
        return NoiseMap(seed=seed)

    # # get the biome based on the internal maps
    # def get_biome_from_point(x, y):

    #     # use the noise function to generate levels at the point
    #     # height = OpenSimplex.noise2d()
    #     # heat = OpenSimplex.noise2d()
    #     # wet = OpenSimplex.noise2d()

    #     if height < self.levels["height"][0]:
    #         height_level = 0

    #     if heat > self.levels["heat"][1]:
    #         heat_level = 1

    #     # (height_level, heat_level, wet_level)
    #     return BIOMES[(1, 2, 3)]
