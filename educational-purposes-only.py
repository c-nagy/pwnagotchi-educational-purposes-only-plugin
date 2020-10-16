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

    def _connect_to_target_network(network_name, channel):
        # Send command to Bettercap to stop using mon0:
        requests.post('http://127.0.0.1:8081/api/session', data='{"cmd":"wifi.recon off"}', auth=('pwnagotchi', 'pwnagotchi'))
        # Disable monitor mode interface mon0 (this seems to be the most reliable method?):
        os.popen('modprobe --remove brcmfmac && modprobe brcmfmac')
        # Randomize wlan0 MAC address prior to connecting (the -A flag: use a random but real vendor string):
        os.popen('macchanger -A wlan0')
        # Ensure wlan0 interface is up:
        os.popen('ifconfig wlan0 up')
        # Set wlan0 channel to match AP. Can be verified by running `iwlist channel`:
        os.popen("iwconfig wlan0 channel %d" % channel)
        # Ensure buggy systemd service version of wpa_supplicant is disabled:
        os.popen('systemctl stop wpa_supplicant; killall wpa_supplicant')
        # Overwrite wpa_supplicant.conf file with creds:
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", 'w') as wpa_supplicant_conf:
            wpa_supplicant_conf.write("ctrl_interface=DIR=/var/run/wpa_supplicant\nupdate_config=1\ncountry=GB\n\nnetwork={\n\tssid=%s\n\tpsk=\"%s\"\n}\n" % (network_name, "password"))
        # Start wpa_supplicant background process:
        os.popen('wpa_supplicant -c /etc/wpa_supplicant/wpa_supplicant.conf -i wlan0 &')
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
        # Ensure wlan0 interface is up:
        os.popen('ifconfig wlan0 up')
        # Start monitor mode:
        os.popen('iw phy "$(iw phy | head -1 | cut -d" " -f2)" interface add mon0 type monitor && ifconfig mon0 up')
        # Send command to Bettercap to resume wifi recon (using mon0):
        requests.post('http://127.0.0.1:8081/api/session', data='{"cmd":"wifi.recon on"}', auth=('pwnagotchi', 'pwnagotchi'))
        
    def _internal_network_scans(network_name):
        nmap_cmd = 'nmap --top-ports=100 $(ip r | grep wlan0 | awk "{print $1}") -oA /root/%s' % network_name)
        aquatone_cmd = 'X'
    
    def on_loaded(self):
        logging.info("educational-purposes-only loaded")

    def on_ui_setup(self, ui):
        pass

    def on_unload(self, ui):
        pass

    def on_ui_update(self, ui):
        # If not connected to a wireless network and mon0 doesn't exist, run _restart_monitor_mode function
        # Might need to think of a way to prevent this from happening in the middle of the _connect_to_target_network function
        if "Not-Associated" in os.popen('iwconfig wlan0').read() and "Monitor" not in os.popen('iwconfig mon0').read():
            _restart_monitor_mode()
        
    def on_wifi_update(self, agent, access_points):
        home_network = self.options['home-network']
        if "Not-Associated" in os.popen('iwconfig wlan0').read():
            nearby_networks = json.loads(access_points) 
            for network in nearby_networks['aps']:
                if network['hostname'] == home_network:
                    logging.info("FOUND home network \"%s\" nearby. Details: %s" % (home_network, network))
                    signal_strength = network['rssi']
                    channel = network['channel']
                    if signal_strength >= self.options['minimum-signal-strength']:
                        _connect_to_target_network(network, channel)
                    else:
                        logging.info("The signal strength of %s is too low (%d)" % (home_network, signal_strength))
