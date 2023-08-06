from __future__ import absolute_import, division, print_function

__version__ = "0.0.1.dev1"  # noqa

import logging
import sys

logger = logging.getLogger(__name__)  # noqa
logger.setLevel(logging.INFO)  # noqa
del logging  # noqa

if sys.platform.startswith("win"):
    from .windows import *
elif sys.platform.startswith("linux"):
    from .linux import *
elif sys.platform.startswith("darwin"):
    from .macos import *
else:
    raise ImportError('Unsupported Platform.')
