# Add to mix.exs
{:sprites, github: "superfly/sprites-ex"}

# Create a sprite
client = Sprites.new(System.get_env("SPRITE_TOKEN"))
Sprites.create(client, System.get_env("SPRITE_NAME"))

# Run Python
sprite = Sprites.sprite(client, System.get_env("SPRITE_NAME"))
{output, _} = Sprites.cmd(sprite, "python", ["-c", "print(2+2)"])
IO.write(output)
