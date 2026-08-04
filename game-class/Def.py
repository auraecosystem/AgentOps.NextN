class Ab12(ARCBaseGame):
    """Click-to-remove game with seeded random sprite generation."""

    def __init__(self, seed: int = 0) -> None:
        self._rng = random.Random(seed)
    
        # Create camera with background and padding colors
        camera = Camera(
            background=BACKGROUND_COLOR,
            letter_box=PADDING_COLOR,
            width=8,
            height=8,
        )

        # Initialize base game
        super().__init__(
            game_id="ab12",
            levels=levels,
            camera=camera,
        )
