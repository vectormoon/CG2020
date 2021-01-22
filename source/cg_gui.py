#!/usr/bin/env python
# -*- coding:utf-8 -*-

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
    QStyleOptionGraphicsItem,
    QColorDialog,
    QDialog,
    QPushButton,
    QInputDialog,
    QLineEdit,
    QMessageBox,
    QLayout,
    QFormLayout)
from PyQt5.QtGui import QPainter, QMouseEvent, QColor
from PyQt5.QtCore import QRectF


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
        self.polygonCompleted = 0
        self.pointNum = 0
        self.select_xy = None
        self.pList = None

    def start_draw_line(self, algorithm, item_id):
        self.status = 'line'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    #TODO
    def start_draw_polygon(self, algorithm, item_id):
        self.status = 'polygon'
        self.temp_algorithm = algorithm
        self.temp_id = item_id

    def start_draw_ellipse(self, item_id):
        self.status = 'ellipse'
        #self.temp_algorithm = algorithm
        self.temp_id = item_id
    
    def start_draw_curve(self, algorithm, item_id, pointNum):
        self.status = 'curve'
        self.temp_algorithm = algorithm
        self.temp_id = item_id
        self.pointNum = pointNum

    def start_translate(self):
        if self.selected_id == '':
            return
        self.status = 'translate'
        self.temp_item = self.item_dict[self.selected_id]
        self.pList = self.temp_item.p_list

    def start_rotate(self):
        if self.selected_id == '':
            return
        self.status = 'rotate'
        self.temp_item = self.item_dict[self.selected_id]
        self.pList = self.temp_item.p_list
        x_coordinate, xCoordinatePressed = QInputDialog.getInt(self, '旋转', 'Please input x_coordinate:', QLineEdit.Normal)
        y_coordinate, yCoordinatePressed = QInputDialog.getInt(self, '旋转', 'Please input y_coordinate:', QLineEdit.Normal)
        angle, anglePressed = QInputDialog.getInt(self, '旋转', 'Please input angle:', QLineEdit.Normal)
        if anglePressed and xCoordinatePressed and yCoordinatePressed:            
            self.temp_item.p_list = alg.rotate(self.pList, x_coordinate, y_coordinate, angle)
        self.pList = self.temp_item.p_list
        self.updateScene([self.sceneRect()])

    def start_scale(self):
        if self.selected_id == '':
            return
        self.status = 'scale'
        self.temp_item = self.item_dict[self.selected_id]
        self.pList = self.temp_item.p_list
        x_coordinate, xCoordinatePressed = QInputDialog.getInt(self, '缩放', 'Please input x_coordinate:', QLineEdit.Normal)
        y_coordinate, yCoordinatePressed = QInputDialog.getInt(self, '缩放', 'Please input y_coordinate:', QLineEdit.Normal)
        multiple, multiplePressed = QInputDialog.getDouble(self, '缩放', 'Please input multiple:', QLineEdit.Normal)
        if multiplePressed and xCoordinatePressed and yCoordinatePressed:
            self.temp_item.p_list = alg.scale(self.pList, x_coordinate, y_coordinate, multiple)
        self.pList = self.temp_item.p_list
        self.updateScene([self.sceneRect()])

    def start_clip(self, algorithm):
        if self.selected_id == '':
            return
        self.status = 'clip'
        self.temp_algorithm = algorithm
        self.temp_item = self.item_dict[self.selected_id]
        self.pList = self.temp_item.p_list

    def finish_draw(self):
        self.temp_id = self.main_window.get_id()
        #finish graph, clear temp_item
        self.temp_item = None

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
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.main_window.setcolor)
            self.scene().addItem(self.temp_item)
        #TODO
        elif self.status == 'polygon':
            if (self.temp_item == None):
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.main_window.setcolor)
                self.scene().addItem(self.temp_item)
            else:
                x0, y0 = self.temp_item.p_list[0]
                if ((abs(x0 - x) + abs(y0 - y) < 10) and len(self.temp_item.p_list) > 2):
                    self.item_dict[self.temp_id] = self.temp_item
                    self.list_widget.addItem(self.temp_id)
                    self.finish_draw()
                    self.polygonCompleted = 1
                else:
                    self.temp_item.p_list.append([x, y])

        elif self.status == 'ellipse':
            self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.main_window.setcolor)
            self.scene().addItem(self.temp_item)
        
        elif self.status == 'curve':
            if (self.temp_item == None):
                self.temp_item = MyItem(self.temp_id, self.status, [[x, y], [x, y]], self.temp_algorithm, self.main_window.setcolor)
                self.scene().addItem(self.temp_item)
            else:
                self.temp_item.p_list.append([x, y])

        elif self.status == 'translate':
            self.select_xy = [x, y]

        elif self.status == 'rotate':
            #self.select_xy = [x, y]
            pass

        elif self.status == 'scale':
            #self.select_xy = [x, y]
            pass

        elif self.status == 'clip':
            self.select_xy = [x, y]

        self.updateScene([self.sceneRect()])
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = self.mapToScene(event.localPos().toPoint())
        x = int(pos.x())
        y = int(pos.y())
        if self.status == 'line':
            self.temp_item.p_list[1] = [x, y]
        #TODO
        elif self.status == 'polygon':
            self.temp_item.p_list[-1] = [x, y]

        elif self.status == 'ellipse':
            self.temp_item.p_list[1] = [x, y]

        elif self.status == 'curve':
            self.temp_item.p_list[-1] = [x, y]
            
        elif self.status == 'translate':
            self.temp_item.p_list = alg.translate(self.pList, x - self.select_xy[0], y - self.select_xy[1])

        elif self.status == 'rotate':
            pass

        elif self.status == 'scale':
            pass

        elif self.status == 'clip':
            self.temp_item.p_list = alg.clip(self.pList, self.select_xy[0], self.select_xy[1], x, y, self.temp_algorithm)

        self.updateScene([self.sceneRect()])
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.status == 'line':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()
        #TODO
        elif self.status == 'polygon':
            pos = self.mapToScene(event.localPos().toPoint())
            x = int(pos.x())
            y = int(pos.y())
            if (self.polygonCompleted == 1):
                self.polygonCompleted = 0
                self.temp_item = None
            else:
                self.temp_item.p_list[-1] = [x, y]
            self.updateScene([self.sceneRect()])

        elif self.status == 'ellipse':
            self.item_dict[self.temp_id] = self.temp_item
            self.list_widget.addItem(self.temp_id)
            self.finish_draw()

        elif self.status == 'curve':
            pos = self.mapToScene(event.localPos().toPoint())
            x = int(pos.x())
            y = int(pos.y())
            self.temp_item.p_list[-1] = [x, y]
            self.updateScene([self.sceneRect()])
            if (len(self.temp_item.p_list) == self.pointNum):
                self.item_dict[self.temp_id] = self.temp_item
                self.list_widget.addItem(self.temp_id)
                self.finish_draw()

        elif self.status == 'translate':
            self.pList = self.temp_item.p_list

        elif self.status == 'rotate':
            #self.pList = self.temp_item.p_list
            pass

        elif self.status == 'scale':
            #self.pList = self.temp_item.p_list
            pass

        elif self.status == 'clip':
            self.pList = self.temp_item.p_list

        super().mouseReleaseEvent(event)

    def clearItem(self):
        for item in self.item_dict:
            self.scene().removeItem(self.item_dict[item])
        self.item_dict = {}
        self.selected_id = ''
        self.status = ''
        self.temp_algorithm = ''
        self.temp_id = ''
        self.temp_item = None

    '''def getXCoordinate(self):
        x_coordinate, xCoordinatePressed = QInputDialog.getInt(self, '旋转', 'Please input x_coordinate:')
        if xCoordinatePressed:
            self.le1.setText(str(x_coordinate))

    def getYCoordinate(self):
        y_coordinate, yCoordinatePressed = QInputDialog.getInt(self, '旋转', 'Please input y_coordinate:')
        if yCoordinatePressed:
            self.le2.setText(str(y_coordinate))'''



