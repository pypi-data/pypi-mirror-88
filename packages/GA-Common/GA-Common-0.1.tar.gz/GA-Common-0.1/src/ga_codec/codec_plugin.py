"""
@file ga_codec/code_plugin.py
@author lipo

编解码插件
@createtime
"""
from ga.genotype import Genotype
from ga.phenotype import Phenotype
from ga.plugins import CodecPlugin as BaseCodecPlugin
from ga.individual import IndividualMeta


class CodecPlugin(BaseCodecPlugin):
    def encode(self, phenotype: Phenotype, meta: IndividualMeta):
        """
        将表现型编码为基因型

        :param phenotype: 表现型
        :param meta: 个体元信息
        """
        code = []
        for val, val_range, bit_count in zip(
                phenotype.phenotype, meta.range_list, meta.bit_count):
            max_size = 2 ** bit_count
            feature_num = int(max_size * (val - val_range[0]) / (val_range[1] - val_range[0]))
            for i in range(bit_count):
                code.append(feature_num >> i & 0b1 == 1)
        return code

    def decode(self, genotype: Genotype, meta: IndividualMeta):
        """
        将基因型解码为表现型

        :param genotype: 基因型
        :param meta: 个体元信息
        """
        val = []
        code = genotype.code
        cursor = 0
        for val_range, bit_count in zip(meta.range_list, meta.bit_count):
            base_code = code[cursor: cursor + bit_count]
            max_size = 2 ** bit_count - 1
            feature_num = 0
            for idx, c in enumerate(base_code):
                if c:
                    feature_num += 2 ** idx
            scale_num = min(feature_num / max_size, 1)
            value = (val_range[1] - val_range[0]) * scale_num + val_range[0]
            val.append(value)
            cursor += bit_count
        return val
