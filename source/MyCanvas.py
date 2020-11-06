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
        self.pencolor = QColor(0, 80, 80)
    
    def get_pencolor(self):
        return self.pencolor
        
    def set_pencolor(self, color: QColor):
        self.pencolor = color

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
        if self.status == 'line_1':
            self.status = 'line_0'
        elif self.status == 'polygon_1':
            self.status = 'polygon_0'
        elif self.status == 'ellipse_1':
            self.status = 'ellipse_0'
        elif self.status == 'curve_1':
            self.status = 'curve_0'
        self.item_dict[self.temp_id] = self.temp_item
        self.list_widget.addItem(self.temp_id)
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
        if(event.buttons() == Qt.LeftButton):
            if self.status == 'line_0' or self.status == 'line_1':
                pass
            elif self.status == 'line_1':
                pass
            elif self.status == 'polygon_0':
                pass
            elif self.status == 'polygon_1':
                self.temp_item.p_list.append([x, y])
                pass
            elif self.status == 'ellipse_0' or self.status == 'ellipse_1':
                pass
            elif self.status == 'curve_0':
                pass
            elif self.status == 'curve_1':
                self.temp_item.p_list.append([x, y])
                pass
            elif self.status == 'translate_0':
                if self.item_dict[self.selected_id].boundingRect().contains(x, y):
                    self.status = 'translate_1'
                    self.x0 = x
                    self.y0 = y

                else:
                    pass
            elif self.status == 'rotate' or self.status == 'scale':
                pass
        else: # Right
            if self.status == 'polygon_1':
                self.temp_item.p_list.append(self.temp_item.p_list[-1][:])
                self.temp_item.p_list[-1] = self.temp_item.p_list[0][:] # add line <p[0], p[n - 1]>
                self.finish_draw()
            elif self.status == 'curve_1':
                self.finish_draw()



        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if(event.buttons() == Qt.LeftButton):
            if self.status == 'line_0': 
                self.temp_item = MyItem(self.temp_id, "line", [[x, y], [x, y]], self.pencolor, self.temp_algorithm)
                self.scene().addItem(self.temp_item)
                self.status = 'line_1'
            elif self.status == 'line_1':
                self.temp_item.p_list[1] = [x, y]
            elif self.status == 'polygon_0':
                self.temp_item = MyItem(self.temp_id, "polygon", [[x, y], [x, y]], self.pencolor, self.temp_algorithm)
                self.scene().addItem(self.temp_item)
                self.status = 'polygon_1'
            elif self.status == 'polygon_1':
                self.temp_item.p_list[-1] = [x, y]
            elif self.status == 'ellipse_0':
                self.temp_item = MyItem(self.temp_id, "ellipse", [[x, y], [x, y]], self.pencolor, self.temp_algorithm)
                self.scene().addItem(self.temp_item)
                self.status = 'ellipse_1'
            elif self.status == 'ellipse_1':
                self.temp_item.p_list[1] = [x, y]
            elif self.status == 'curve_0':
                self.temp_item = MyItem(self.temp_id, "curve", [[x, y], [x, y]], self.pencolor, self.temp_algorithm)
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
        if self.status == 'line_1':
            self.finish_draw()
        elif self.status == 'polygon_1':
            p_list = self.temp_item.p_list
            num = len(p_list)
            if (num > 2) and math.hypot(p_list[0][0] - p_list[num - 1][0], p_list[0][1] - p_list[num - 1][1]) < 10:
                p_list[num - 1] = p_list[0][:] # add line <p[0], p[n - 1]>
                self.finish_draw()
        elif self.status == 'ellipse_1':
            self.finish_draw()
        elif self.status == 'translate_1':
            self.status = 'translate_0'
        elif self.status == 'curve_1':
            pass    
        super().mouseReleaseEvent(event)
    
    def mouseDoubleClickEvent(self, event: QMouseEvent) ->None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'polygon_1':
            pass
        elif self.status == 'curve_1':
            pass

        return super().mouseDoubleClickEvent(event)

    def wheelEvent(self, event: QWheelEvent) -> None:
        pos = self.mapToScene(event.position().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        
        ctrl_being_pressed = QApplication.keyboardModifiers() == Qt.ControlModifier
        d = event.angleDelta().y()                              # 滚轮转一格返回120

        if self.status == 'rotate':
            r = d / (12 * (1 + ctrl_being_pressed * 9))         # if ctrl r = +=10, else r = +=1
            self.item_dict[self.selected_id].rotate(x, y, r)
        elif self.status == 'scale':
            s = 1 + d / (1200 * (1 + ctrl_being_pressed * 9))   # if ctrl s = 1 += 0.1, else s = 1 +- 0.01
            self.item_dict[self.selected_id].scale(x, y, s)
        self.updateScene([self.sceneRect()])
        super().wheelEvent(event)

