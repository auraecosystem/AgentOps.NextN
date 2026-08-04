def _check_win(self) -> bool:
        """Check if all targets have been removed."""
        return len(self.current_level._sprites) == 0
