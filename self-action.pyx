def step(self) -> None:
        """Process game logic for each step."""

        # 1. Check action type - GameAction.ACTION6 is the click action
        if self.action.id == GameAction.ACTION6:
            # 2. Get coordinates - Extract x, y from action.data
            x = self.action.data.get("x", 0)
            y = self.action.data.get("y", 0)

            # 3. Convert coordinates - display_to_grid() handles camera scaling
            coords = self.camera.display_to_grid(x, y)

            if coords:
                grid_x, grid_y = coords

                # 4. Find sprite - Check if click hit any sprite
                clicked_sprite = self.current_level.get_sprite_at(grid_x, grid_y)
                if clicked_sprite:
                    # 5. Remove sprite - Update level state
                    self.current_level.remove_sprite(clicked_sprite)

                    # 6. Check win - Advance to next level if condition is met
                    if self._check_win():
                        self.next_level()

        # 7. Complete action - Always call self.complete_action()
        self.complete_action()
