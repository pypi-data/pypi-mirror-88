from ga.plugins.plugin_type import PluginType


class Plugin:
    plugin_name = ""
    plugin_type = PluginType.Undefined

    @classmethod
    def use(cls, name: str):
        # 选择需要的插件
        _ins = None
        for _subcls in cls.__subclasses__():
            if _subcls.plugin_name == name:
                _ins = _subcls()
                break
        return _ins


class CodecPlugin(Plugin):
    plugin_type = PluginType.Codec

    def encode(self, phonetype):
        return phonetype

    def decode(self, genotype):
        return genotype


class CmPlugin(Plugin):
    plugin_type = PluginType.Cm

    def mutate(self, individual):
        """
        变异流程

        :param individual 个体
        """
        pass

    def crossover(self, individuals):
        """
        交叉

        :param individuals 个体列表
        """
        pass


class IterPlugin(Plugin):
    plugin_type = PluginType.Iter

    def __call__(self, ga):
        """
        挂载ga对象，执行迭代流程
        """
        # 进行下一步迭代流程
        self.ga = ga
        self.iter_next()

    def iter_next(self):
        pass


class ParamPlugin(Plugin):
    plugin_type = PluginType.Param

    def param_input(self):
        pass

    def param_output(self):
        pass


class GeneratePlugin(Plugin):
    plugin_type = PluginType.Generate

    def generate(self):
        """
        返回生成的种群

        :return Pupolation 种群
        """
        pass
