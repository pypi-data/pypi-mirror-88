from ga.plugins import IterPlugin as BaseIterPlugin


class StopIterPlugin(BaseIterPlugin):
    iter_count: int = 0  # 迭代次数

    def __init__(
            self,
            max_iter_count: int,

    ):
        """
        :param max_iter_count: 最大迭代次数
        """
        self.max_iter_count = max_iter_count

    def iter_next(self):
        self.iter_count += 1
        if self.iter_count >= self.max_iter_count:
            # 跳出循环
            raise StopIteration()
