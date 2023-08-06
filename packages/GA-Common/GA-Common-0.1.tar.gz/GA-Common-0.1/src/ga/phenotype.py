"""
@author lipo
@file ga/phenotype.py
@description 表现型文件

@createtime Wed, 14 Oct 2020 15:12:26 +0800
"""


class Phenotype:
    """
    表现型
    """
    meta_info = None
    _phenotype = None

    @property
    def phenotype(self):
        return self._phenotype

    @phenotype.setter
    def phenotype(self, value):
        self._phenotype = value
