from enum import auto, Flag


class PluginType(Flag):
    # 编解码器
    Codec = auto()
    # 交叉/变异插件
    Cm = auto()
    # 迭代控制插件
    Iter = auto()
    # 参数解析插件
    Param = auto()
    # 种群生成插件
    Generate = auto()
    # 未定义
    Undefined = auto()
