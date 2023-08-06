"""
Clarisse

log module.
Process global logging behavior.

by 1MLightyears@gmail.com

on 20201214
"""

import logging
import logging.config
import sys
import json
import os

info = logging.info
warning = logging.warning
error = logging.error
critical = logging.critical
fatal = logging.fatal
debug = logging.debug

### log settings

with open('..'+os.sep+'log_config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
    logging.config.dictConfig(config)