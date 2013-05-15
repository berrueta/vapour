#!/usr/bin/python

import os
import sys

root_path = os.path.dirname(__file__)
parent_path = os.path.join(root_path, "..")

sys.path.append(parent_path)
os.environ["DJANGO_SETTINGS_MODULE"] = "vapour.settings"

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

