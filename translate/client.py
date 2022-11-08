#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from logging import basicConfig, getLogger, DEBUG, ERROR
from google.cloud import translate

# これはメインのファイルにのみ書く
from translate.glossary import GlossaryConfig

logger = getLogger(__name__)


class TranslateClient:
    def __init__(self, projectid, location):
        self.project_id = projectid
        self.location = location
        self.client = translate.TranslationServiceClient()
        self.parent = f"projects/{self.project_id}/locations/{self.location}"
        logger.debug("TranslateClient initialized")

    def get_glossary_config(self, glossary_name, glossary_location):
        return GlossaryConfig(glossary_name, glossary_location)

    def simple_translate(self, text, target_lang_code, source_lang_code=None, glossary_config = None):

        contents = [text]
        translatedlist = list()
        if glossary_config is not None:
            glossary_name = glossary_config.name
            glossary_location = glossary_config.location
            if source_lang_code == None:
                logger.log(ERROR, 'Source language code must be specified for requests that use glossaries.')
                exit()
            glossary_config = self.__glossary_config_for_translate(glossary_name, glossary_location)
            # response = self.client.translate_text(
            #     contents=[text],
            #     source_language_code=source_lang_code,
            #     target_language_code=target_lang_code,
            #     parent=self.parent,
            #     glossary_config=glossary_config,
            #     mime_type='text/plain'
            # )
            response = self.client.translate_text(
                request={
                    "contents": [text],
                    "target_language_code": target_lang_code,
                    "source_language_code": source_lang_code,
                    "parent": self.parent,
                    "glossary_config": glossary_config,
                }
            )
            logger.log(DEBUG, response)
            for translation in response.glossary_translations:
                translatedlist.append(translation.translated_text)
        else:
            response = self.client.translate_text(contents=contents,
                                                  target_language_code=target_lang_code,
                                                  parent=self.parent,
                                                  mime_type='text/plain')
            logger.log(DEBUG, response)
            for translation in response.translations:
                translatedlist.append(translation.translated_text)
        return translatedlist

    def __glossary_config_for_translate(self, glossary_name, glossary_location):
        glossary_path = self.client.glossary_path(
            self.project_id, glossary_location, glossary_name  # The location of the glossary
        )
        return translate.TranslateTextGlossaryConfig(glossary=glossary_path)
