import argparse
import random
import uuid

from magrathea.database import SessionLocal
from magrathea.maps.map import Map
from magrathea.maps.rendering_engine import render_map_to_buffer


def seed_maps(
    count: int = 5, size: int = 128, octaves: int = 4, island_density: float = 0.0
) -> None:
    db = SessionLocal()
    try:
        print(f"Pre-generating {count} maps...")
        for i in range(count):
            seed = random.randint(0, 1000000)
            print(f"  [{i + 1}/{count}] Generating with seed {seed}...")

            buf = render_map_to_buffer(
                size, octaves, seed=seed, island_density=island_density
            )

            map_id = str(uuid.uuid4())
            new_map = Map(
                id=map_id,
                size=size,
                octaves=octaves,
                seed=seed,
                island_density=island_density,
                data=buf.getvalue(),
                is_pregenerated=True,
            )
            db.add(new_map)
        db.commit()
        print(f"Successfully added {count} maps to the pool.")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()


def cli() -> None:
    parser = argparse.ArgumentParser(description="Pre-generate maps for the database.")
    parser.add_argument(
        "--count", type=int, default=5, help="Number of maps to generate"
    )
    parser.add_argument("--size", type=int, default=128, help="Size of the map")
    parser.add_argument(
        "--octaves", type=int, default=4, help="Number of octaves for noise generation"
    )
    parser.add_argument(
        "--island-density",
        type=float,
        default=0.0,
        help="Island density adjustment (float)",
    )

    args = parser.parse_args()

    seed_maps(
        count=args.count,
        size=args.size,
        octaves=args.octaves,
        island_density=args.island_density,
    )
