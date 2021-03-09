#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import threading
import scanner
import proxies


def capture_args():
    parser = argparse.ArgumentParser(prog="Vulnerability Scanner",
                                     description="Scan a url for potential vulnerabilities.")
    parser.add_argument("-n", "--name", dest="scan_name", help="This is the name of the directory created to hold"
                        " scans for this project.")
    parser.add_argument("-t", "--target", dest="target_url", help="Target url e.g http://example.co.uk.")
    parser.add_argument("-d", "--depth", dest="proxy_count", help="Essentially how deep to go digging for proxies.")
    parser.add_argument("-c", "--cutoff", dest="time_to_cutoff", help="How long to wait for server response in proxy "
                        "testing. Default is 3 seconds, reducing this "
                        "will result in less usable proxies but "
                        "decrease execution time.")
    parser.add_argument("-v", "--verbose", dest="verbose", help="Whether to print proxy testing results as they "
                        "occur, or not. Default is off. Pass on for on.")
    parser.add_argument("-fN", "--filename", dest="proxy_filename", help='Filename for saving proxy list in proxies '
                        'directory. Default is \"proxies\".')
    parser.add_argument("-sD", "--subdomain", action="store_true", help="Must be passed to enable scanning for "
                        "subdomains.")
    parser.add_argument("-Dd", "--subdirectories", action="store_true", help="Must be passed to enable scanning for "
                        "directories and subdirectories.")
    parser.add_argument("-Cr", "--crawler", action="store_true", help="Must be passed to enable crawling URL "
                        "specified in -t.")
    parser.add_argument("-F", "--forms", action='store_true', default=False, help="Must be passed to extract forms "
                        "data from"
                        " specified url.")
    parser.add_argument("-Th", "--threads", default=8, dest="threads", help="This program uses threading. The default "
                        "is 8 threads.")
    parser.add_argument("-a", "--all", action="store_true", default=False, help="Performs all scans.")
    build_scan = parser.parse_args()
    if not build_scan.target_url:
        parser.error("\n[-] Please specify a target and a gateway, use --help for info\n")
    return build_scan


def setup_proxy():
    proxy_servers = proxies.ScannerProxies()
    proxy_servers.get_proxies()
    return proxy_servers


def run_program(user_args):
    for _ in range(int(user_args.threads)):
        thread = threading.Thread()
        thread.daemon = True
        thread.start()

    vuln_scanner = scanner.Scanner(user_args.target_url, user_args.scan_name, threading.current_thread().name)

    if user_args.subdomain or user_args.all:
        print(str(vuln_scanner.find_subdomains()))
    if user_args.subdirectories or user_args.all:
        print(str(vuln_scanner.find_directories()))
    if user_args.crawler or user_args.all:
        print(str(vuln_scanner.crawl_single_url()))
    if user_args.forms or user_args.all:
        print(str(vuln_scanner.extract_forms()))


args = capture_args()
# proxy = setup_proxy()
run_program(args)
