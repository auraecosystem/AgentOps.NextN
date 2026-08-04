import arc_agi
from arcengine import GameAction

# Default: looks for games in "environment_files" directory
arc = arc_agi.Arcade()
env = arc.make("ab12-v1", seed=0, render_mode="terminal")

# Or specify a custom directory
arc = arc_agi.Arcade(environments_dir="./my_games")
env = arc.make("ab12-v1", seed=0, render_mode="terminal")

# Perform clicks (ACTION6 with x, y coordinates)
env.step(GameAction.ACTION6, data={"x": 32, "y": 32})
