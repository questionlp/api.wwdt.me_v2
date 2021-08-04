# -*- coding: utf-8 -*-
# Copyright (c) 2018-2021 Linh Pham
# api.wwdt.me is relased under the terms of the Apache License 2.0
"""Gunicorn Configuration File"""

# Make a copy of this file and name it `gunicorn.conf.py` in order
# for it to be picked up by Gunicorn upon startup. Update any of
# the settings below with the appropriate values for the environment
# this application will be running in.
#
# For more information, on what configuration settings are available,
# refer to the Gunicorn documentation site at:
# https://docs.gunicorn.org/en/stable/settings.html#config-file

bind = "unix:/tmp/gunicorn-wwdtmapi.sock"
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = ".log/access.log"
errorlog = ".log/error.log"
umask = 0o007
