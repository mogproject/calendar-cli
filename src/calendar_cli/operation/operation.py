from __future__ import division, print_function, absolute_import, unicode_literals

from calendar_cli.util import CaseClass
from abc import ABCMeta, abstractmethod
import six


@six.add_metaclass(ABCMeta)
class Operation(CaseClass):
    """abstract operation class"""

    @abstractmethod
    def run(self):
        """do nothing by default"""
