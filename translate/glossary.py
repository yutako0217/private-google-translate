#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint

from google.cloud import translate_v3 as translate

from logging import basicConfig, getLogger, DEBUG, ERROR

# これはすべてのファイルに書く
logger = getLogger(__name__)


class GlossaryConfig():
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def get_glossary_config(self):
        return self

    def set_glossary_name(self, name):
        self.name = name

    def set_glossary_location(self, location):
        self.location = location

    def info(self):
        logger.info("name:{},location:{}".format(self.name, self.location))


class GlossaryClient():

    def __init__(self, project, location):
        '''
        Constructor.

        :param project:
        :param location:
        '''
        self.project_id = project
        self.location = location
        self.client = translate.TranslationServiceClient()
        self.parent = self.client.location_path(project, location)

    def list_glossary(self):
        '''
        List glossaries
        :return:
        '''
        glossary_list = []
        print('{:<32}{}'.format("Glossary Name", "Glossary Path"))
        for element in self.client.list_glossaries(self.parent):
            path = element.name
            name = path.split('/')[-1]
            glossary_list.append(name)

        return glossary_list

    def describe_glossary(self, glossary_name):
        '''
        Describe glossary info
        :param glossary_name:
        :return:
        '''
        glossary_path = self.__get_glossary_path(glossary_name)
        logger.log(DEBUG, glossary_path)
        response = self.client.get_glossary(glossary_path)
        return response

    def create_glossary(self, glossary_name, input_uri, source_lang_code, target_lang_code):
        name = self.client.glossary_path(self.project_id, self.location, glossary_name)

        language_codes_set = translate.types.Glossary.LanguageCodesSet(
            language_codes=[source_lang_code, target_lang_code])
        gcs_source = translate.types.GcsSource(input_uri=input_uri)

        input_config = translate.types.GlossaryInputConfig(gcs_source=gcs_source)

        glossary = translate.types.Glossary(name=name,
                                            language_codes_set=language_codes_set,
                                            input_config=input_config)

        operation = self.client.create_glossary(parent=self.parent, glossary=glossary)

        result = operation.result(timeout=180)
        print(result)
        # [END translate_create_glossary_beta]

    def __get_glossary_path(self, glossary_name):
        return self.client.glossary_path(
            self.project_id, self.location, glossary_name  # The location of the glossary
        )
