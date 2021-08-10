# -*- coding: utf-8 -*-
from rdflib import Literal, URIRef
from EpsUtil import draw_rectangle
from EpsUtil import draw_text
from EpsUtil import text_length_in_picture
from Resource import Resource
from NodeType import NodeType

import logging
logger = logging.getLogger(__name__)
colors = ["0.9 0.8 0.9", "0.8 0.9 0.9", "0.9 0.9 0.8"]

class ResourceNode(Resource):
    """
    グラフ上のRDFリソースを表現するオブジェクト。
    """

    MIN_WIDTH = 24
    HEIGHT = 24

    def __init__(self, data, x=0, y=0, label=None,
                 node_type=None):
        """

        Parameters
        ----------
        data:
            rdflibオブジェクト
        x, y:
            x, y座標
        label:
            人間が読めるラベル
        pos:
            座標
        """
        super().__init__(data, label=label)

        self.x, self.y = x, y
        self.node_type = node_type
        self.width = self.len_x+10
        self.height = 28

    def __str__(self):
        return f"<ResouceNode label={self.label}, (x, y)={(self.x, self.y)}"

    def export(self):
        """
        eps形式で出力可能な文字列を返す。

        Returns
        -------
        ret: str
            eps形式で出力可能な文字列。ヘッダー、フッターは含まれない。
        """
        ret = []

        # 色選択
        color = colors[0]
        if self.node_type is not None:
            if self.node_type == NodeType.LITERAL:
                color = colors[0]
            elif self.node_type == NodeType.CLASS:
                color = colors[1]
            else:
                color = colors[2]
        else:
            if isinstance(self.data, Literal):
                color = colors[0]
            else:
                color = colors[2]


        stroke_option = "\n".join(
            ["gsave",
             f"{color} setrgbcolor",
             "fill",
             "grestore",
             "0 0 0 setrgbcolor",
             "1 setlinewidth"])


        # 矩形を描く
        rect = draw_rectangle(self.x, self.y,
                              self.width, self.height,
                              stroke_option=stroke_option)
        ret.append(rect)

        # 文字を描く
        text = draw_text(self.x +self.width/2 - self.len_x/2,
                         self.y +self.height/2,
                         self.label)
        ret.append(text)

        return "\n".join(ret)

if __name__ == '__main__':
    resource_node = ResourceNode(data=None, label="iiiiiiii"*2)
    ret = ["""%!PS-Adobe-3.0 EPSF-3.0
%%BoundingBox: 0 0 300 300
"""]
    ret.append(resource_node.export())
    ret.append("\n%%EOF")
    print("\n".join(ret))
