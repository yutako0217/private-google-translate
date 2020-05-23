FROM python:3.7-slim
ARG project_dir=/projects/
WORKDIR /$project_dir
COPY . /$project_dir/

RUN pip install -r requirements.txt
#COPY key.json key.json
#ENV GOOGLE_APPLICATION_CREDENTIALS key.json
ENV PROJECT_ID yutty-project-1
ENV BUCKET_NAME translate-advanced
CMD ["python", "app.py"]