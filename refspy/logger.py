"""
Package-level logging
"""

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # default
logger.propagate = False
