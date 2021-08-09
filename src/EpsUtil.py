# -*- coding: utf-8 -*-
from PIL import ImageFont
import itertools
import logging

logger = logging.getLogger(__name__)

FONT_PATH = "/mnt/c/Windows/Fonts/times.ttf"
FONT_SIZE = 21
FONT = ImageFont.truetype(FONT_PATH, FONT_SIZE)

INF = float('inf')

def flatten(list_of_lists):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(list_of_lists)


def draw_rectangle(start_x, start_y, width, height, stroke_option=None):
    """
    引数をもとに、eps形式で矩形を示す文字列を返す。
    """
    ret = []
    ret.append(f"newpath")
    ret.append(f"{start_x} {start_y} moveto")
    ret.append(f"{start_x+width} {start_y} lineto")
    ret.append(f"{start_x+width} {start_y+height} lineto")
    ret.append(f"{start_x} {start_y+height} lineto")
    ret.append(f"{start_x} {start_y} lineto")
    ret.append(f"{start_x+width} {start_y} lineto")
    if stroke_option is not None:
        ret.append(stroke_option)
    ret.append(f"stroke")
    return "\n".join(ret)

def draw_lines(points: list[tuple], stroke_option=None):
    """
    引数をもとに、eps形式で折れ線を描く
    """
    ret = []
    ret.append(f"newpath")
    for i, (px, py) in enumerate(points):
        if i == 0:
            ret.append(f"{px} {py} moveto")
            continue
        else:
            ret.append(f"{px} {py} lineto")
    if stroke_option is not None:
        ret.append(stroke_option)
    ret.append(f"stroke")
    return "\n".join(ret)


def draw_text(start_x, start_y, text):
    """
    eps形式で文字列を描く。
    """
    fontsize = 21
    offset = 21//3
    ret = f"""/Times-Roman findfont {fontsize} scalefont setfont
{start_x} {start_y-offset} moveto
({text}) show
"""
    return ret

def text_length_in_picture(text):
    """
    描画したときの文字列の横幅を長さ(px)を取得する。
    """
    return FONT.getlength(text)


def export_eps(objects, links):
    """
    """
    logger.debug(objects)

    # BoundingBox
    bb_xmin, bb_xmax = INF, -INF
    bb_ymin, bb_ymax = INF, -INF

    margin = 50
    for obj in objects:
        if obj is None:
            continue
        bb_xmin = min(bb_xmin, obj.x-margin)
        bb_xmax = max(bb_xmax, obj.x + text_length_in_picture(obj.label)+margin)
        bb_ymin = min(bb_ymin, obj.y-margin)
        bb_ymax = max(bb_ymax, obj.y+margin)

    logger.info(f"{bb_xmin} {bb_ymin} {bb_xmax} {bb_ymax}")

    ret = [f"""\
%!PS-Adobe-3.0 EPSF-3.0
%%BoundingBox: {bb_xmin} {bb_ymin} {bb_xmax-bb_xmin} {bb_ymax-bb_ymin}
"""
    ]

    for link in links:
        ret.append(link.export())

    for obj in objects:
        if obj is None:
            continue
        ret.append(obj.export())

    ret.append("\n%%EOF")

    return "\n".join(ret)
