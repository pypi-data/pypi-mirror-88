"""
@author lipo
@file ga/selector.py
@description 生物选择器

@createtime Wed, 14 Oct 2020 15:16:33 +0800
"""
from typing import List

from ga.individual import Individual


class Selector:

    def select(
        self,
        individuals: List[Individual]
    ) -> List[Individual]:
        """
        @name select
        @description 对种群进行选择人

        @parameter population 生成的种群对象

        @return Population 返回的新种群
        """
        pass
