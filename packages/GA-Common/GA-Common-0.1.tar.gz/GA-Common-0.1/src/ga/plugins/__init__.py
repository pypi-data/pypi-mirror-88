"""
主要负责四种类型的插件

主要包含以下类型
- 编解码插件
- 交叉/变异插件
- 迭代控制插件
- 参数解析器插件

@createtime Mon, 12 Oct 2020 17:50:33 +0800
"""
from ga.plugins.plugins import CodecPlugin, CmPlugin, \
    IterPlugin, ParamPlugin, GeneratePlugin


__all__ = (
    "CodecPlugin", "CmPlugin", "IterPlugin",
    "ParamPlugin", "GeneratePlugin"
)
