# educational-purposes-only performs automatic wifi authentication and internal network recon
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import pwnagotchi
import logging
import os


class EducationalPurposesOnly(plugins.Plugin):
    __author__ = '@nagy_craig'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'A plugin to automatically authenticate to known networks and perform internal network recon'

    def on_loaded(self):
        logging.info("educational-purposes-only loaded")

    def on_ui_setup(self, ui):

    def on_unload(self, ui):

    def on_ui_update(self, ui):
