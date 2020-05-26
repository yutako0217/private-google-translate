import os
from builtins import Exception
from sys import exit

from flask import Flask, render_template, request, make_response, json
from translate.client import TranslateClient
from translate.glossary import GlossaryConfig, GlossaryClient
from google.cloud import storage as gcs
import datetime

app = Flask(__name__)

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


@app.route('/createglossary', methods=["POST"])
def glossarycreate():
    translated = None
    if request.method != 'POST':
        return ""

    content = request.json
    name = content['glossaryname']
    now = datetime.datetime.now().strftime("%Y%m%d%H%M")
    glossaryname = "{}-{}".format(name, now)
    glossaryinput = content['glossary_input']

    langcodeline = glossaryinput.split("\n")[0]
    source_lang_code = langcodeline.split(",")[0]
    target_lang_code = langcodeline.split(",")[1]

    # file = "gs://{}/{}".format(BUCKET_NAME, "{}.csv".format(glossaryname))
    gcs_input_uri = __create_file(glossaryname, glossaryinput)
    glossary_client = GlossaryClient(PROJECT_ID, GLOSSARY_LOCATION)
    result = glossary_client.create_glossary(glossaryname, gcs_input_uri, source_lang_code, target_lang_code)

    print(result)

    return "ok"


@app.route('/translate', methods=["POST"])
def translate():
    translated = None
    if request.method == 'POST':
        content = request.json
        contents = content['text']
        if contents == '':
            return ''
        glossaryname = content['glossaryname']
        language_from = content['from']
        language_to = content['to']
        if language_from == '':
            language_from = 'ja'
        if language_to == '':
            language_to = 'en'

        client = TranslateClient(PROJECT_ID, GLOSSARY_LOCATION)

        if glossaryname == "" or glossaryname == "---":
            translated = client.simple_translate(contents, language_to, language_from, None)
        else:
            glossary_config = GlossaryConfig(glossaryname, GLOSSARY_LOCATION)
            translated = client.simple_translate(contents, language_to, language_from, glossary_config)
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


def __create_file(filename, contents):
    try:
        client = gcs.Client(PROJECT_ID)
        bucket = client.get_bucket(BUCKET_NAME)
        blob = bucket.blob("{}.csv".format(filename))
        blob.upload_from_string(contents)
    except Exception as e:
        print(e)
        return ""
    return "gs://{}/{}.csv".format(BUCKET_NAME, filename)


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
