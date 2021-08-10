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
from DiGraph import DiGraph

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

def get_start_point(E, V):
    """
    隣接リストを受け取り、入次数が小さいノードを返す。
    """
    c = Counter()
    for targets in E.values():
        c += Counter(targets)
    sorted_V = sorted((c[i], i) for i in range(V))
    min_in_degree, _ = sorted_V[0]
    ret = [k for v, k in sorted_V if min_in_degree == v]
    logger.info(f"DAGの出発ノードの一覧を取得 {ret}")
    return ret

def main():
    args = parse_arguments()

    # turtleファイルの読み込み
    g = load_turtle(args.input)
    mn = g.namespace_manager

    # 隣接リストによるグラフ構造の作成
    tmap = Mapping()            # 型のマッピング
    rmap = Mapping()            # 型以外のリソースのマッピング
    object_class = {}

    dg = DiGraph()
    for s, p, o in g:
        if p == RDF.type:
            si = rmap.register(s)
            oi = tmap.register(o)
            object_class[si] = oi
        else:
            si = rmap.register(s)
            oi = rmap.register(o)
            dg.add_link(si, oi)
    logger.info("DAGの構成完了")

    # 描画位置の計算
    x, y = 0, 0
    dy = 40
    # 描画オブジェクト群
    resource_nodes = [None]*dg.V

    for v in dg.pre_order_gen():
        # ノードの作成
        obj = rmap.rev(v)
        rn = ResourceNode(obj, label=obj.n3(mn))
        resource_nodes[v] = rn
        # yの決定
        rn.y = y
        y -= dy

    # xの決定
    for v in dg.bfs_order_gen():
        lm = max([text_length_in_picture(p.n3(mn))
                  for u in dg.E[v]
                  for p in g[rmap.rev(v)::rmap.rev(u)]],
                 default=0)
        for u in dg.E[v]:
            resource_nodes[u].x = resource_nodes[v].x+lm+20\
                +min(10, resource_nodes[v].width*0.25)

    # 型の追加
    class_nodes = [None]*len(object_class)
    for i, (v, u) in enumerate(object_class.items()):
        obj = tmap.rev(u)
        cn = ResourceNode(obj, label=obj.n3(mn),
                          node_type=NodeType.CLASS)
        cn.x = resource_nodes[v].x + resource_nodes[v].width + 10
        cn.y = resource_nodes[v].y
        class_nodes[i] = cn

    # リンク用のオブジェクトの作成
    visited = [False]*len(dg.E)
    links = []
    for s, p, o in g:
        if p == RDF.type:
            continue
        link = ResourceLink(resource_nodes[rmap(s)],
                            resource_nodes[rmap(o)],
                            p, label=p.n3(mn))
        links.append(link)

    eps = export_eps(resource_nodes+class_nodes, links)
    print(eps)
    return

if __name__ == '__main__':
    main()
