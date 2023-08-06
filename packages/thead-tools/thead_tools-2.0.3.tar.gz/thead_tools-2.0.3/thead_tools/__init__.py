import codecs
import sys
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
# ssl._create_default_https_context = ssl._create_unverified_context

from .log import logger
from .toolchain import *
from .tools import *
from .command import *
from .progress import *
from .subcmds import all_commands
from .cmd import *
