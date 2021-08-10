# -*- coding: utf-8 -*-

from EpsUtil import draw_lines
from EpsUtil import draw_text
from Resource import Resource

import logging
logger = logging.getLogger(__name__)

class ResourceLink(Resource):
    """
    グラフ上のRDFリソース間のリンクを表現するオブジェクト
    """

    def __init__(self, subj, obj, data, label=None):
        super().__init__(data, label)
        self.subj = subj
        self.obj = obj
        pass

    def connection(self, obj):
        x = min(obj.x + obj.width*0.25, obj.x + 10)
        y = obj.y + obj.height/2
        return (x, y)

    def export(self):
        """
        eps形式で出力可能な文字列を返す。

        Returns
        -------
        ret: str
            eps形式で出力可能な文字列。ヘッダー、フッターは含まれない。
        """
        ret = []
        start = self.connection(self.subj)
        end = self.connection(self.obj)
        middle = (start[0], end[1])
        ret.append(draw_lines([start, middle, end]))
        ret.append(draw_text(middle[0], middle[1]+10, self.label))
        return "\n".join(ret)
