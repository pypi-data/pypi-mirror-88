"""
@author lipo
@file ga/genetype.py
@description 基础基因型文件

@cratetime Wed, 14 Oct 2020 15:10:38 +0800
"""


class Genotype:
    _code = None

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code
