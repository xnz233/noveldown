from .base import BaseRule
from .biquge345 import Biquge345

RULE_CLASSES = [Biquge345]

__all__ = ['RULE_CLASSES','BaseRule']