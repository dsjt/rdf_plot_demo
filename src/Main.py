# -*- coding: utf-8 -*-
import argparse
from collections import defaultdict
import logging
import rdflib
from rdflib import RDF
from collections import Counter
from collections import deque
from EpsUtil import text_length_in_picture
from EpsUtil import export_eps
from Mapping import Mapping
from ResourceNode import ResourceNode
from ResourceLink import ResourceLink
from NodeType import NodeType

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

INF = float('inf')

def parse_arguments():
    """
    引数パーサー
    """
    parser = argparse.ArgumentParser(description='turtle形式のrdfを作図するデモ')
    parser.add_argument('-i', '--input', default="tmp.ttl",
                        help="入力ファイル(turtle)")
    parser.add_argument('-o', '--output', default=None,
                        help="出力ファイル(eps)")
    return parser.parse_args()


def load_turtle(fn):
    """
    パスを引数で受け取り、turtleファオイルを読み込んで、rdflibグラフオブジェクトを返す。
    """
    g = rdflib.Graph().parse(fn, format="turtle")
    logger.info("turtleのロード完了")
    return g

def get_start_point(E: list[list]):
    """
    隣接リストを受け取り、入次数が小さいノードを返す。
    """
    c = Counter()
    for targets in E:
        c += Counter(targets)

    sorted_V = sorted((c[i], i) for i in range(len(E)))
    min_in_degree, _ = sorted_V[0]
    return [k for v, k in sorted_V if min_in_degree == v]

def main():
    args = parse_arguments()

    # turtleファイルの読み込み
    g = load_turtle(args.input)
    mn = g.namespace_manager


    # 隣接リストによるグラフ構造の作成
    mapping = Mapping()
    for s, p, o in g:
        if p == RDF.type:
            continue
        mapping.register(s)
        mapping.register(o)
    E = [[] for _ in range(len(mapping))]
    for s, p, o in g:
        if p == RDF.type:
            continue
        si = mapping(s)
        oi = mapping(o)
        E[si].append(oi)
    logger.info("隣接リストの構成完了")
    # 型は取り分けておく
    object_class = {}
    for s, o in g[:RDF.type:]:
        object_class[mapping(s)] = mapping(o)

    # グラフから次数が小さいノードを取得する。複数可。
    roots = get_start_point(E)
    logger.info(roots)
    logger.info([(i, mapping.rev(i)) for i in roots])

    # 描画位置の計算
    x, y = 0, 0
    dx, dy = 10, 40
    visited = [False]*len(E)# 訪問済みオブジェクトを管理
    # 描画オブジェクト群
    resource_nodes = [None]*len(E)

    # 描画オブジェクトの作成とy座標の決定
    stack = roots.copy()
    while stack:
        v = stack.pop()
        if visited[v]:
            continue
        # dfs追加
        for u in E[v]:
            if visited[u]:
                continue    # ループは切る
            stack.append(u)
        visited[v]=True

        # ノードの作成
        obj = mapping.rev(v)
        rn = ResourceNode(obj, label=obj.n3(mn))
        resource_nodes[v] = rn

        # yの決定
        rn.y = y
        y -= dy

    # xの決定
    visited = [False]*len(E)
    stack = deque(roots)
    while stack:
        v = stack.popleft()
        if visited[v]:
            continue
        for u in E[v]:
            if visited[u]:
                continue
            stack.append(u)
        visited[v] = True

        if len(E[v]) == 0:
            continue

        for u in E[v]:
            lm = 0
            for p in g[mapping.rev(v)::mapping.rev(u)]:
                lm = max(text_length_in_picture(p.n3(mn)), lm)
        for u in E[v]:
            resource_nodes[u].x = resource_nodes[v].x+lm+20\
                +min(10, resource_nodes[v].width*0.25)


    logger.info("\n".join([str(rn) for rn in resource_nodes]))

    # 型の追加
    class_nodes = [None]*len(object_class)
    for i, (v, cu) in enumerate(object_class.items()):
        obj = mapping.rev(cu)
        cn = ResourceNode(obj, label=obj.n3(mn),
                          node_type=NodeType.CLASS)
        cn.x = resource_nodes[v].x + resource_nodes[v].width + 10
        cn.y = resource_nodes[v].y
        class_nodes[i] = cn

    # リンク用のオブジェクトの作成
    visited = [False]*len(E)
    stack = roots.copy()
    links = []
    while stack:
        v = stack.pop()
        if visited[v]:
            continue
        # dfs追加
        for u in E[v]:
            if visited[u]:
                continue    # ループは切る
            stack.append(u)
        visited[v]=True


        for u in E[v]:
            if visited[u]:
                continue
            for p in g[mapping.rev(v)::mapping.rev(u)]:
                link = ResourceLink(resource_nodes[v],
                                    resource_nodes[u],
                                    p,
                                    label=p.n3(mn))
                links.append(link)
                break

    eps = export_eps(resource_nodes+class_nodes, links)
    print(eps)
    return

if __name__ == '__main__':
    main()
