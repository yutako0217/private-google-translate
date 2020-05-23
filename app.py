import os

from flask import Flask, render_template, request, make_response, json

app = Flask(__name__)
from translate.client import TranslateClient
from translate.glossary import GlossaryConfig, GlossaryClient
from google.cloud import storage as gcs

PROJECT_ID = os.getenv('PROJECT_ID', None)
GLOSSARY_LOCATION = os.getenv('GLOSSARY_LOCATION', "us-central1")
BUCKET_NAME = os.getenv('BUCKET_NAME', None)

if PROJECT_ID is None or BUCKET_NAME is None:
    exit(1)


@app.route('/')
def hello_world():
    client = GlossaryClient(PROJECT_ID, GLOSSARY_LOCATION)
    glossary_list = client.list_glossary()
    return render_template("index.html", glossaries=glossary_list)


@app.route('/glossarycat', methods=["POST"])
def glossarycat():
    translated = None
    if request.method != 'POST':
        return ""

    content = request.json
    glossaryname = content['glossaryname']
    glossary_client = GlossaryClient(PROJECT_ID, GLOSSARY_LOCATION)
    glosasry_detail = glossary_client.describe_glossary(glossaryname)
    print(glosasry_detail)
    input_uri = glosasry_detail.input_config.gcs_source.input_uri
    glossary_input = __get_gcs_input(input_uri)
    return glossary_input


@app.route('/translate', methods=["POST"])
def translate():
    translated = None
    if request.method == 'POST':
        content = request.json
        contents = content['text']
        glossaryname = content['glossaryname']
        client = TranslateClient(PROJECT_ID, GLOSSARY_LOCATION)

        if glossaryname == "" or glossaryname == "---":
            translated = client.simple_translate(contents, "ja", "en", None)
        else:
            glossary_config = GlossaryConfig(glossaryname, GLOSSARY_LOCATION)
            translated = client.simple_translate(contents, "ja", "en", glossary_config)
        print(translated)
    merged_string = ''.join(translated)
    return merged_string


def __get_gcs_input(path):
    bucket_name = path.split("/")[2]
    client = gcs.Client(PROJECT_ID)
    bucket = client.get_bucket(bucket_name)

    filename = path.replace('gs://{}/'.format(bucket_name), '')
    blob = gcs.Blob(filename, bucket)
    content = blob.download_as_string()
    return content.decode()


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
