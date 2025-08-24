# Base image URI and version arguments
ARG IMAGE_URI_PREFIX=public.ecr.aws/docker/library/python
ARG PYTHON_VERSION=3.11
ARG IMAGE_URI_SUFFIX=-slim

FROM ${IMAGE_URI_PREFIX}:${PYTHON_VERSION}${IMAGE_URI_SUFFIX}

# Operating system dependencies
# hadolint ignore=DL3013,DL3042
RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    && apt-get autoremove -y \
    && pip install -U pip \
    && rm -rf /var/lib/apt/lists/*

# Application directory
WORKDIR /usr/local/lib/hcn
RUN python -m venv .venv \
    && .venv/bin/pip install -U pip \
    && .venv/bin/pip install poetry \
    && .venv/bin/poetry config virtualenvs.in-project true --local

# Copy pyproject.toml and poetry.lock, install project dependencies
COPY pyproject.toml poetry.lock README.md ./
RUN .venv/bin/poetry install --no-root --without=dev \
    && ln -s "$(realpath .venv/bin/hcn)" /usr/local/bin/hcn

# Copy the rest of the application
COPY . .

RUN .venv/bin/poetry install --without=dev \
    && useradd -m hcn \
    && mkdir -p /home/hcn \
    && chown -R hcn:hcn /home/hcn

USER hcn

WORKDIR /home/hcn

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/hcn", "api"]
