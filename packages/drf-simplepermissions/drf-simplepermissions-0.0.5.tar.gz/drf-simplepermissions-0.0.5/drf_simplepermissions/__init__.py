import os
from .permissions import is_demo
from .permissions import SimplePermissions


__version__ = os.environ.get('PACKAGE_VERSION', '0.0.0'),
__all__ = ['SimplePermissions', 'is_demo']
