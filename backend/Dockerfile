FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

WORKDIR /backend

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Copy lockfiles first
COPY pyproject.toml uv.lock ./

# Install dependencies (no cache mount - Railway compatible)
RUN uv sync --locked --no-install-project

# Copy rest of project
COPY . /backend

# Install project itself
RUN uv sync --locked

# Fix permissions
RUN chown -R nonroot:nonroot /backend/.venv

ENV PATH="/backend/.venv/bin:$PATH"

ENTRYPOINT []

USER nonroot

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
