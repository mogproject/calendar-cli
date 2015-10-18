from __future__ import division, print_function, absolute_import, unicode_literals

from abc import ABCMeta, abstractmethod
import six
from mog_commons.case_class import CaseClass


@six.add_metaclass(ABCMeta)
class Operation(CaseClass):
    """abstract operation class"""

    @abstractmethod
    def run(self):
        """do nothing by default"""
