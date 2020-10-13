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

    def _connect_to_target_network(self, target_network, channel):
        # Send command to Bettercap to stop using mon0
        # Disable monitor mode: `ifconfig mon0 down && iw dev mon0 del`
        # Check to ensure monitor mode is indeed disabled
        # Set wlan0 channel
        # Update wpa_supplicant.conf file
        # Start wpa_supplicant service
        # Connect to wifi: `wpa_cli -i wlan0 reconfigure`
        
    def _restart_monitor_mode():
        # Stop wpa_supplicant service and ensure its process is killed
        # Start monitor mode: `iw phy "$(iw phy | head -1 | cut -d" " -f2)" interface add mon0 type monitor && ifconfig mon0 up`
        # Send command to Bettercap to use mon0
        
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
            if signal_strength > self.options['minimum-signal-strength']:
                _stop_monitor_mode()
                _connect_to_target_network(home_network, channel)
                #_restart_monitor_mode when some conditions are met
            else:
                logging.info("The signal strength of %s is too low (%s)" % (home_network, signal_strength))
        else:
            logging.info("%s NOT FOUND inside of %s" % (home_network, detected_networks))
        pass
