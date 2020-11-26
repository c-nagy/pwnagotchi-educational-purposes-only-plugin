# Pwnagotchi educational-purposes-only.py Plugin

This plugin allows your Pwnagotchi to detect your home network, intelligently pause wifi monitor mode, and associate to the network. <3 pull requests.

# Installation

1. SSH into your Pwnagotchi and create a new folder for third-party Pwnagotchi plugins. I use `/root/custom_plugins/` but it doesn't really matter: `mkdir /root/custom_plugins/`

1. Grab the `educational-purposes-only.py` file from this Github repo and put it into that custom plugins directory.

1. Edit `/etc/pwnagotchi/config.toml` and change the `main.custom_plugins` variable to point to the custom plugins directory you just created: `main.custom_plugins = "/root/custom_plugins/"`

1. In the same `/etc/pwnagotchi/config.toml` file, add the following line to enable the plugin:

```

main.plugins.educational-purposes-only.enabled = true

```

Once the above steps are completed, reboot the Pwnagotchi to ensure all changes are applied.
