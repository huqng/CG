#!/usr/bin/python3
# -*- coding:utf-8 -*-

import math
import sys
import cg_algorithms as alg
from typing import Optional
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsItem,
    QListWidget,
    QHBoxLayout,
    QWidget,
    QStyleOptionGraphicsItem)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor
from PyQt5.QtGui import QWheelEvent, QKeyEvent
from PyQt5.QtCore import QRectF, Qt


class MyCanvas(QGraphicsView):
    """
    画布窗体类，继承自QGraphicsView，采用QGraphicsView、QGraphicsScene、QGraphicsItem的绘图框架
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.main_window = None
        self.list_widget = None
        self.item_dict = {}
        self.selected_id = ''

        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

        self.polygon_p_list = []

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon_0'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_ellipse(self, item_id):
        self.temp_algorithm = "Naive"
        self.status = 'ellipse'
        self.temp_id = item_id

    def start_translate(self):
        self.status = 'translate'

    def start_rotate(self):
        self.status = 'rotate'
        
    def start_scale(self):
        self.status = 'scale'

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()
        self.updateScene([self.sceneRect()])

    def clear_selection(self):
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.selected_id = ''

    def selection_changed(self, selected):
        self.main_window.statusBar().showMessage('图元选择： %s' % selected)
        if self.selected_id != '':
            self.item_dict[self.selected_id].selected = False
            self.item_dict[self.selected_id].update()
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'polygon_0':
            self.temp_item = MyItem(self.temp_id, "polygon", [[x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
            self.status = 'polygon_1'
        elif self.status == 'polygon_1':
            self.temp_item.p_list.append([x, y])
            pass
        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, "ellipse", [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
        elif self.status == 'translate':
            self.temp_item = self.item_dict[self.selected_id]
            if self.temp_item.boundingRect().contains(x, y):
                self.status = 'translate_1'
                self.x0 = x
                self.y0 = y
            else:
                pass

        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon_1':
            num = len(self.temp_item.p_list)
            self.temp_item.p_list[num - 1] = [x, y]
        elif self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'translate_1':
            alg.translate(self.temp_item.p_list, x - self.x0, y - self.y0)
        #    for p in self.temp_item.p_list:
        #        p[0] += (x - self.x0)
        #        p[1] += (y - self.y0)
            self.x0 = x
            self.y0 = y

        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'polygon_1':
            num = len(self.temp_item.p_list)
            if (num > 2) and math.hypot(self.temp_item.p_list[0][0] - self.temp_item.p_list[num - 1][0], self.temp_item.p_list[0][1] - self.temp_item.p_list[num - 1][1]) < 10:
                self.temp_item.p_list[num - 1][:] = self.temp_item.p_list[0][:]
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.status = 'polygon_0'
                self.finish_draw()
            else:
                pass
        elif self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        elif self.status == 'translate_1':
            self.status = 'translate'

        self.updateScene([self.sceneRect()])
        super().mouseReleaseEvent(event)
    
    def wheelEvent(self, event: QWheelEvent) -> None:
        pos = self.mapToScene(event.position().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            ctrl = 1
        else:
            ctrl = 0
        d = event.angleDelta().y() / 12 / (1 + 9 * ctrl)

        if self.status == 'rotate':
            alg.rotate(self.item_dict[self.selected_id].p_list, x, y, d)
        elif self.status == 'scale':
            if d > 0 and ctrl == 0:
                alg.scale(self.item_dict[self.selected_id].p_list, x, y, 1.1)
            elif d > 0:
                alg.scale(self.item_dict[self.selected_id].p_list, x, y, 1.01)
            elif d < 0 and ctrl == 0:
                alg.scale(self.item_dict[self.selected_id].p_list, x, y, 0.9)
            else:
                alg.scale(self.item_dict[self.selected_id].p_list, x, y, 0.99)



        self.updateScene([self.sceneRect()])
        super().wheelEvent(event)


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
            pass
        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
            pass
        elif self.item_type == 'curve':
            pass

    def boundingRect(self) -> QRectF:
        if self.item_type == 'line':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)
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
            pass


class MainWindow(QMainWindow):
    """
    主窗口类
    """

    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMaximumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
    #    self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        exit_act = file_menu.addAction('退出')
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
        polygon_naive_act = polygon_menu.addAction('Naive')
        polygon_dda_act = polygon_menu.addAction('DDA')
        polygon_bresenham_act = polygon_menu.addAction('Bresenham')
        ellipse_act = draw_menu.addAction('椭圆')
        curve_menu = draw_menu.addMenu('曲线')
        curve_bezier_act = curve_menu.addAction('Bezier')
        curve_b_spline_act = curve_menu.addAction('B-spline')
        edit_menu = menubar.addMenu('编辑')
        translate_act = edit_menu.addAction('平移')
        rotate_act = edit_menu.addAction('旋转')
        scale_act = edit_menu.addAction('缩放')
        clip_menu = edit_menu.addMenu('裁剪')
        clip_cohen_sutherland_act = clip_menu.addAction('Cohen-Sutherland')
        clip_liang_barsky_act = clip_menu.addAction('Liang-Barsky')

        # 连接信号和槽函数
        exit_act.triggered.connect(qApp.quit)                                   # EXIT - QUIT
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        line_naive_act.triggered.connect(self.line_naive_action)                # Line - Naive
        polygon_naive_act.triggered.connect(self.polygon_naive_action)          # Polygon - Naive
        ellipse_act.triggered.connect(self.ellipse_action)                      # Ellipse
        translate_act.triggered.connect(self.translate_action)                  # Translate
        rotate_act.triggered.connect(self.rotate_action)                        # Rotate
        scale_act.triggered.connect(self.scale_action)                          # Scale
        curve_bezier_act.triggered.connect(self.curve_bezier_action)               # Bezier - Curve
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)           # B-spline - Curve

        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)
                                                                                # Selection changed

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(1280, 720)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id
        
    # SLOTS

    def line_naive_action(self):            
        if self.item_cnt != 0:
            self.item_cnt -= 1  # 为了补偿draw finish中的增量
        id = self.get_id()
        self.canvas_widget.start_draw_line('Naive', id)
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_naive_action(self):           
        if self.item_cnt != 0:
            self.item_cnt -= 1  # 为了补偿draw finish中的增量
        id = self.get_id()
        self.canvas_widget.start_draw_polygon('Naive', id)
        self.statusBar().showMessage('Naive算法绘制Polygon')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def ellipse_action(self):
        if self.item_cnt != 0:
            self.item_cnt -= 1  # 为了补偿draw finish中的增量
        id = self.get_id()
        self.canvas_widget.start_draw_ellipse(id)
        self.statusBar().showMessage('绘制Ellipse')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        if self.canvas_widget.selected_id == '':
            self.statusBar().showMessage("选择需要变换的Item！")
        else:
            self.statusBar().showMessage("使用鼠标拖动")
            self.canvas_widget.start_translate()
            
    def rotate_action(self):
        if self.canvas_widget.selected_id == '':
            self.statusBar().showMessage("选择需要旋转的Item！")
        else:
            self.statusBar().showMessage("使用鼠标滚轮和Ctrl")
            self.canvas_widget.start_rotate()
            
    def scale_action(self):
        if self.canvas_widget.selected_id == '':
            self.statusBar().showMessage("选择需要scale的Item！")
        else:
            self.statusBar().showMessage("使用鼠标滚轮和Ctrl")
            self.canvas_widget.start_scale()

    def curve_bezier_action(self):
        pass

    def curve_b_spline_action(self):
        pass

    def reset_canvas_action(self):
        self.item_cnt = 0
        self.list_widget.clear()
        self.statusBar().showMessage("")
        self.canvas_widget.scene().clear()
        self.canvas_widget.item_dict.clear()
        self.canvas_widget.temp_algorithm = ''
        self.canvas_widget.temp_id = ''
        self.canvas_widget.temp_item = None
        self.canvas_widget.status = ''
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
