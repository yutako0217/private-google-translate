FROM python:3.7-slim
ARG project_dir=/projects/
WORKDIR /$project_dir
COPY . /$project_dir/

RUN pip install -r requirements.txt

## For Run at local
#COPY key.json key.json
#ENV GOOGLE_APPLICATION_CREDENTIALS key.json
#ENV PROJECT_ID <YOUR_PROJECT_ID>
#ENV BUCKET_NAME <BUCKET_NAME_FOR_STORE_GLOSSARY>

CMD ["gunicorn","-b",":8080", "app:app"]
