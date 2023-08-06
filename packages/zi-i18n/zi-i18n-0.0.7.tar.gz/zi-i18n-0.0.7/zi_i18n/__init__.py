"""
Copyright (c) 2020 null2264

This file is part of zi-i18n.

zi-i18n is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

zi-i18n is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with zi-i18n.  If not, see <https://www.gnu.org/licenses/>
"""

__title__ = 'zi-i18n'
__author__ = 'null2264'
__license__ = 'GPL-3.0-or-Later'
__copyright__ = 'Copyright 2020 null2264'
__version__ = '0.0.7'

from collections import namedtuple
import logging

from .i18n import I18n
from .object import Translation

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=0, micro=7, releaselevel='alpha', serial=0)

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
    
# locale = I18n("test/locale", "id_ID")
# print(locale.latency())
# locale.change_lang("id_ID")
# print(locale.translate("example.text"))
# locale.change_lang("pl")
# print(locale.translate("example.test"))
