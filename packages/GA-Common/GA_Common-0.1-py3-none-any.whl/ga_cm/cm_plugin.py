"""
@author lipo
@file ga_cm/cm_plugin.py
@description 交叉变异插件

@createtime Thu, 26 Nov 2020 16:55:15 +0800
@updatetime Tue, 01 Dec 2020 21:21:02 +0800
"""
from random import random, sample, randint

from ga.individual import Individual
from ga.genotype import Genotype
from ga.plugins import CmPlugin as BaseCmPlugin


class CmPlugin(BaseCmPlugin):

    def __init__(self, mutate_rate: float, crossover_rate: float):
        """
        :param mutate_rate: 变异率(0 ~ 1)
        :param crossover_rate: 交叉率(0 ~ 1)
        """
        self.mutate_rate = mutate_rate  # 变异率
        self.crossover_rate = crossover_rate  # 交叉率

    def cross(self, i1, i2):
        gen1 = i1.genotype
        gen2 = i2.genotype

        code_seq1 = gen1.code
        code_seq2 = gen2.code

        code_length = len(code_seq1)
        size = randint(1, code_length)
        start_idx = max(randint(-size, code_length), 0)
        end_idx = min(start_idx + size, code_length)

        code_seq1[start_idx: end_idx], code_seq2[start_idx: end_idx] = \
            code_seq2[start_idx: end_idx], code_seq1[start_idx: end_idx]

        i1.phenotype = None
        i2.phenotype = None

    def crossover(self, individuals):
        """
        群体交叉

        默认交叉只产生一个个体，个体基因组合来自于父体的混合
        交叉后的子代会替代父代的基因

        :param individuals: 个体列表
        """
        cross_count = max(
            int(len(individuals) * self.crossover_rate / 2) * 2, 2)
        cross_individuals = sample(individuals, cross_count)
        cross_pair = zip(cross_individuals[::2], cross_individuals[1::2])

        for i1, i2 in cross_pair:
            # 交叉每一对个体
            self.cross(i1, i2)

    def mutate(self, individual: Individual):
        """
        个体变异

        默认只考虑二进制编码的变异流程

        :param individual: 变异个体
        """
        # 获取基因型
        genotype: Genotype = individual.genotype
        code_seq = genotype.code
        mutate_flag = False

        for code_idx, code in enumerate(code_seq):
            if random() < self.mutate_rate:
                mutate_flag = True  # 设定突变标志
                code_seq[code_idx] = not code

        if mutate_flag:
            # 删除个体表现型
            individual.phenotype = None
