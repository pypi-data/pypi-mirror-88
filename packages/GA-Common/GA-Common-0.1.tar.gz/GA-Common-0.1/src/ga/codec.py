"""
@author lipo
@file ga/codec.py
@description 编解码器

@createtime Wed, 14 Oct 2020 15:20:26 +0800
@updatetime Thu, 10 Dec 2020 00:18:31 +0800
"""
from ga.genotype import Genotype
from ga.phenotype import Phenotype
from ga.individual import IndividualMeta


class Codec:
    """
    编解码器

    用于种群中个体的编解码流程
    """

    def encode(self, phenotype: Phenotype, meta: IndividualMeta) -> Genotype:
        """
        编码流程，用于将表现型编码为基因型

        :param phenotype: 表现型
        :param meta: 个体元信息

        :return Genotype: 返回编码后的基因型对象
        """

    def decode(self, genotype: Genotype, meta: IndividualMeta) -> Phenotype:
        """
        解码流程，用于将基因型解码为表现型

        :param genotype: 基因型
        :param meta: 个体元信息

        :return Phenotype: 返回表现型对象
        """
