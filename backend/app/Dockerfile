
# Use a minimal Python image with uv for dependency management
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Setup a non-root user for security
RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

# Set working directory
WORKDIR /app

# Enable bytecode compilation for performance
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
# Omit development dependencies by default
ENV UV_NO_DEV=1
# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Install dependencies using lockfile for reproducibility
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy project files (including .env for environment variables)
COPY . /app

# Install the project itself (editable mode)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Copy .env file if present (for local development)
COPY ../.env ./ || true

# Reset the entrypoint, don't invoke `uv` directly
ENTRYPOINT []

# Use the non-root user to run our application
USER nonroot

# Expose FastAPI default port
EXPOSE 8000

# Healthcheck for container monitoring (optional, can be removed if not needed)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

# Default: run FastAPI in dev mode with hot reload
# For production, override CMD to use: ["uv", "run", "fastapi", "run", "--host", "0.0.0.0", "app/app.py"]
CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0", "app/app.py"]
