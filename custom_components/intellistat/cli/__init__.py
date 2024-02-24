import platform as p
import logging
from os import system, path, getcwd
from time import sleep
import subprocess, sys

def setup():
    """
    Setup the script
    """
    log = logging.getLogger(__name__)
    if p.system() != "Linux":
        log.warn("You're using the setup script on a non-linux environment. Proceed at your own caution")

    system('mkdir -p ./custom_components/intellistat/translations')
    system('cp ./custom_components/intellistat/strings.json ./custom_components/intellistat/translations/en.json')

def dev():
    """
    You need to hit ctrl + c multiple times to actual kill it
    """
    while True:
        setup()
        try:
            process = subprocess.Popen(["hass", "-c", ".homeassistant"])
            process.wait()
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
        except KeyboardInterrupt:
            print("Sleeping for 1 second, hit ctrl + c again to exit")
            sleep(1)
