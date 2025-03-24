"""
Settings for the middleware service.
"""

import os

MIDDLEWARE_SERVICE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_FILE = os.path.join(MIDDLEWARE_SERVICE_DIR, "output.jsonl")
