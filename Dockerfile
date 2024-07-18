FROM python:3.11-slim
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PATH "/app/scripts:${PATH}"
WORKDIR /app

# Install Hatch
RUN set +x \
    && apt update \
    && apt upgrade -y \
    && apt install -y curl gcc build-essential \
    && pip install hatch \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY pyproject.toml /app/
RUN hatch env create

# Prepare entrypoint
ADD . /app/
RUN chmod +x scripts/* \
    && hatch run pip install .

ENTRYPOINT ["docker-entrypoint.sh"]
