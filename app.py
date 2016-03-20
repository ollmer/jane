#!/usr/bin/env python2
# -*- coding: utf-8-*-

import sys
import argparse
import logging
from src import jasperpath, diagnose
from src.jane import Jane

# Add jasperpath.LIB_PATH to sys.path
sys.path.append(jasperpath.LIB_PATH)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Jana Intelligent Voice Assistant')
    parser.add_argument('-t', '--text', action='store_true',
                        help='Use text input instead of a real microphone')
    parser.add_argument('--no-network-check', action='store_true',
                        help='Disable the network connection check')
    parser.add_argument('--diagnose', action='store_true',
                        help='Run diagnose and exit')
    parser.add_argument('--debug', action='store_true', help='Show debug messages')
    args = parser.parse_args()


    logging.basicConfig()
    logger = logging.getLogger()
    logger.getChild("client.stt").setLevel(logging.INFO)

    options = {
        'config': jasperpath.config('profile.yml')
    }
    if args.text:
        options['text'] = True

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if not args.no_network_check and not diagnose.check_network_connection():
        logger.warning("Network not connected. This may prevent Jasper from " +
                       "running properly.")

    if args.diagnose:
        failed_checks = diagnose.run()
        sys.exit(0 if not failed_checks else 1)

    try:
        app = Jane(options=options)
    except Exception:
        logger.error("Error occured!", exc_info=True)
        sys.exit(1)

    app.run()
