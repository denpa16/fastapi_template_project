FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS=ignore
ENV CURL_CA_BUNDLE=""
ENV POETRY_VIRTUALENVS_CREATE=true

EXPOSE 8000/tcp
RUN apt-get update -y --no-install-recommends
RUN apt-get install -y --no-install-recommends \
    curl `# для установки poetry` \
    git `# для установки зависимостей из git` \
    gcc `# для cryptography`
RUN pip install --user --no-cache-dir poetry==1.6

ENV PATH="${PATH}:/root/.local/bin"

COPY pyproject.toml poetry.lock /app/
WORKDIR /app/
RUN poetry install --no-interaction --no-ansi
COPY wait-for /usr/bin/
RUN chmod +x /usr/bin/wait-for
COPY / /app/
RUN chmod +x entrypoint.*
