FROM python:3.10 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10

WORKDIR /venhapararecomb

COPY --from=requirements-stage /tmp/requirements.txt /venhapararecomb/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /venhapararecomb/requirements.txt

COPY . /venhapararecomb

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]