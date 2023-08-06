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

import json
import os
import re
import time

from .object import Translation


LANG = os.getenv("LANG").split(".")[0] or "en_US"


class I18n:
    def __init__(self, directory: str = "locale", language: str = LANG):
        self.dir = directory or "."
        self.def_lang = LANG or "en_US"
        self.languages = []
        self.suffix = ".zi.lang"
        files = os.listdir(self.dir)
        for f in files:
            if f.endswith(self.suffix):
                self.languages.append(f)
        self.translation = {}
        self.change_lang(language)

    def fetch_translations(self, text: str = None, count: int = None):
        if not text:
            return
        lang = self.lang
        if self.lang + self.suffix not in self.languages:
            import warnings

            warnings.warn(f"Language '{self.lang}' Not Found")
            lang = "en_US"

        def fetch(query):
            regex = r"^<(.)(\S*): \"(.*)\">"
            match = re.search(regex, query)

            if not match:
                regex = r"^<(.)(\S*): ({(.*)})>"
                match = re.search(regex, query)

            match_res = None
            if match:
                match_res = match.groups()

            if match_res and match_res[1] == text:
                if match_res[0] == "!":
                    return Translation(match_res[1], match_res[2], match_res[0])
                elif match_res[0] == "%":
                    pluralized = self.pluralize(match_res[2], count)
                    if pluralized:
                        return Translation(match_res[1], pluralized, match_res[0])

        for i in self.read:
            res = fetch(i)
            if res:
                return res
        return Translation(text, type="?")

    def pluralize(self, text: str, count: int):
        if count is None:
            return None
        _json = json.loads(text)
        if count > 1:
            return _json.get("many", None)
        elif count == 1:
            return _json.get("one", None)
        elif count < 1:
            return _json.get("zero", None)
        else:
            return None

    def change_lang(self, language: str):
        self.lang = language

        self.fallback = open(
            f"{self.dir}/{self.def_lang}{self.suffix}", "r"
        ).readlines()

        if self.lang == self.def_lang:
            self.read = self.fallback
        else:
            try:
                self.read = open(f"{self.dir}/{language}{self.suffix}", "r").readlines()
            except FileNotFoundError:
                self.read = self.fallback

        if self.read != self.fallback:
            self.read += self.fallback

    def translate(self, text: str, count: int = None):
        return self.fetch_translations(text, count)

    @property
    def latency(self):
        start = time.perf_counter()
        with self.translate("latency.test"):
            end = time.perf_counter()
            latency = end - start
            return latency

    # translate alias
    t = translate
