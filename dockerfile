FROM python:3.10

WORKDIR /code

# Copiar archivos necesarios
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
RUN mkdir -p /code/temp_files

# Establecer las variables de entorno en el contenedor
ENV GOOGLE_APPLICATION_CREDENTIALS="${GOOGLE_APPLICATION_CREDENTIALS}"
ENV GCP_PROJECT_ID="${GCP_PROJECT_ID}"
ENV SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_EMAIL}"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