class MyItem(QGraphicsItem):
    """
    自定义图元类，继承自QGraphicsItem
    """
    def __init__(self, item_id: str, item_type: str, p_list: list, algorithm: str = '', setcolor: QColor = QColor(0, 0, 0),parent: QGraphicsItem = None):
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

        self.setcolor = setcolor

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        if self.item_type == 'line':
            item_pixels = alg.draw_line(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.setcolor)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())
        #TODO

        elif self.item_type == 'polygon':
            item_pixels = alg.draw_polygon(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.setcolor)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())

        elif self.item_type == 'ellipse':
            item_pixels = alg.draw_ellipse(self.p_list)
            for p in item_pixels:
                painter.setPen(self.setcolor)
                painter.drawPoint(*p)
            if self.selected:
                painter.setPen(QColor(255, 0, 0))
                painter.drawRect(self.boundingRect())

        elif self.item_type == 'curve':
            item_pixels = alg.draw_curve(self.p_list, self.algorithm)
            for p in item_pixels:
                painter.setPen(self.setcolor)
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
            return QRectF(x - 1, y - 1, w + 2, h + 2)
        
        #TODO
        elif self.item_type == 'polygon':
            x, y = self.p_list[0]
            x0, y0 = x, y
            x1, y1 = x, y
            for i in range(1, len(self.p_list)):
                x, y = self.p_list[i]
                x0 = min(x0, x)
                y0 = min(y0, y)
                x1 = max(x1, x)
                y1 = max(y1, y)
            w = x1 - x0
            h = y1 - y0
            return QRectF(x0 - 1, y0 - 1, w + 2, h + 2)

        elif self.item_type == 'ellipse':
            x0, y0 = self.p_list[0]
            x1, y1 = self.p_list[1]
            x = min(x0, x1)
            y = min(y0, y1)
            w = max(x0, x1) - x
            h = max(y0, y1) - y
            return QRectF(x - 1, y - 1, w + 2, h + 2)

        elif self.item_type == 'curve':
            x, y = self.p_list[0]
            x0, y0 = x, y
            x1, y1 = x, y
            for i in range(1, len(self.p_list)):
                x, y = self.p_list[i]
                x0 = min(x0, x)
                y0 = min(y0, y)
                x1 = max(x1, x)
                y1 = max(y1, y)
            w = x1 - x0
            h = y1 - y0
            return QRectF(x0 - 1, y0 - 1, w + 2, h + 2)


