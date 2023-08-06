"""
@file ga_selector/selector.py
@author lipo
@description 默认轮盘选择器

@creattime
"""
from random import choices
from typing import Callable, List

from ga.individual import Individual
from ga.selector import Selector as BaseSelector


class Selector(BaseSelector):

    def __init__(self, get_fitness: Callable):
        self.get_fitness = get_fitness

    def select(
        self,
        individuals: List[Individual]
    ) -> List[Individual]:
        individual_count = len(individuals)
        new_individuals = []

        # 计算个体适应度
        fitness = []
        for individual in individuals:
            fitness.append(self.get_fitness(individual))

        per_individuals = choices(
            individuals, fitness, k=individual_count
        )

        for individual in per_individuals:
            new_individuals.append(individual.duplicate())

        return new_individuals
