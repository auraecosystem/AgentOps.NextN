def generate_sprites(self) -> None:
           """Generate a random set of sprites based on the seed."""
           # Determine number of sprites
           cell_count = self.current_level.grid_size[0] * self.current_level.grid_size[1]
           sprite_count = cell_count // 64  
           for idx in range(sprite_count):
               scale = self._rng.randint(MIN_SIZE, MAX_SIZE)
               color = self._rng.choice(SPRITE_COLORS)
               x = self._rng.randint(0, self.current_level.grid_size[0] - 1)
               y = self._rng.randint(0, self.current_level.grid_size[1] - 1)
               # Create the sprite setting color, scale, and position then add it to the level
               sprite = sprites[f"sprite-1"].clone().color_remap(None, color).set_scale(scale).set_position(x, y)
               self.current_level.add_sprite(sprite)
