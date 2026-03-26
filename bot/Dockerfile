FROM harbor.pg.innopolis.university/docker-hub-cache/python:3.14-slim

WORKDIR /app

# Install uv using pip (avoids needing a separate image)
RUN pip install uv

# Copy bot files
COPY bot/pyproject.toml bot/uv.lock ./
RUN uv sync --frozen --no-dev

COPY bot/ .

CMD ["uv", "run", "bot_telegram.py"]
