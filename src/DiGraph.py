# -*- coding: utf-8 -*-
import logging
from collections import defaultdict
from collections import Counter
from collections import deque

logger = logging.getLogger(__name__)

class DiGraph(object):
    def __init__(self):
        self.E = defaultdict(list)
        self.V = 0
        pass

    def add_link(self, a, b):
        self.E[a].append(b)
        self.E[b]
        self.V = len(self.E)
        pass

    def add_node(self, a):
        self.E[a]               # 呼び出すのみ
        self.V = len(self.E)
        pass

    def get_root(self):
        """
        入次数が小さいノードを返す
        """
        c = Counter()
        for k, tos in self.E.items():
            for u in tos:
                c[u] += 1
        sorted_V = sorted([(c[v], v) for v in self.E])
        min_in_degree, _ = sorted_V[0] # 入次数の最小値
        ret = [k for v, k in sorted_V if min_in_degree == v]
        return ret


    def pre_order_gen(self):
        """
        DAGとみなしてdfs入り順に巡回する。ループは無視する
        """
        stack = self.get_root()
        visited = [False]*self.V
        order = []

        while stack:
            v = stack.pop()
            if visited[v]:      # ループの可能性を排除
                continue
            for u in self.E[v]:
                if visited[u]:
                    continue
                stack.append(u)
            visited[v] = True
            order.append(v)
            yield v
        logger.debug(f"pre {order=}")
        pass

    def post_order_gen(self):
        """
        DAGとみなしてdfs帰り順に巡回する。ループは無視する
        """
        roots = self.get_root()
        stack = []
        for r in roots:
            stack.append(~r)
            stack.append(r)
        visited = [False]*self.V
        order = []

        while stack:
            v = stack.pop()
            if v >= 0:
                if visited[v]:      # ループの可能性を排除
                    continue
                for u in self.E[v]:
                    if visited[u]:
                        continue
                    stack.append(~u)
                    stack.append(u)
                visited[v] = True
            else:
                order.append(v)
                yield ~v
        logger.debug(f"post {order=}")
        pass


    def bfs_order_gen(self):
        """
        幅優先探索順に巡回するジェネレータ
        """
        visited = [False]*self.V
        stack = deque(self.get_root())
        order = []
        while stack:
            v = stack.popleft()
            if visited[v]:
                continue
            for u in self.E[v]:
                if visited[u]:
                    continue
                stack.append(u)
            visited[v] = True
            order.append(v)
            yield v
        logger.debug(f"bfs {order=}")
        pass
