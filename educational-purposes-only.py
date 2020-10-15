# educational-purposes-only performs automatic wifi authentication and internal network recon
# Install dependencies: apt update; apt install nmap macchanger
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import pwnagotchi
import logging
import os
import requests
import json


class EducationalPurposesOnly(plugins.Plugin):
    __author__ = '@nagy_craig'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'A plugin to automatically authenticate to known networks and perform internal network recon'

    def _connect_to_target_network(self, target_network, channel):
        # Send command to Bettercap to stop using mon0:
        requests.post('http://127.0.0.1:8081/api/session', data='{"cmd":"wifi.recon off"}', auth=('pwnagotchi', 'pwnagotchi'))
        # Disable monitor mode interface mon0 (this seems to be the most reliable method?):
        os.popen('modprobe --remove brcmfmac && modprobe brcmfmac')
        # Randomize wlan0 MAC address (-A means a random but real vendor string is used) prior to connecting:
        os.popen('macchanger -A --bia wlan0')
        # Set wlan0 channel to match AP. Can be verified by running `iwlist channel`:
        os.popen("iwconfig wlan0 channel %d" % channel)
        # Update wpa_supplicant.conf file
        # Start wpa_supplicant service:
        os.popen('systemctl start wpa_supplicant')
        # Connect to wifi:
        os.popen('wpa_cli -i wlan0 reconfigure')
        
    def _restart_monitor_mode():
        # Stop wpa_supplicant service:
        os.popen('systemctl stop wpa_supplicant')
        # Ensure wpa_supplicant processes are killed:
        os.popen('killall wpa_supplicant')
        # Restart potentially buggy driver:
        os.popen('modprobe --remove brcmfmac && modprobe brcmfmac')
        # Randomize MAC address of wlan0 again:
        os.popen('macchanger -A --bia wlan0')
        # Start monitor mode:
        os.popen('iw phy "$(iw phy | head -1 | cut -d" " -f2)" interface add mon0 type monitor && ifconfig mon0 up')
        # Send command to Bettercap to resume wifi recon (using mon0):
        requests.post('http://127.0.0.1:8081/api/session', data='{"cmd":"wifi.recon on"}', auth=('pwnagotchi', 'pwnagotchi'))
        
    def _internal_network_scans():
        pass
    
    def on_loaded(self):
        logging.info("educational-purposes-only loaded")

    def on_ui_setup(self, ui):
        pass

    def on_unload(self, ui):
        pass

    def on_ui_update(self, ui):
        pass
        
    def on_wifi_update(self, agent, access_points):
        detected_networks = json.loads(access_points)
        home_network = self.options['home-network']
        if home_network in str(detected_networks):
            logging.info("FOUND %s inside of %s" % (home_network, detected_networks))
            # signal_strength = X
            # channel = X
            if signal_strength > self.options['minimum-signal-strength']:
                _connect_to_target_network(home_network, channel)
            else:
                logging.info("The signal strength of %s is too low (%s)" % (home_network, signal_strength))
        else:
            logging.info("%s NOT FOUND inside of %s" % (home_network, detected_networks))
