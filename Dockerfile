
FROM python:3.12-slim


WORKDIR /app


RUN pip install --no-cache-dir pipenv


COPY Pipfile Pipfile.lock /app/


RUN pipenv --python $(which python) install --deploy --ignore-pipfile


COPY . /app/


EXPOSE 8000


CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
