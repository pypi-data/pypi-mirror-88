"""
@author lipo
@file ga/invdividual.py
@description |
考虑到动态变异和动态交叉的流程，可以实现交叉率
和变异率的动态浮动，使得交叉变异过程能够在整个
系统演进过程中不断自行优化和退化

@createtime Mon, 12 Oct 2020 15:35:28 +0800
"""
from typing import Union, List

from ga.plugins import CodecPlugin
from ga.genotype import Genotype
from ga.phenotype import Phenotype


class IndividualMeta:
    type_list = []
    range_list = []
    bit_count = []


class Individual:
    """
    抽象的个体

    fitness 计算环境适应度的数值
    """
    codec_plugin: Union[None, List[CodecPlugin]] = None
    _phenotype: Union[None, Phenotype] = None
    _genotype: Union[None, Genotype] = None
    _meta: Union[None, IndividualMeta] = None

    @property
    def genotype(self) -> Genotype:
        """
        编码计算，并返回基因型对象

        :return Genotype: 基因型
        """
        if self._genotype is not None:
            return self._genotype

        self._genotype = Genotype()
        processed_phenotype = Phenotype()
        processed_phenotype.phenotype = self._phenotype.phenotype
        for cp in self.codec_plugin:
            processed_phenotype.phenotype = cp.encode(processed_phenotype, self.meta)

        self._genotype.code = processed_phenotype.phenotype
        return self._genotype

    @genotype.setter
    def genotype(self, value: Union[Genotype, None]):
        self._genotype = value

    @property
    def phenotype(self) -> Phenotype:
        """
        解码计算，并返回表现型对象

        :return Phenotype 表现型对象
        """
        if self._phenotype is not None:
            return self._phenotype

        self._phenotype = Phenotype()
        processed_genotype = Genotype()
        processed_genotype.code = self._genotype.code
        for cp in self.codec_plugin[::-1]:
            processed_genotype.code = cp.decode(processed_genotype, self.meta)

        self._phenotype.phenotype = processed_genotype.code
        return self._phenotype

    @phenotype.setter
    def phenotype(self, value: Union[Phenotype, None]):
        self._phenotype = value

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, value):
        self._meta = value

    def use(self, codec_plugin: List[CodecPlugin]):
        self.codec_plugin = codec_plugin

    def duplicate(self):
        """
        个体复制
        """
        instance = self.__class__()
        instance.codec_plugin = self.codec_plugin
        instance.meta = self.meta

        genotype = Genotype()
        genotype.code = [i for i in self.genotype.code]
        instance._genotype = genotype

        phenotype = Phenotype()
        phenotype.phenotype = [i for i in self.phenotype.phenotype]
        instance._phenotype = phenotype

        return instance
