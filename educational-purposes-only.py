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

    def _stop_monitor_mode():
        
    def _restart_monitor_mode():
    
    def on_loaded(self):
        logging.info("educational-purposes-only loaded")

    def on_ui_setup(self, ui):

    def on_unload(self, ui):

    def on_ui_update(self, ui):
        
    def on_wifi_update(self, agent, access_points):
        detected_networks = str(access_points)
        home_network = self.options['home-network']
        if home_network in detected_networks:
            logging.info("FOUND %s inside of %s" % (home_network, detected_networks))
            # signal_strength = X
            # channel = X
            # _stop_monitor_mode
            # set wlan0 channel command
            # create wpa_supplicant.conf file
            # start wpa_supplicant service
            # `wpa_cli -i wlan0 reconfigure` to connect
            # _restart_monitor_mode
        else:
            logging.info("%s NOT FOUND inside of %s" % (home_network, detected_networks))
        pass
