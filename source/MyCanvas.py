from MyItem import *

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication
from PyQt5.QtGui import (
    QMouseEvent, 
    QWheelEvent
)
from PyQt5.QtCore import Qt

import math

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
        self.status = 'line_0'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon_0'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_ellipse(self, item_id):
        self.status = 'ellipse_0'
        self.temp_algorithm = "Naive"
        self.temp_id = item_id

    def start_draw_curve(self, algorithm, item_id):
        self.status = 'curve_0'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_translate(self):
        self.status = 'translate_0'

    def start_rotate(self):
        self.status = 'rotate'
        
    def start_scale(self):
        self.status = 'scale'

    def finish_draw(self):
        print("f", end='')
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
        if selected == '':
            return
        self.selected_id = selected
        self.item_dict[selected].selected = True
        self.item_dict[selected].update()
        self.status = ''
        self.updateScene([self.sceneRect()])

    def mousePressEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line_0' or self.status == 'line_1':
            pass
        elif self.status == 'line_1':
            pass
        elif self.status == 'polygon_0':
            pass
        elif self.status == 'polygon_1':
            self.temp_item.p_list.append([x, y])
        elif self.status == 'ellipse_0' or self.status == 'ellipse_1':
            pass
        elif self.status == 'curve_0':
            pass
        elif self.status == 'curve_1':
            self.temp_item.p_list.append([x, y])
        elif self.status == 'translate_0':
            if self.item_dict[self.selected_id].boundingRect().contains(x, y):
                self.status = 'translate_1'
                self.x0 = x
                self.y0 = y
            else:
                pass
        elif self.status == 'rotate' or self.status == 'scale':
            pass

        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line_0': 
            self.temp_item = MyItem(self.temp_id, "line", [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
            self.status = 'line_1'
        elif self.status == 'line_1':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'polygon_0':
            self.temp_item = MyItem(self.temp_id, "polygon", [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
            self.status = 'polygon_1'
        elif self.status == 'polygon_1':
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'ellipse_0':
            self.temp_item = MyItem(self.temp_id, "ellipse", [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
            self.status = 'ellipse_1'
        elif self.status == 'ellipse_1':
            self.temp_item.p_list[1] = [x, y]
        elif self.status == 'curve_0':
            self.temp_item = MyItem(self.temp_id, "curve", [[x, y], [x, y]], self.temp_algorithm)
            self.scene().addItem(self.temp_item)
            self.status = 'curve_1'
        elif self.status == 'curve_1':
            self.temp_item.p_list[-1] = [x, y]
        elif self.status == 'translate_0':
            pass
        elif self.status == 'translate_1':
            self.item_dict[self.selected_id].translate(x - self.x0, y - self.y0)
            self.x0 = x
            self.y0 = y
        elif self.status == 'rotate' or self.status == 'scale':
            pass

        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        # normally 4 steps:
        # add to dict
        # add to list
        # reset status
        # call finishdraw
        if self.status == 'line_1':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.status = 'line_0'
            self.finish_draw()
        elif self.status == 'polygon_1':
            num = len(self.temp_item.p_list)
            p_list = self.temp_item.p_list
            if (num > 2) and math.hypot(p_list[0][0] - p_list[num - 1][0], p_list[0][1] - p_list[num - 1][1]) < 10:
                self.temp_item.p_list[num - 1][:] = self.temp_item.p_list[0][:] # add line <p[0], p[n - 1]>
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.status = 'polygon_0'
                self.finish_draw()
            else:
                pass
        elif self.status == 'ellipse_1':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.status = 'ellipse_0'
            self.finish_draw()
        elif self.status == 'translate_1':
            self.status = 'translate_0'
        elif self.status == 'curve_1':
        #    self.item_dict[self.temp_id] = self.temp_item
        #    self.list_widget.addItem(self.temp_id)
        #    self.status = 'curve_0'
        #    self.finish_draw()
            pass

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
            self.item_dict[self.selected_id].rotate(x, y, d)
        elif self.status == 'scale':
            if d > 0 and ctrl == 0:
                self.item_dict[self.selected_id].scale(x, y, 1.1)
            elif d > 0:
                self.item_dict[self.selected_id].scale(x, y, 1.01)
            elif d < 0 and ctrl == 0:
                self.item_dict[self.selected_id].scale(x, y, 0.9)
            else:
                self.item_dict[self.selected_id].scale(x, y, 0.99)

        self.updateScene([self.sceneRect()])
        super().wheelEvent(event)

