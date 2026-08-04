def on_set_level(self, level: Level) -> None:
        """Called when the level is set."""
        # Generate sprites based on seed
        self.generate_sprites()
