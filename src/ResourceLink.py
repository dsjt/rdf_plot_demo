from EpsUtil import draw_lines
from EpsUtil import draw_text

import logging
logger = logging.getLogger(__name__)

class ResourceLink(object):
    """
    グラフ上のRDFリソース間のリンクを表現するオブジェクト
    """

    def __init__(self, subj, obj, data, label=None):
        self.subj = subj
        self.obj = obj

        self.data = data

        if label is not None:
            self.label = label
        else:
            self.label = data.n3()
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
