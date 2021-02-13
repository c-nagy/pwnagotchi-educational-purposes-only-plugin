# Pwnagotchi educational-purposes-only.py Plugin

This plugin allows your Pwnagotchi to detect your home network, pause wifi monitor mode, and associate to the network. It intelligently resumes monitor mode when connection to the home network is lost. <3 pull requests.

## Install Dependencies

Nmap and Macchanger must be installed on your Pwnagotchi:

```

apt update; apt install nmap macchanger

```

## Install and Configure Plugin

1. While SSH'd in to the Pwnagotchi, create a new folder for third-party Pwnagotchi plugins: `mkdir /root/custom_plugins/`

1. Grab the `educational-purposes-only.py` file from this Github repo and put it into that custom plugins directory.

1. Edit `/etc/pwnagotchi/config.toml` and change the `main.custom_plugins` variable to point to the custom plugins directory you just created: `main.custom_plugins = "/root/custom_plugins/"`

1. In the same `/etc/pwnagotchi/config.toml` file, add the following lines to enable and configure the plugin:

```

main.plugins.educational-purposes-only.enabled = true
main.plugins.educational-purposes-only.home_network = "Home Network SSID"
main.plugins.educational-purposes-only.home-password = "Home Network Password" # FIXME: use consistent hyphen or underscores in variable names 
main.plugins.educational-purposes-only.minimum-signal-strength = -75  # Minimum accepted RSSI (should be a negative integer)

```

Reboot the Pwnagotchi to ensure the plugin is initialized.