class MainWindow(QMainWindow):
    """
    主窗口类
    """
    def __init__(self):
        super().__init__()
        self.item_cnt = 0
        #TODO
        self.setcolor = QColor(0, 0, 0)

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
        draw_menu = menubar.addMenu('绘制')
        line_menu = draw_menu.addMenu('线段')
        line_naive_act = line_menu.addAction('Naive')
        line_dda_act = line_menu.addAction('DDA')
        line_bresenham_act = line_menu.addAction('Bresenham')
        polygon_menu = draw_menu.addMenu('多边形')
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
        exit_act.triggered.connect(qApp.quit)
        line_naive_act.triggered.connect(self.line_naive_action)
        #TODO
        line_dda_act.triggered.connect(self.line_dda_action)
        line_bresenham_act.triggered.connect(self.line_bresenham_action)
        polygon_dda_act.triggered.connect(self.polygon_dda_action)
        polygon_bresenham_act.triggered.connect(self.polygon_bresenham_action)
        set_pen_act.triggered.connect(self.set_pen_action)
        reset_canvas_act.triggered.connect(self.reset_canvas_action)
        ellipse_act.triggered.connect(self.ellipse_action)
        curve_bezier_act.triggered.connect(self.curve_bezier_action)
        curve_b_spline_act.triggered.connect(self.curve_b_spline_action)
        translate_act.triggered.connect(self.translate_action)
        rotate_act.triggered.connect(self.rotate_action)
        scale_act.triggered.connect(self.scale_action)
        clip_cohen_sutherland_act.triggered.connect(self.clip_cohen_sutherland_action)
        clip_liang_barsky_act.triggered.connect(self.clip_liang_barsky_action)
        self.list_widget.currentTextChanged.connect(self.canvas_widget.selection_changed)

        # 设置主窗口的布局
        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.canvas_widget)
        self.hbox_layout.addWidget(self.list_widget, stretch=1)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.hbox_layout)
        self.setCentralWidget(self.central_widget)
        self.statusBar().showMessage('空闲')
        self.resize(600, 600)
        self.setWindowTitle('CG Demo')

    def get_id(self):
        _id = str(self.item_cnt)
        self.item_cnt += 1
        return _id

    def line_naive_action(self):
        self.canvas_widget.start_draw_line('Naive', self.get_id())
        self.statusBar().showMessage('Naive算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    #TODO
    def line_dda_action(self):
        self.canvas_widget.start_draw_line('DDA', self.get_id())
        self.statusBar().showMessage('DDA算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def line_bresenham_action(self):
        self.canvas_widget.start_draw_line('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制线段')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def polygon_dda_action(self):
        self.canvas_widget.start_draw_polygon('DDA', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制polygon')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()
    
    def polygon_bresenham_action(self):
        self.canvas_widget.start_draw_polygon('Bresenham', self.get_id())
        self.statusBar().showMessage('Bresenham算法绘制polygon')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def set_pen_action(self):
        color = QColorDialog.getColor()
        self.setcolor = color
        self.statusBar().showMessage('设置画笔')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def reset_canvas_action(self):
        self.item_cnt = 0
        dialog = QDialog()
        dialog.setWindowTitle('重置画布')
        dialog.resize(400,247)
        height, width = 0, 0
        errorFlag = 0
        while 1:
            if ((height < 100 or width < 100 or height > 1000 or width > 1000) and (errorFlag == 0)):
                height, heightPressed = QInputDialog.getInt(self, '重置画布', 'Please input height(range:100-1000):', QLineEdit.Normal)
                width, widthPressed = QInputDialog.getInt(self, '重置画布', 'Please input width(range:100-1000):', QLineEdit.Normal)
                errorFlag = 1
            elif ((height < 100 or width < 100 or height > 1000 or width > 1000) and (errorFlag == 1)):
                QMessageBox.critical(self, 'Error', 'out of range')
                errorFlag = 0
            else:
                break

        if heightPressed and height and widthPressed and width:
            #clear item
            self.canvas_widget.clearItem()
            self.list_widget.clearSelection()
            self.canvas_widget.clear_selection()
            #resetsize
            self.scene = QGraphicsScene(self)
            self.scene.setSceneRect(0, 0, width, height)
            self.canvas_widget.resize(width, height)
            self.canvas_widget.setFixedSize(width, height)
            self.statusBar().showMessage('空闲')
            self.setMaximumSize(width, height)
            self.resize(width, height)

    def ellipse_action(self):
        self.canvas_widget.start_draw_ellipse(self.get_id())
        self.statusBar().showMessage('椭圆')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_bezier_action(self):
        self.canvas_widget.start_draw_curve('Bezier', self.get_id(), 3)#numofpoint
        self.statusBar().showMessage('Bezier算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def curve_b_spline_action(self):
        self.canvas_widget.start_draw_curve('B-spline', self.get_id(), 4)#numofpoint
        self.statusBar().showMessage('B-spline算法绘制曲线')
        self.list_widget.clearSelection()
        self.canvas_widget.clear_selection()

    def translate_action(self):
        self.canvas_widget.start_translate()
        self.statusBar().showMessage('平移')
        #self.list_widget.clearSelection()
        #self.canvas_widget.clear_selection()

    def rotate_action(self):
        self.canvas_widget.start_rotate()
        self.statusBar().showMessage('旋转')
        #self.list_widget.clearSelection()
        #self.canvas_widget.clear_selection()
    
    def scale_action(self):
        self.canvas_widget.start_scale()
        self.statusBar().showMessage('缩放')
        #self.list_widget.clearSelection()
        #self.canvas_widget.clear_selection()

    def clip_cohen_sutherland_action(self):
        self.canvas_widget.start_clip('Cohen-Sutherland')
        self.statusBar().showMessage('Cohen-Sutherland算法裁剪')
        #self.list_widget.clearSelection()
        #self.canvas_widget.clear_selection()

    def clip_liang_barsky_action(self):
        self.canvas_widget.start_clip('Liang-Barsky')
        self.statusBar().showMessage('Liang-Barsky算法裁剪')
        #self.list_widget.clearSelection()
        #self.canvas_widget.clear_selection()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
