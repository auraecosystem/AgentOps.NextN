git clone https://github.com/AgentOps-AI/AgentOps.Next.git
cd AgentOps.Next/app

# Copy environment files
cp .env.example .env
cp api/.env.example api/.env
cp dashboard/.env.example dashboard/.env.local
# Install shared tools (linting, formatting)
bun install

# Install Python development tools
uv pip install -r requirements-dev.txt
cd api

# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .

cd ..
cd dashboard

# Using bun (recommended)
bun install

# Or using npm
npm install

cd ..
# Terminal 1: API Server
cd api && uv run python run.py

# Terminal 2: Dashboard (in a new terminal)
cd dashboard && bun dev

# Terminal 3: Landing Page (optional, in a new terminal)
cd landing && bun dev

cd supabase
npx supabase db push

cd api
uv run python run.py
# Using pip and python directly
cd api
pip install -e .
python run.py

# Using uvicorn directly
cd api
uvicorn agentops.main:app --host 0.0.0.0 --port 8000 --reload

cd dashboard

# Using bun
bun install
bun dev

# Using npm
npm install
npm run dev

# Using yarn
yarn install
yarn dev
# Format code
just format

# Run linting
just lint

# Run tests
just test

# All-in-one quality check
just format && just lint && just test

# Apply Supabase migrations
cd supabase
npx supabase db push

# Reset database (development only)
npx supabase db reset

# Generate TypeScript types
npx supabase gen types typescript --local > types/database.types.ts
cd api

# Run all tests
pytest

# Run with coverage
pytest --cov=agentops

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v

cd dashboard

# Run all tests
bun test

# Run tests in watch mode
bun test --watch

# Run tests with coverage
bun test --coverage

# Run full test suite
just test

# Test API and dashboard separately
just api-test
just fe-test

cd api
python -m debugpy --listen 5678 --wait-for-client run.py

# Use bun instead of npm
cd dashboard
rm -rf node_modules
bun install

# Use uv for faster Python package management
uv pip install -e .
