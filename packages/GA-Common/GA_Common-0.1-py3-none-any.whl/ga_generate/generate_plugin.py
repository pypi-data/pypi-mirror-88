"""
@file ga_generate/generate_plugin.py
@author lipo
@description 生成器插件

@createtime
"""
from random import random

from ga.plugins import GeneratePlugin as BaseGeneratePlugin
from ga.population import Population
from ga.individual import Individual, IndividualMeta
from ga.phenotype import Phenotype


class GeneratePlugin(BaseGeneratePlugin):

    def __init__(
            self,
            individual_num: int,
            individual_meta: IndividualMeta
    ):
        """
        :param individual_num: 个体数量
        """
        self.individual_num = individual_num
        self.individual_meta = individual_meta

    def generate(self) -> Population:
        """
        种群生成算法
        """
        individuals = []

        for _ in range(self.individual_num):
            # setup phenotype
            phenotype = Phenotype()
            values = []
            for val_range in self.individual_meta.range_list:
                val = random() * (val_range[1] - val_range[0]) + val_range[0]
                values.append(val)
            phenotype.phenotype = values
            individual = Individual()
            individual.meta = self.individual_meta
            individual.phenotype = phenotype
            individuals.append(individual)

        population = Population()
        population.individuals = individuals
        return population
