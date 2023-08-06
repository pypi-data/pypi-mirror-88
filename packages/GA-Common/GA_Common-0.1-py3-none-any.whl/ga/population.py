"""
@author lipo
@file ga/population.py
@description 种群对象

@cratetime Wed, 14 Oct 2020 15:37:28 +0800
@updatetime Fri, 20 Nov 2020 22:34:50 +0800
"""
from typing import List

from ga.exception import SelectorIsNone
from ga.plugins import CodecPlugin, CmPlugin
from ga.selector import Selector


class Population:
    """
    种群

    种群本质上是个体的集合
    主要是一个个体的集合
    """
    cm_plugin: CmPlugin = None  # 交叉变异插件
    codec_plugin: List[CodecPlugin] = None  # 编解码插件
    selector = None  # 环境选择器
    individuals = []  # 个体列表

    def __call__(
        self,
        cm_plugin: CmPlugin,
        codec_plugin: CodecPlugin
    ):
        self.cm_plugin = cm_plugin
        self.codec_plugin = codec_plugin
        self.bind()

    def cross(self):
        """
        种群内部交叉
        """
        self.cm_plugin.crossover(self.individuals)

    def mutate(self):
        """
        种群内变异
        """
        for individual in self.individuals:
            self.cm_plugin.mutate(individual)

    def select(self):
        """
        进行选择
        """
        if self.selector is None:
            raise SelectorIsNone("You should add selector first")
        self.individuals = self.selector.select(
            self.individuals)

    def use_selector(self, selector: Selector):
        """
        使用选择器

        :param selector: 环境选择器
        :return:
        """
        self.selector = selector

    def bind(self):
        # 绑定编解码插件
        for individual in self.individuals:
            individual.use(self.codec_plugin)

    def iter_next(
        self,
        codec_plugin: List[CodecPlugin]
    ):
        """
        种群迭代

        :param codec_plugin: 编解码插件
        """
        # 编解码器优化
        if self.codec_plugin != codec_plugin:
            self.codec_plugin = codec_plugin
            self.bind()  # 重新绑定编解码器

        self.cross()  # 进行交叉
        self.mutate()  # 引发变异
        self.select()  # 进行选择
