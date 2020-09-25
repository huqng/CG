from PyQt5.QtWidgets import (
    QMainWindow,
    QListWidget,
    QHBoxLayout,
    qApp,
    QMessageBox
)
from MyCanvas import *


class MainWindow(QMainWindow):
    """
    主窗口类
    """

    def __init__(self):
        super().__init__()
        self.item_cnt = 0

        # 使用QListWidget来记录已有的图元，并用于选择图元。注：这是图元选择的简单实现方法，更好的实现是在画布中直接用鼠标选择图元
        self.list_widget = QListWidget(self)
        self.list_widget.setMinimumWidth(200)

        # 使用QGraphicsView作为画布
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 600, 600)
        self.canvas_widget = MyCanvas(self.scene, self)
        self.canvas_widget.setFixedSize(600, 600)
        self.canvas_widget.main_window = self
        self.canvas_widget.list_widget = self.list_widget

        # 设置菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')
        set_pen_act = file_menu.addAction('设置画笔')
        reset_canvas_act = file_menu.addAction('重置画布')
        exit_act = file_menu.addAction('退出')
        test_act = file_menu.addAction('test')
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
        reset_canvas_act.triggered.connect(self.reset_canvas_action)                    # File/Reset
        exit_act.triggered.connect(self.exit_action)                                    # File/Exit
        set_pen_act.triggered.connect(self.set_pen_action)                              # File/Set pen
        test_act.triggered.connect(self.test_action)                                    # File/test
        line_naive_act.triggered.connect(self.line_naive_action)                        # Draw/Line/Naive
        line_dda_act.triggered.connect(self.line_dda_action)                            # Draw/Line/DDA
        line_bresenham_act.triggered.connect(self.line_bresenham_action)                # Draw/Line/B
        polygon_naive_act.triggered.connect(self.polygon_naive_action)                  # Draw/Polygon/Naive
        polygon_dda_act.triggered.connect(self.polygon_dda_action)                      # Draw/Polygon/DDA
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)          # Draw/Polygon/B
        ellipse_act.triggered.connect(self.ellipse_action)                              # Draw/Ellipse
        curve_bezier_act.triggered.connect(self.curve_bezier_action)                    # Draw/Curve/Bezier
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)                # Draw/Curve/B-spline
        translate_act.triggered.connect(self.translate_action)                          # Edit/Translate
        rotate_act.triggered.connect(self.rotate_action)                                # Edit/Rotate
        scale_act.triggered.connect(self.scale_action)                                  # Edit/Scale
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)  # Edit/Clip/Cohen-Sutherland
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)          # Edit/Clip/Liang-Barsky

        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)
                                                                                # Selection change

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addStretch()
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(800, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id
        
    # SLOTs
    def reset_canvas_action(self):
        self.item_cnt = 0
        self.list_widget.clear()
        self.statusBar().showMessage("")
        self.canvas_widget.scene().clear()
        self.canvas_widget.temp_algorithm = ''
        self.canvas_widget.temp_id = ''
        self.canvas_widget.temp_item = None
        self.canvas_widget.status = ''
        self.canvas_widget.clear_selection()
        self.canvas_widget.item_dict.clear()

    def exit_action(self):
        qApp.quit()

    def set_pen_action(self):
        pass

    def test_action(self):
        nmb = QMessageBox()
        nmb.warning(self, "________Warning________", "TODO")
        pass

    def line_naive_action(self):            
        if self.item_cnt != 0:
            self.item_cnt -= 1  # 为了补偿draw finish中的增量
        id = self.get_id()
        self.canvas_widget.start_draw_line('Naive', id)
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_dda_action(self):
        if self.item_cnt != 0:
            self.item_cnt -= 1  # 为了补偿draw finish中的增量
        id = self.get_id()
        self.canvas_widget.start_draw_line('DDA', id)
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        if self.item_cnt != 0:
            self.item_cnt -= 1  # 为了补偿draw finish中的增量
        id = self.get_id()
        self.canvas_widget.start_draw_line('Bresenham', id)
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        pass

    def polygon_naive_action(self):           
        if self.item_cnt != 0:
            self.item_cnt -= 1  # 为了补偿draw finish中的增量
        id = self.get_id()
        self.canvas_widget.start_draw_polygon('Naive', id)
        self.statusBar().showMessage('Naive算法绘制Polygon')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def polygon_dda_action(self):
        if self.item_cnt != 0:
            self.item_cnt -= 1  # 为了补偿draw finish中的增量
        id = self.get_id()
        self.canvas_widget.start_draw_polygon('DDA', id)
        self.statusBar().showMessage('DDA算法绘制Polygon')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        pass

    def polygon_bresenham_action(self):
        if self.item_cnt != 0:
            self.item_cnt -= 1  # 为了补偿draw finish中的增量
        id = self.get_id()
        self.canvas_widget.start_draw_polygon('Bresenham', id)
        self.statusBar().showMessage('Bresenham算法绘制Polygon')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
        pass

    def ellipse_action(self):
        if self.item_cnt != 0:
            self.item_cnt -= 1  # 为了补偿draw finish中的增量
        id = self.get_id()
        self.canvas_widget.start_draw_ellipse(id)
        self.statusBar().showMessage('绘制Ellipse')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        pass

    def curve_b_spline_action(self):
        pass

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

    def clip_cohen_sutherland_action(self):
        pass

    def clip_liang_barsky_action(self):
        pass



