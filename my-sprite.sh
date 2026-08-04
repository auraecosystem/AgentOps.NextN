# Create a new sprite
curl -X PUT https://api.sprites.dev/v1/sprites/my-sprite \
  -H "Authorization: Bearer $SPRITES_TOKEN"

# Execute a command
curl -X POST https://api.sprites.dev/v1/sprites/my-sprite/exec \
  -H "Authorization: Bearer $SPRITES_TOKEN" \
  -d '{"command": "echo hello"}'
