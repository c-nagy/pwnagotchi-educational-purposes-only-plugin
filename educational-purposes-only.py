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
        
    def on_wifi_update(self, agent, access_points):
        detected_networks = str(access_points)
        home_network = self.options['home-network']
        if home_network in network_list:
            logging.info("FOUND %s inside of %s" % (home_network, network_list))
        else:
            logging.info("%s NOT FOUND inside of %s" % (home_network, network_list))
        pass                
        # signal_strength = X
        # channel = X
        # stop_monitor_interface OS command
        # set wlan0 channel OS command
        # create wpa_supplicant.conf file
        # start wpa_supplicant service OS command
        # sudo wpa_cli -i wlan0 reconfigure
