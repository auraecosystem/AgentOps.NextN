# Base sprite template - single pixel will be cloned, scaled, and recolored
sprites = {
    "sprite-1": Sprite(
        pixels=[
            [9],
        ],
        name="sprite-1",
        visible=True,
        collidable=True,
    ),
}

# Create levels array with all level definitions
levels = [
    # Level 1
    Level(
        sprites=[],
        grid_size=(8, 8),
    ),
    Level(
        sprites=[],
        grid_size=(16, 16),
    ),
    Level(
        sprites=[],
        grid_size=(24, 24),
    ),
    Level(
        sprites=[],
        grid_size=(32, 32),
    ),
    Level(
        sprites=[],
        grid_size=(64, 64),
    ),
]
