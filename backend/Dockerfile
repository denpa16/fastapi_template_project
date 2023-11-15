FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

RUN mkdir /app_dir/
COPY pyproject.toml poetry.lock /app_dir/
WORKDIR /app_dir/
RUN poetry install --no-interaction --no-ansi
COPY . /app_dir/

CMD ["alembic upgrade head"]
CMD ["uvicorn", "--reload", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
