# Private Google Translate
Private Google Translate provides private translation environment on Google Cloud Platform.
* Using Translation API Advanced
* Running on GAE or Cloud Run, so you can have dedicated translation with pay as you go.
* Easy to create, delete and confirm Glossary.

# Setup on GAE

1. Enable Translation API
```bash
gcloud services enable translate.googleapis.com
```

2. Create Google Cloud Storage Bucket.
```bash
gsutil mb gs://<BUCKET_NAME_FOR_STORE_GLOSSARY>
```

3. Update app.yaml with your <YOUR_PROJECT_ID> and <BUCKET_NAME_FOR_STORE_GLOSSARY>
```
runtime: python37
service: parivate-google-translate
env_variables:
  PROJECT_ID: '<YOUR_PROJECT_ID>'
  BUCKET_NAME: '<BUCKET_NAME_FOR_STORE_GLOSSARY>'
entrypoint: gunicorn -b :8080 app:app
```

4. Deploy to GAE
```
gcloud app deploy
```

5. Setup Firewall

# Setup on CloudRun

1. Enable Translation API
```bash
gcloud services enable translate.googleapis.com
```

2. Create Google Cloud Storage Bucket.
```bash
gsutil mb gs://<BUCKET_NAME_FOR_STORE_GLOSSARY>
```

3. At your local environment(or Cloudshell), you need to make docker images as following command.
```bash
docker build -t gcr.io/<YOUR_PROJECT_ID>/private-google-translate:v1 .
```

4. Push docker image to Google Container Registry
```bash
docker push gcr.io/<YOUR_PROJECT_ID>/private-google-translate:v1
```

5. Deploy Cloud Run with environment variables
```bash
gcloud run deploy gcr.io/<YOUR_PROJECT_ID>/private-google-translate:v1 --platform=managed --port=8080 --set-env-vars=PROJECT_ID=<YOUR_PROJECT_ID>,BUCKET_NAME=<BUCKET_NAME_FOR_STORE_GLOSSARY> --project <YOUR_PROJECT_ID> --region us-central1
```

