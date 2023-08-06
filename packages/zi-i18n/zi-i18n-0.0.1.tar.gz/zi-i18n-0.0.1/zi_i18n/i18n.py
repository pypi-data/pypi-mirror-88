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

import os
import re
import time

from .object import Translation


class I18n:
    def __init__(self, directory: str = "locale", language: str = "en_US"):
        self.dir = directory or "."
        self.languages = []
        self.suffix = ".zi.lang"
        files = os.listdir(self.dir)
        for f in files:
            if f.endswith(self.suffix):
                self.languages.append(f)
        self.translation = {}
        self.change_lang(language)

    def fetch_translations(self, text: str = None):
        if not text:
            return
        lang = self.lang
        if self.lang + self.suffix not in self.languages:
            import warnings

            warnings.warn(f"Language '{self.lang}' Not Found")
            lang = "en_US"

        fallback = open(f"{self.dir}/en_US{self.suffix}", "r")
        fallback = fallback.readlines()

        if lang == "en_US":
            read = fallback
        else:
            read = open(f"{self.dir}/{lang}{self.suffix}", "r")
            read = read.readlines() or fallback
            if read != fallback:
                read += fallback
        
        def fetch(query):
            try:
                regex = r"^<(.)(\S*): \"(.*)\">"
                match = re.search(regex, query).groups()
            except AttributeError:
                return

            if match and match[1] == text:
                return Translation(match[1], match[2])
        
        for i in read:
            res = fetch(i)
            if res:
                return res
        return Translation(text)

    def change_lang(self, language: str):
        self.lang = language

    def translate(self, text: str):
        return self.fetch_translations(text)
    
    @property
    def latency(self):
        start = time.perf_counter()
        with self.translate("latency.test"):
            end = time.perf_counter()
            latency = end-start
            return latency
