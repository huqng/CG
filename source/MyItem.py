import cg_algorithms as alg
from PyQt5.QtWidgets import (
    QGraphicsItem,
    QStyleOptionGraphicsItem,
    QWidget
)
from typing import Optional
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QRectF

class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """

    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', parent: QGraphicsItem = None):
        """

        :param item_id: 图元ID
        :param item_type: 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        :param p_list: 图元参数
        :param algorithm: 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        :param parent:
        """
        super().__init__(parent)
        self.id = item_id           # 图元ID
        self.item_type = item_type  # 图元类型，'line'、'polygon'、'ellipse'、'curve'等
        self.p_list = p_list        # 图元参数
        self.algorithm = algorithm  # 绘制算法，'DDA'、'Bresenham'、'Bezier'、'B-spline'等
        self.selected = False

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(int(x - 1), int(y - 1), int(w + 2), int(h + 2))
        elif self.item_type == 'polygon':
            xmin = 0xFFFF
            ymin = 0xFFFF
            xmax = -0xFFFF
            ymax = -0xFFFF
            for p in self.p_list:
                if xmin > p[0]:
                    xmin = p[0]
                if ymin > p[1]:
                    ymin = p[1]
                if xmax < p[0]:
                    xmax = p[0]
                if ymax < p[1]:
                    ymax = p[1]
            w = xmax - xmin
            h = ymax - ymin
            return QRectF(xmin - 1, ymin - 1, w + 2, h + 2)
        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        elif self.item_type == 'curve':
            return QRectF(0, 0, 600, 500)
            pass

    def translate(self, dx, dy):
        alg.translate(self.p_list, dx, dy)

    def rotate(self, x, y, degree):
        alg.rotate(self.p_list, x, y, degree)

    def scale(self, x, y, s):
        alg.scale(self.p_list, x, y, s)

    def clip(self, xmin, ymin, xmax, ymax, algorithm):
        alg.clip(self.p_list, xmin, ymin, xmax, ymax, algorithm)