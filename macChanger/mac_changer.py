#!/usr/bin/env python
# address changing (module.function).
# ifconfig down to disable
# ifconfig up to enable

import subprocess
import optparse
import re


class ChangeMac:
    # options = ""
    # current_mac = ""

    def __init__(self):
        options = self.get_arguments()
        current_mac = self.get_current_mac(options.interface)
        print("Current MAC address = " + str(current_mac))
        self.change_mac(str(options.interface), str(options.new_mac))

    def get_arguments(self):
        # create an instance of option parser
        parser = optparse.OptionParser()
        parser.add_option("-i", "--interface", dest="interface", help="Interface: to change its MAC address")
        parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
        # options = variables, arguments = --i or --m
        (options, arguments) = parser.parse_args()
        if not options.interface:
            parser.error("[-] Please specify an interface, use --help for info")
        elif not options.new_mac:
            parser.error("[-] Please specify a new MAC address, use --help for info")
        return options

    def get_current_mac(self, interface):
        ifconfig_result = subprocess.check_output(["ifconfig", str(interface)])
        mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

        if mac_address_search_result:
            return mac_address_search_result.group(0)
        else:
            print("[-] Could not read MAC address.")
        return False

    def change_mac(self, interface, new_mac):
        print("[+] Changing MAC address for " + interface + " to " + new_mac)
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["ifconfig", interface, "up"])
        return True
