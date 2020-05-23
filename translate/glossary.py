#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pprint import pprint

from google.cloud import translate_v3 as translate

from logging import basicConfig, getLogger, DEBUG, ERROR

# これはすべてのファイルに書く
logger = getLogger(__name__)


class GlossaryConfig():
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location

    def get_glossary_config(self):
        return self

    def set_glossary_name(self, name: str):
        self.name = name

    def set_glossary_location(self, location: str):
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

    def __get_glossary_path(self, glossary_name):
        return self.client.glossary_path(
            self.project_id, self.location, glossary_name  # The location of the glossary
        )

