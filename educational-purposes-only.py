# educational-purposes-only performs automatic wifi authentication and internal network recon
# Install dependencies: apt update; apt install nmap macchanger
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import pwnagotchi
import logging
import subprocess
import os
import requests
import time

READY = True

class EducationalPurposesOnly(plugins.Plugin):
    __author__ = '@nagy_craig'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'A plugin to automatically authenticate to known networks and perform internal network recon'
    
    def _connect_to_target_network(self, network_name, channel):
        global READY
        READY = False
        logging.info("READY state set to \"%b\" while attempting to connect to network..." % READY)
        logging.info("Starting connection to target network on channel %d!" % channel) 
        logging.info("Telling Bettercap to pause wifi recon...")
        requests.post('http://127.0.0.1:8081/api/session', data='{"cmd":"wifi.recon off"}', auth=('pwnagotchi', 'pwnagotchi'))
        logging.info("Ensuring all wpa_supplicant processes are terminated...")
        subprocess.Popen('systemctl stop wpa_supplicant; killall wpa_supplicant', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(5)
        logging.info("Disabling monitor mode by reloading the brcmfmac driver...")
        subprocess.Popen('modprobe --remove brcmfmac; modprobe brcmfmac', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(5)
        # Ensures the driver gets loaded successfully:
        while "No such device" in os.popen('ifconfig wlan0 up 2>&1').read():
            logging.info("Reloading brcmfmac driver again...")
	        subprocess.Popen('modprobe --remove brcmfmac; modprobe brcmfmac', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
	        time.sleep(5)
        logging.info("Reloading brcmfmac driver again because sometimes it gets stuck on the first reload...")
        subprocess.Popen('modprobe --remove brcmfmac; modprobe brcmfmac', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(5)
        logging.info("Randomizing the MAC address prior to bringing up the wlan0 interface...")
        subprocess.Popen('macchanger -A wlan0', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(5)
        logging.info("Bringing up wlan0 interface...")
        subprocess.Popen('ifconfig wlan0 up', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(3)
        logging.info("Ensuring wlan0 interface is up...")
        subprocess.Popen('ifconfig wlan0 up', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(5)
        logging.info("Setting the wlan0 channel to match the target access point...")
        subprocess.Popen("iwconfig wlan0 channel %d" % channel, shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        subprocess.Popen('ifconfig wlan0 up', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(5)
        logging.info("Writing to the wpa_supplicant.conf file...")
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", 'w') as wpa_supplicant_conf:
            wpa_supplicant_conf.write("ctrl_interface=DIR=/var/run/wpa_supplicant\nupdate_config=1\ncountry=GB\n\nnetwork={\n\tssid=\"%s\"\n\tpsk=\"%s\"\n}\n" % (network_name, self.options['home-password']))
        logging.info("Starting wpa_supplicant background process and ensuring wlan0 is up again...")
        subprocess.Popen('ifconfig wlan0 up', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        subprocess.Popen('wpa_supplicant -u -s -c /etc/wpa_supplicant/wpa_supplicant.conf -i wlan0 &', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(5)
        logging.info("Connecting to wifi and ensuring wlan0 is up one more time...")
        subprocess.Popen('ifconfig wlan0 up', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        subprocess.Popen('wpa_cli -i wlan0 reconfigure', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(5)
        logging.info("Trying to get an IP address on the network via DHCP...")
        subprocess.Popen('dhclient wlan0', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        time.sleep(5)
        logging.info("Running dhclient once again to be safe...")
        subprocess.Popen('dhclient wlan0', shell=True, stdin=None, stdout=open("/dev/null", "w"), stderr=None, executable="/bin/bash")
        READY = True
        
    def _restart_monitor_mode(self):
        # Stop wpa_supplicant processes:
        os.popen('systemctl stop wpa_supplicant; killall wpa_supplicant')
        # Restart potentially buggy driver:
        os.popen('modprobe --remove brcmfmac && modprobe brcmfmac')
        # Randomize MAC address of wlan0 again:
        os.popen('macchanger -A wlan0')
        # Ensure wlan0 interface is up:
        os.popen('ifconfig wlan0 up')
        # Start monitor mode:
        os.popen('iw phy "$(iw phy | head -1 | cut -d" " -f2)" interface add mon0 type monitor && ifconfig mon0 up')
        # Send command to Bettercap to resume wifi recon (using mon0):
        requests.post('http://127.0.0.1:8081/api/session', data='{"cmd":"wifi.recon on"}', auth=('pwnagotchi', 'pwnagotchi'))
        
    def _internal_network_scans(network_name):
        #nmap_cmd = 'nmap --top-ports=100 $(ip r | grep wlan0 | awk "{print $1}") -oA /root/%s' % network_name)
        aquatone_cmd = 'X'
    
    def on_loaded(self):
        logging.info("educational-purposes-only loaded")

    def on_ui_setup(self, ui):
        pass

    def on_unload(self, ui):
        pass

    def on_ui_update(self, ui):
        # If not connected to a wireless network and mon0 doesn't exist, run _restart_monitor_mode function
        if "Not-Associated" in os.popen('iwconfig wlan0').read() and "Monitor" not in os.popen('iwconfig mon0').read():
            self._restart_monitor_mode()
            
    def on_wifi_update(self, agent, access_points):
        global READY
        logging.info("Wifi state updating!")
        logging.info("READY state is %b" % READY)
        if READY == True and "Not-Associated" in os.popen('iwconfig wlan0').read():
            for network in access_points:
                if network['hostname'] == self.options['home-network']:
                    logging.info("%s is nearby! Signal strength is %d and channel is %d." % (self.options['home-network'], network['rssi'], network['channel']))
                    if network['rssi'] >= self.options['minimum-signal-strength']:
                        self._connect_to_target_network(network['hostname'], network['channel'])
                    else:
                        logging.info("Unfortunately, the signal strength of %s is currently %d, which is weaker than the minimum set in config.toml (%d)." % (network['hostname'], network['rssi'], self.options['minimum-signal-strength']))
