import logging

import yaml

from plugins import tts, stt
from conversation import Conversation
from mic import Mic
from text_input import TextInput


class Jane(object):
    def __init__(self, options={}):
        self._logger = logging.getLogger(__name__)

        # Read config
        config_file = options['config']
        self._logger.debug("Trying to read config file: '%s'", config_file)
        try:
            with open(config_file, "r") as f:
                self.config = yaml.safe_load(f)
        except OSError:
            self._logger.error("Can't open config file: '%s'", config_file)
            raise

        try:
            stt_engine_slug = self.config['stt_engine']
        except KeyError:
            stt_engine_slug = 'sphinx'
            self._logger.warning("stt_engine not specified in profile, defaulting " +
                                 "to '%s'", stt_engine_slug)
        stt_engine_class = stt.get_engine_by_slug(stt_engine_slug)

        try:
            slug = self.config['stt_passive_engine']
            stt_passive_engine_class = stt.get_engine_by_slug(slug)
        except KeyError:
            stt_passive_engine_class = stt_engine_class

        try:
            tts_engine_slug = self.config['tts_engine']
        except KeyError:
            tts_engine_slug = tts.get_default_engine_slug()
            self._logger.warning("tts_engine not specified in profile, defaulting " +
                                 "to '%s'", tts_engine_slug)
        tts_engine_class = tts.get_engine_by_slug(tts_engine_slug)

        # Initialize Mic
        if 'text' in options:
            self.input = TextInput()
        else:
            self.input = Mic(tts_engine_class.get_instance(),
                             stt_passive_engine_class.get_passive_instance(),
                             stt_engine_class.get_active_instance())

    def run(self):
        print 'Start'
        if 'first_name' in self.config:
            salutation = ("How can I be of service, %s?"
                          % self.config["first_name"])
        else:
            salutation = "How can I be of service?"
        self.input.say(salutation)

        conversation = Conversation("JANE", self.input, self.config)
        conversation.handleForever()
