"""
@author lipo
@file ga/ga.py
@description 基础的GA对象

@createtime Wed, 14 Oct 2020 15:35:22 +0800
@updatetime Fri, 20 Nov 2020 14:47:22 +0800
"""
from typing import Union, List

from ga.exception import IterStop
from ga.lib import Iterable
from ga.population import Population
from ga.plugins import CodecPlugin, CmPlugin, \
    IterPlugin, GeneratePlugin
from ga.selector import Selector


class GA(Iterable):
    population: Union[None, Population] = None

    def __init__(
        self,
        codec_plugin: Union[CodecPlugin, List[CodecPlugin]],
        cm_plugin: CmPlugin,
        iter_plugin: Union[IterPlugin, List[IterPlugin]],
        param_plugin: str,
        generate_plugin: Union[None, GeneratePlugin] = None
    ):
        """
        初始化ga算法模型
        :param codec_plugin: 绑定ga编解码器
        :param cm_plugin: ga交叉变异插件
        :param iter_plugin: 迭代控制器插件
        :param param_plugin: 参数解析插件
        :param generate_plugin: 种群生成插件
        """
        self.codec_plugin = codec_plugin \
            if isinstance(codec_plugin, list) else [codec_plugin]
        self.cm_plugin = cm_plugin
        self.iter_plugins = iter_plugin \
            if isinstance(iter_plugin, list) else [iter_plugin]
        self.param_plugin = param_plugin
        self.generate_plugin = generate_plugin

    def use_selector(self, selector: Selector):
        """
        使用环境选择器
        :param selector: 指定群体的选择器
        """
        if self.population is not None:
            self.population.use_selector(selector)

    def setup_population(
        self,
        population: Union[Population, None] = None
    ):
        """
        配置种群信息

        :param population: 生成的种群
        """
        if population is None and self.generate_plugin is not None:
            # 基于种群生成器，生成种群
            population = self.generate_plugin.generate()
        self.population = population
        self.population(self.cm_plugin, self.codec_plugin)

    def next(self):
        """
        步进GA算法流程
        """
        # 告知种群机进行下一次迭代
        self.population.iter_next(
            self.codec_plugin
        )

        try:
            # 使用迭代控制器构建迭代切面
            for _iter in self.iter_plugins:
                _iter(self)
        except IterStop:
            pass
