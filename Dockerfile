FROM python:3.11.0
WORKDIR /work
COPY pyproject.toml .
RUN python3 -m pip install --no-cache-dir --upgrade pip && python3 -m pip install --no-cache-dir .
