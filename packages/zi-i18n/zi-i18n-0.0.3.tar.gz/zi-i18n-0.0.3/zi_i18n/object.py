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

class Translation:
    def __init__(self, name, translate=None):
        self.name = name
        self.translate = translate or name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def __str__(self):
        return self.translate

    def __repr__(self):
        return f"<!{self.name}: \"{self.translate}\">"
