FROM python:3.11-slim

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

RUN mkdir /app/
COPY pyproject.toml poetry.lock /app/
WORKDIR /app/
RUN poetry install --no-interaction --no-ansi
COPY . /app/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]