FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

COPY . .

RUN python -m spacy download en_core_web_sm

EXPOSE 8000

CMD ["uvicorn", "claimchecker.api.main:app", "--host", "0.0.0.0", "--port", "8000"]