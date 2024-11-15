FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
RUN mkdir -p /code/temp_files

ENV GOOGLE_APPLICATION_CREDENTIALS="${GOOGLE_APPLICATION_CREDENTIALS}"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
