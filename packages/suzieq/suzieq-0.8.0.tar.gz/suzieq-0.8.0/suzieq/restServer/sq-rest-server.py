#!/usr/bin/env python3

import uvicorn
import argparse
import sys
import yaml
import os
from suzieq.utils import validate_sq_config

from suzieq.restServer.query import app, get_configured_api_key, get_configured_log_level, get_log_file


def check_config_file(cfgfile):
    if cfgfile:
        with open(cfgfile, "r") as f:
            cfg = yaml.safe_load(f.read())

        validate_sq_config(cfg, sys.stderr)


def check_for_cert_files():
    if not os.path.isfile(os.getenv("HOME") + '/.suzieq/key.pem') or not \
            os.path.isfile(os.getenv("HOME") + '/.suzieq/cert.pem'):
        print("ERROR: Missing cert files in ~/.suzieq")
        sys.exit(1)


def get_log_config():
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config['handlers']['access']['class'] = 'logging.handlers.RotatingFileHandler'
    log_config['handlers']['access']['maxBytes'] = 10000000
    log_config['handlers']['access']['backupCount'] = 2
    log_config['handlers']['default']['class'] = 'logging.handlers.RotatingFileHandler'
    log_config['handlers']['default']['maxBytes'] = 10_000_000
    log_config['handlers']['default']['backupCount'] = 2

    log_config['handlers']['access']['filename'] = get_log_file()
    del(log_config['handlers']['access']['stream'])
    log_config['handlers']['default']['filename'] = get_log_file()
    del(log_config['handlers']['default']['stream'])

    return log_config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=str, help="alternate config file"
    )
    userargs = parser.parse_args()
    check_config_file(userargs.config)
    app.cfg_file = userargs.config
    get_configured_api_key()
    check_for_cert_files()

    uvicorn.run(app, host="0.0.0.0", port=8000,
                log_level=get_configured_log_level(),
                log_config=get_log_config(),
                ssl_keyfile=os.getenv("HOME") + '/.suzieq/key.pem',
                ssl_certfile=os.getenv("HOME") + '/.suzieq/cert.pem')
