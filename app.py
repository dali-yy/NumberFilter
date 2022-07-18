# -*- coding: utf-8 -*-
# @Time : 2022/7/10 14:24
# @Author : XXX
# @Site : 
# @File : app.py
# @Software: PyCharm
import sys
import itertools
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from filter import match_line, text_to_nums, match_all, match_any, prize_analysize


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.filter_results = []  # 过滤结果
        self.total_count = 33  # 总的可选号码个数
        self.prize_count = 7  # 中奖号码个数

        self.selected_num_btns = []  # 选中的中奖号码

        self.clipboard = QtWidgets.QApplication.clipboard()  # 剪切板

        # 设置应用名称
        self.setWindowTitle("彩票号码过滤器")
        # 设置图标
        self.setWindowIcon(QtGui.QIcon('./favicon.ico'))
        # 设置窗口大小
        self.resize(1200, 800)
        # 设置窗口背景颜色
        palette = QtGui.QPalette()
        palette.setColor(self.backgroundRole(), QtGui.QColor(255, 255, 255))  # 设置背景颜色
        self.setPalette(palette)
        # 窗口居中显示
        self.center()
        # 初始化界面部件
        self.init_ui()

    def init_ui(self):
        """************** 界面总体布局 **************"""
        # 创建窗口主部件
        self.main_widget = QtWidgets.QWidget()

        # 过滤窗口
        self.filter_widget = QtWidgets.QWidget()
        # 分析窗口
        self.analysis_widget = QtWidgets.QWidget()
        # 微信号标签
        self.wechat_label = QtWidgets.QLabel('微信号：Ly661833')
        # 主界面布局
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.main_layout.addWidget(self.analysis_widget, 0, 0, 15, 0)
        self.main_layout.addWidget(self.filter_widget, 0, 0, 15, 0)
        self.main_layout.addWidget(self.wechat_label, 15, 0, 1, 0, alignment=QtCore.Qt.AlignCenter)
        # 设置窗口主部件
        self.setCentralWidget(self.main_widget)

        """************** 设置过滤部件 **************"""
        # 创建配置部件
        self.config_widget = QtWidgets.QWidget()
        self.config_widget.setObjectName("config_widget")

        # 创建内容部件
        self.content_widget = QtWidgets.QWidget()
        self.content_widget.setObjectName("content_widget")

        # 主界面布局
        self.filter_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.filter_widget.setLayout(self.filter_layout)  # 设置窗口主部件布局为网格布局
        self.filter_layout.addWidget(self.config_widget, 0, 0, 1, 1)
        self.filter_layout.addWidget(self.content_widget, 1, 0, 7, 1)

        """************** 设置相关配置部件 **************"""
        # 彩票类型控件
        self.lottery_type_frame = QtWidgets.QFrame()
        self.lottery_type_frame.setObjectName('config_frame')
        # 彩票类型标签
        self.lottery_type_label = QtWidgets.QLabel('彩票类型')
        self.lottery_type_label.setObjectName('config_title_label')
        # 总的号码个数
        self.total_spin = QtWidgets.QSpinBox()
        self.total_spin.setObjectName('config_spin')
        self.total_spin.setMaximum(33)
        self.total_spin.setMinimum(11)
        self.total_spin.setValue(self.total_count)
        self.total_spin.valueChanged.connect(self.on_total_spin_change)
        # 选标签
        self.select_label = QtWidgets.QLabel('选')
        self.select_label.setObjectName('config_label')
        # 中将号码个数
        self.prize_spin = QtWidgets.QSpinBox()
        self.prize_spin.setObjectName('config_spin')
        self.prize_spin.setMaximum(11)
        self.prize_spin.setMinimum(1)
        self.prize_spin.setValue(self.prize_count)
        self.prize_spin.valueChanged.connect(self.on_prize_spin_change)
        # 设置彩票类型布局
        self.lottery_type_layout = QtWidgets.QGridLayout()
        self.lottery_type_layout.addWidget(self.lottery_type_label, 0, 0, 1, 3)
        self.lottery_type_layout.addWidget(self.total_spin, 1, 0, 1, 1)
        self.lottery_type_layout.addWidget(self.select_label, 1, 1, 1, 1, alignment=QtCore.Qt.AlignCenter)
        self.lottery_type_layout.addWidget(self.prize_spin, 1, 2, 1, 1)
        self.lottery_type_frame.setLayout(self.lottery_type_layout)

        # 过滤条件控件
        self.filter_condition_frame = QtWidgets.QFrame()
        self.filter_condition_frame.setObjectName('config_frame')
        # 过滤条件标签
        self.filter_condition_label = QtWidgets.QLabel('过滤条件')
        self.filter_condition_label.setObjectName('config_title_label')
        # 过滤类型下拉框
        self.filter_type_combobox = QtWidgets.QComboBox()
        self.filter_type_combobox.setObjectName('filter_type_combobox')
        self.filter_type_combobox.addItems([
            'A 在 B 中每组重',
            'B 在 A 中每组重',
            'A 在 B 中任意一组重',
            'B 在 A 中任意一组重',
            'A 中每组重',
            'B 中每组重',
            'A 中任意两组重',
            'B 中任意两组重'
        ])
        # 重复的号码数（左边界）
        self.duplicate_left_spin = QtWidgets.QSpinBox()
        self.duplicate_left_spin.setObjectName('config_spin')
        self.duplicate_left_spin.setMinimum(0)
        self.duplicate_left_spin.setMaximum(7)
        # -标签
        self.between_label1 = QtWidgets.QLabel('-')
        self.between_label1.setObjectName('config_label')
        # 重复的号码数（右边界）
        self.duplicate_right_spin = QtWidgets.QSpinBox()
        self.duplicate_right_spin.setObjectName('config_spin')
        self.duplicate_right_spin.setMinimum(0)
        self.duplicate_right_spin.setMaximum(7)
        # 个号标签
        self.num_label = QtWidgets.QLabel('个号')
        self.num_label.setObjectName('config_label')
        # 结果保留勾选框
        self.result_retain_checkbox = QtWidgets.QCheckBox('最终结果保留')
        self.result_retain_checkbox.setObjectName('result_retain_checkbox')
        # 结果保留注数
        self.result_spin = QtWidgets.QSpinBox()
        self.result_spin.setObjectName('config_spin')
        self.result_spin.setMinimum(1)  # 结果至少保留1注
        # 注标签
        self.note_label = QtWidgets.QLabel('注')
        self.note_label.setObjectName('config_label')
        # 保留、排除单选框
        self.include_radio_btn = QtWidgets.QRadioButton('保留')
        self.include_radio_btn.setObjectName('config_radio_btn')
        self.include_radio_btn.setChecked(True)
        self.exclude_radio_btn = QtWidgets.QRadioButton('排除')
        self.exclude_radio_btn.setObjectName('config_radio_btn')
        # 容错标签
        self.fault_tolerant_label = QtWidgets.QLabel('容错')
        self.fault_tolerant_label.setObjectName('config_label')
        # 容错个数（左边界）
        self.fault_left_spin = QtWidgets.QSpinBox()
        self.fault_left_spin.setObjectName('config_spin')
        self.fault_left_spin.setMinimum(0)
        # -标签
        self.between_label2 = QtWidgets.QLabel('-')
        self.between_label2.setObjectName('config_label')
        # 容错个数（右边界）
        self.fault_right_spin = QtWidgets.QSpinBox()
        self.fault_right_spin.setObjectName('config_spin')
        self.fault_right_spin.setMinimum(0)

        # 过滤条件布局
        self.filter_condition_layout = QtWidgets.QGridLayout()
        self.filter_condition_layout.addWidget(self.filter_condition_label, 0, 0, 1, 1)
        self.filter_condition_layout.addWidget(self.filter_type_combobox, 1, 0, 1, 2)
        self.filter_condition_layout.addWidget(self.duplicate_left_spin, 1, 2, 1, 1)
        self.filter_condition_layout.addWidget(self.between_label1, 1, 3, 1, 1, alignment=QtCore.Qt.AlignCenter)
        self.filter_condition_layout.addWidget(self.duplicate_right_spin, 1, 4, 1, 1)
        self.filter_condition_layout.addWidget(self.num_label, 1, 5, 1, 1)
        self.filter_condition_layout.addWidget(self.include_radio_btn, 1, 6, 1, 1)
        self.filter_condition_layout.addWidget(self.exclude_radio_btn, 1, 7, 1, 1)
        self.filter_condition_layout.addWidget(self.result_retain_checkbox, 1, 8, 1, 1)
        self.filter_condition_layout.addWidget(self.result_spin, 1, 9, 1, 1)
        self.filter_condition_layout.addWidget(self.note_label, 1, 10, 1, 1)
        self.filter_condition_layout.addWidget(self.fault_tolerant_label, 1, 11, 1, 1)
        self.filter_condition_layout.addWidget(self.fault_left_spin, 1, 12, 1, 1)
        self.filter_condition_layout.addWidget(self.between_label2, 1, 13, 1, 1, alignment=QtCore.Qt.AlignCenter)
        self.filter_condition_layout.addWidget(self.fault_right_spin, 1, 14, 1, 1)
        self.filter_condition_frame.setLayout(self.filter_condition_layout)

        # 相关配置布局
        self.config_layout = QtWidgets.QHBoxLayout()
        self.config_layout.addWidget(self.lottery_type_frame, stretch=2)
        self.config_layout.addStretch(1)
        self.config_layout.addWidget(self.filter_condition_frame, stretch=6)
        self.config_widget.setLayout(self.config_layout)

        # 设置过滤条件部件样式
        self.config_widget.setStyleSheet("""
            QFrame#config_frame {
                padding: 10px;
                border: 1px solid #d3d7d4;
                border-radius: 10px;
            }
            QLabel#config_title_label {
                margin-bottom: 10px;
                font-size: 24px;
                font-weight: 400;
                font-family: '微软雅黑';
            }
            QLabel#config_label {
                font-size: 22px;
            }
            QComboBox#filter_type_combobox {
                font-size: 22px;
            }
            QSpinBox#config_spin {
                font-size: 22px;
            }
            QRadioButton#config_radio_btn {
                font-size: 22px;
            }
            QRadioButton#config_radio_btn {
                font-size: 22px;
            }
            QCheckBox#result_retain_checkbox {
                font-size: 22px;
            }
        """)

        """************** 设置内容部件 **************"""
        # A 框架
        self.frame_A = QtWidgets.QFrame()
        self.frame_A.setObjectName('content_frame')
        # A 标签
        self.label_A = QtWidgets.QLabel('A')
        self.label_A.setObjectName('content_label')
        # A 注数标签
        self.note_label_A = QtWidgets.QLabel('注数：')
        self.note_label_A.setObjectName('content_label')
        # A 输入框
        self.text_edit_A = QtWidgets.QTextEdit()
        self.text_edit_A.setObjectName('content_text_edit')
        # A 输入框清空按钮
        self.clear_btn_A = QtWidgets.QPushButton('清 空')
        self.clear_btn_A.setObjectName('clear_btn')
        self.clear_btn_A.setFixedSize(QtCore.QSize(130, 50))
        self.clear_btn_A.setCursor(QtCore.Qt.PointingHandCursor)
        self.clear_btn_A.clicked.connect(self.reset_A)
        # A 中粘贴内容按钮
        self.paste_btn_A = QtWidgets.QPushButton('粘  贴')
        self.paste_btn_A.setObjectName('paste_btn')
        self.paste_btn_A.setFixedSize(QtCore.QSize(130, 50))
        self.paste_btn_A.setCursor(QtCore.Qt.PointingHandCursor)
        self.paste_btn_A.clicked.connect(self.on_paste_a)

        # A 框架布局
        self.layout_A = QtWidgets.QGridLayout()
        self.layout_A.addWidget(self.label_A, 0, 0, 1, 6)
        self.layout_A.addWidget(self.note_label_A, 0, 6, 1, 6)
        self.layout_A.addWidget(self.text_edit_A, 1, 0, 8, 12)
        self.layout_A.addWidget(self.clear_btn_A, 9, 0, 3, 6, alignment=QtCore.Qt.AlignCenter)
        self.layout_A.addWidget(self.paste_btn_A, 9, 6, 3, 6, alignment=QtCore.Qt.AlignCenter)
        self.frame_A.setLayout(self.layout_A)

        # B 框架
        self.frame_B = QtWidgets.QFrame()
        self.frame_B.setObjectName('content_frame')
        # B 标签
        self.label_B = QtWidgets.QLabel('B')
        self.label_B.setObjectName('content_label')
        # B 标签
        self.note_label_B = QtWidgets.QLabel('注数：')
        self.note_label_B.setObjectName('content_label')
        # B 输入框
        self.text_edit_B = QtWidgets.QTextEdit()
        self.text_edit_B.setObjectName('content_text_edit')
        # B 输入框清空按钮
        self.clear_btn_B = QtWidgets.QPushButton('清  空')
        self.clear_btn_B.setObjectName('clear_btn')
        self.clear_btn_B.setFixedSize(QtCore.QSize(130, 50))
        self.clear_btn_B.setCursor(QtCore.Qt.PointingHandCursor)
        self.clear_btn_B.clicked.connect(self.reset_B)
        # B 中粘贴内容按钮
        self.paste_btn_B = QtWidgets.QPushButton('粘  贴')
        self.paste_btn_B.setObjectName('paste_btn')
        self.paste_btn_B.setFixedSize(QtCore.QSize(130, 50))
        self.paste_btn_B.setCursor(QtCore.Qt.PointingHandCursor)
        self.paste_btn_B.clicked.connect(self.on_paste_b)
        # B 框架布局
        self.layout_B = QtWidgets.QGridLayout()
        self.layout_B.addWidget(self.label_B, 0, 0, 1, 6)
        self.layout_B.addWidget(self.note_label_B, 0, 6, 1, 6)
        self.layout_B.addWidget(self.text_edit_B, 1, 0, 8, 12)
        self.layout_B.addWidget(self.clear_btn_B, 9, 0, 3, 6, alignment=QtCore.Qt.AlignCenter)
        self.layout_B.addWidget(self.paste_btn_B, 9, 6, 3, 6, alignment=QtCore.Qt.AlignCenter)
        self.frame_B.setLayout(self.layout_B)

        # C 框架
        self.frame_C = QtWidgets.QFrame()
        self.frame_C.setObjectName('content_frame')
        # C 标签
        self.label_C = QtWidgets.QLabel('C')
        self.label_C.setObjectName('content_label')
        # C 标签
        self.note_label_C = QtWidgets.QLabel('注数： ')
        self.note_label_C.setObjectName('content_label')
        # C 标签
        self.add_button_C = QtWidgets.QPushButton('+')
        self.add_button_C.setObjectName('content_label')
        self.add_button_C.setFixedSize(20, 20)
        self.add_button_C.clicked.connect(self.add_table_row)
        # C 结果列表
        self.result_table_C = QtWidgets.QTableWidget()
        self.result_table_C.setObjectName('result_table')
        self.result_table_C.setColumnCount(1)
        self.result_table_C.setHorizontalHeaderLabels(['彩票号码'])
        self.result_table_C.setColumnWidth(0, 600)
        # 进度条
        self.progress_bar_C = QtWidgets.QProgressBar()
        self.progress_bar_C.setMinimum(0)
        self.progress_bar_C.setMaximum(100)
        self.progress_bar_C.setValue(0)
        # C 输入框清空按钮
        self.clear_btn_C = QtWidgets.QPushButton('清  空')
        self.clear_btn_C.setObjectName('clear_btn')
        self.clear_btn_C.setFixedSize(QtCore.QSize(130, 50))
        self.clear_btn_C.setCursor(QtCore.Qt.PointingHandCursor)
        self.clear_btn_C.clicked.connect(self.reset_C)
        # C 框复制内容按钮
        self.copy_btn_C = QtWidgets.QPushButton('复  制')
        self.copy_btn_C.setObjectName('copy_btn')
        self.copy_btn_C.setFixedSize(QtCore.QSize(130, 50))
        self.copy_btn_C.setCursor(QtCore.Qt.PointingHandCursor)
        self.copy_btn_C.clicked.connect(self.on_copy_c)
        # C 框复制内容按钮
        self.paste_btn_C = QtWidgets.QPushButton('粘贴')
        self.paste_btn_C.setObjectName('paste_btn')
        self.paste_btn_C.setFixedSize(QtCore.QSize(130, 50))
        self.paste_btn_C.setCursor(QtCore.Qt.PointingHandCursor)
        self.paste_btn_C.clicked.connect(self.on_paste_c)
        # 过滤按钮
        self.filter_btn = QtWidgets.QPushButton('过  滤')
        self.filter_btn.setObjectName('filter_btn')
        self.filter_btn.setFixedSize(QtCore.QSize(130, 50))
        self.filter_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.filter_btn.clicked.connect(self.filter_num)
        # 中奖分析按钮
        self.prize_analysis_btn = QtWidgets.QPushButton('中奖分析')
        self.prize_analysis_btn.setObjectName('prize_analysis_btn')
        self.prize_analysis_btn.setFixedSize(QtCore.QSize(130, 50))
        self.prize_analysis_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.prize_analysis_btn.clicked.connect(self.to_prize_analysis)
        # C 框架布局
        self.layout_C = QtWidgets.QGridLayout()
        self.layout_C.addWidget(self.label_C, 0, 0, 1, 4)
        self.layout_C.addWidget(self.note_label_C, 0, 4, 1, 4)
        self.layout_C.addWidget(self.add_button_C, 0, 8, 1, 4, alignment=QtCore.Qt.AlignRight)
        self.layout_C.addWidget(self.result_table_C, 1, 0, 18, 12)
        self.layout_C.addWidget(self.progress_bar_C, 19, 0, 2, 12)
        self.layout_C.addWidget(self.clear_btn_C, 21, 0, 3, 2, alignment=QtCore.Qt.AlignCenter)
        self.layout_C.addWidget(self.copy_btn_C, 21, 2, 3, 2, alignment=QtCore.Qt.AlignCenter)
        self.layout_C.addWidget(self.paste_btn_C, 21, 4, 3, 2, alignment=QtCore.Qt.AlignCenter)
        self.layout_C.addWidget(self.filter_btn, 21, 6, 3, 2, alignment=QtCore.Qt.AlignCenter)
        self.layout_C.addWidget(self.prize_analysis_btn, 21, 8, 3, 4, alignment=QtCore.Qt.AlignRight)
        self.frame_C.setLayout(self.layout_C)

        # 设置内容部件部件
        self.content_layout = QtWidgets.QGridLayout()
        self.content_layout.addWidget(self.frame_A, 0, 0, 1, 1)
        self.content_layout.addWidget(self.frame_B, 1, 0, 1, 1)
        self.content_layout.addWidget(self.frame_C, 0, 1, 2, 1)
        self.content_widget.setLayout(self.content_layout)

        # 设置内容部件样式
        self.content_widget.setStyleSheet("""
            QWidget#content_widget{
                background:#fff;
                border: 2px solid #d3d7d4;
            }
            QLabel#content_label {
                font-size: 24px;
                font-weight: 400;
                font-family: '微软雅黑';
            }
            QTextEdit#content_text_edit {
                font-size: 24px;
            }
            QTableWidget#result_table {
                font-size: 22px;
                text-align: 'center';
            }
            QPushButton {
                border: 1px solid #d3d7d4;
                color: #1c1e21;
                font-size: 24px;
                font-family: '黑体';
                font-weight: 400;
                border-radius: 5px;
            }
            QPushButton:hover {
                border: 1px solid #69c0ff;
                color: #69c0ff;
            }
            QPushButton#filter_btn {
                background: #40a9ff;
                color: #fff;
            }
            QPushButton#filter_btn:hover {
                background: #69c0ff;
            }
            QPushButton#prize_analysis_btn {
                background: #1890ff;
                color: #fff;
            }
            QPushButton#prize_analysis_btn:hover {
                background: #69c0ff;
            }
        """)

        """************** 设置中奖分析部件 **************"""
        self.prize_number_frame = QtWidgets.QFrame()  # 中奖号码框架 
        self.prize_number_frame.setObjectName('prize_number_frame')
        self.prize_number_layout = QtWidgets.QGridLayout()

        # 设置中奖号码框架
        self.num_btns = [QtWidgets.QPushButton('0' + str(idx + 1) if idx < 9 else str(idx + 1)) for idx in range(33)]
        for idx, btn in enumerate(self.num_btns):
            btn.setObjectName('num_btn')
            btn.setCheckable(True)
            btn.setFixedSize(QtCore.QSize(40, 40))
            btn.setCursor(QtCore.Qt.PointingHandCursor)
            btn.clicked.connect(self.on_num_btn_click)
            self.prize_number_layout.addWidget(btn, idx // 11, idx % 11, 1, 1)

        self.prize_number_frame.setLayout(self.prize_number_layout)

        # 中奖分析结果展示
        self.analysis_result_tree = QtWidgets.QTreeWidget()
        self.analysis_result_tree.setObjectName('analysis_result_tree')
        self.analysis_result_tree.setHeaderLabels(['注数', '序号', '中奖号码'])
        self.analysis_result_tree.setColumnWidth(0, 350)
        self.analysis_result_tree.setColumnWidth(1, 100)

        # 重置按钮
        self.reset_btn = QtWidgets.QPushButton('重置')
        self.reset_btn.setObjectName('reset_btn')
        self.reset_btn.setFixedSize(QtCore.QSize(130, 50))
        self.reset_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.reset_btn.clicked.connect(self.reset_analysis)
        # 开始分析按钮
        self.analysis_btn = QtWidgets.QPushButton('开始分析')
        self.analysis_btn.setObjectName('analysis_btn')
        self.analysis_btn.setFixedSize(QtCore.QSize(130, 50))
        self.analysis_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.analysis_btn.clicked.connect(self.on_prize_analysize)
        # 返回按钮
        self.return_btn = QtWidgets.QPushButton('返回')
        self.return_btn.setObjectName('return_btn')
        self.return_btn.setFixedSize(QtCore.QSize(130, 50))
        self.return_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.return_btn.clicked.connect(lambda: self.change_widget(self.filter_widget))

        self.analysis_operate_layout = QtWidgets.QHBoxLayout()
        self.analysis_operate_layout.addWidget(self.reset_btn)
        self.analysis_operate_layout.addWidget(self.analysis_btn)
        self.analysis_operate_layout.addWidget(self.return_btn)

        self.analysis_layout = QtWidgets.QVBoxLayout()
        self.analysis_layout.addWidget(self.prize_number_frame, stretch=3)
        self.analysis_layout.addWidget(self.analysis_result_tree, stretch=4)
        self.analysis_layout.addLayout(self.analysis_operate_layout, stretch=1)
        self.analysis_widget.setLayout(self.analysis_layout)

        # 设置样式
        self.analysis_widget.setStyleSheet("""
            QFrame#prize_number_frame {
                border: 2px solid black;
                border-radius: 5px;
            }

            QTreeWidget#analysis_result_tree {
                font-size: 24px;
            }

            QPushButton {
                border: 1px solid #d3d7d4;
                color: #1c1e21;
                font-size: 24px;
                font-family: '黑体';
                font-weight: 400;
                border-radius: 5px;
            }
            QPushButton:hover {
                border: 1px solid #69c0ff;
                color: #69c0ff;
            }
            QPushButton#analysis_btn {
                background: #1890ff;
                color: #fff;
            }
            QPushButton#analysis_btn:hover {
                background: #69c0ff;
            }
            QPushButton#num_btn {
                border-radius: 20px;
            }
        """)

        self.analysis_widget.hide()

    def center(self):
        """
        窗口居中显示
        :return:
        """
        # 获取屏幕的坐标系
        screenGeo = QtWidgets.QDesktopWidget().geometry()
        # 获取窗口的坐标系
        windowGeo = self.geometry()
        # 左边距
        marginLeft = (screenGeo.width() - windowGeo.width()) / 2
        # 上边距
        marginTop = (screenGeo.height() - windowGeo.height()) / 2
        # 居中显示
        self.move(marginLeft, marginTop)

    def change_widget(self, widget):
        """
        切换部件
        """
        # 隐藏所有部件
        self.filter_widget.hide()
        self.analysis_widget.hide()

        # 显示指定部件
        widget.show()

    def on_total_spin_change(self):
        """
        中奖号码个数改变触发的函数
        :return:
        """
        total_count = self.total_spin.value()  # 中奖号码个数
        self.total_count = total_count

    def on_prize_spin_change(self):
        """
        中奖号码个数改变触发的函数
        :return:
        """
        prize_count = self.prize_spin.value()  # 中奖号码个数
        self.prize_count = prize_count
        self.duplicate_left_spin.setMaximum(prize_count)
        self.duplicate_right_spin.setMaximum(prize_count)

    def to_prize_analysis(self):
        """
        进入中奖分析
        """
        if self.result_table_C.rowCount() == 0:
            QMessageBox.warning(self, "提示", "未过滤或粘贴彩票号码，不能进行中奖分析！", QMessageBox.Yes, QMessageBox.Yes)
            return
        self.filter_results = []
        for row in range(self.result_table_C.rowCount()):
            item = self.result_table_C.item(row, 0)
            text = item.text().strip() if item is not None else ''
            match_result = match_line(text, self.prize_count)

            if match_result is None:
                QMessageBox.warning(self, "提示",
                                    "C表格第{}行彩票号码格式错误！每行需要包含{}个号码，号码之间用空格隔开，且不能存在数字之外的字符".format(row + 1,
                                                                                                self.prize_count),
                                    QMessageBox.Yes, QMessageBox.Yes)
                return
            self.filter_results.append(match_result.group().split(' '))
        self.change_widget(self.analysis_widget)

    def reset_A(self):
        """
        重置A
        :return:
        """
        self.text_edit_A.clear()
        self.note_label_A.setText('注数：')

    def reset_B(self):
        """
        重置A
        :return:
        """
        self.text_edit_B.clear()
        self.note_label_B.setText('注数：')

    def reset_C(self):
        """
        重置C
        :return:
        """
        # 清空C表格
        self.result_table_C.clearContents()
        self.result_table_C.setRowCount(0)
        self.progress_bar_C.setValue(0)  # 进度条清空
        self.filter_results = []  # 过滤结果置空
        self.note_label_C.setText('注数：')

    def on_paste_a(self):
        """
        向A框中粘贴内容
        """
        # 获取剪切板内容
        text = self.clipboard.mimeData().text().strip().strip('\n')
        if not text:
            QMessageBox.warning(self, "提示", "未复制内容！", QMessageBox.Yes, QMessageBox.Yes)
            return
        self.text_edit_A.setText(text)
        self.note_label_A.setText('注数：{}'.format(len(text.split('\n'))))
        QMessageBox.information(self, "提示", "A 框粘贴成功！", QMessageBox.Yes, QMessageBox.Yes)

    def on_paste_b(self):
        """
        向B框中粘贴内容
        """
        # 获取剪切板内容
        text = self.clipboard.mimeData().text().strip().strip('\n')
        if not text:
            QMessageBox.warning(self, "提示", "未复制内容！", QMessageBox.Yes, QMessageBox.Yes)
            return
        self.text_edit_B.setText(text)
        self.note_label_B.setText('注数：{}'.format(len(text.split('\n'))))
        QMessageBox.information(self, "提示", "B 框粘贴成功！", QMessageBox.Yes, QMessageBox.Yes)

    def add_table_row(self):
        """
        添加表格一行
        :return:
        """
        self.result_table_C.setRowCount(self.result_table_C.rowCount() + 1)

    def on_paste_c(self):
        """
        向B框中粘贴内容
        """
        # 获取剪切板内容
        text = self.clipboard.mimeData().text().strip().strip('\n')
        if not text:
            QMessageBox.warning(self, "提示", "未复制内容！", QMessageBox.Yes, QMessageBox.Yes)
            return
        conversion = text_to_nums(text, self.prize_count)
        if not conversion['flag']:
            QMessageBox.warning(self, "提示",
                                "复制内容第{}行彩票号码格式错误！每行需要包含{}个号码，号码之间用空格隔开，且不能存在数字之外的字符".format(conversion['data'],
                                                                                             self.prize_count),
                                QMessageBox.Yes, QMessageBox.Yes)
            return
        results = conversion['data']  # 获取复制的内容
        # 将结果显示在C中
        for idx, result in enumerate(results):
            nums_item = QtWidgets.QTableWidgetItem(' '.join(result))
            nums_item.setTextAlignment(QtCore.Qt.AlignCenter)
            # 设置表格行数
            self.result_table_C.setRowCount(self.result_table_C.rowCount() + 1)
            self.result_table_C.setItem(self.result_table_C.rowCount() - 1, 0, nums_item)
        # 修改注数
        self.note_label_C.setText('注数：{}'.format(self.result_table_C.rowCount()))
        QMessageBox.information(self, "提示", "C 框粘贴成功！", QMessageBox.Yes, QMessageBox.Yes)

    def on_copy_c(self):
        """
        复制C框中内容
        """
        text = ''
        # 获取中奖号码
        for row in range(self.result_table_C.rowCount()):
            item = self.result_table_C.item(row, 0)
            text += item.text().strip() + '\n' if item is not None else ''
        self.clipboard.setText(text)
        QMessageBox.information(self, "提示", "C 框号码复制成功！", QMessageBox.Yes, QMessageBox.Yes)

    def filter_num(self):
        """
        号码过滤
        :return:
        """
        # 进度条清空
        self.progress_bar_C.setValue(0)
        # 过滤类型
        filter_type = self.filter_type_combobox.currentIndex()

        duplicate_left = self.duplicate_left_spin.value()
        duplicate_right = self.duplicate_right_spin.value()
        # 重复个数左边界不能大于右边界
        if duplicate_left > duplicate_right:
            QMessageBox.warning(self, "提示", "重复个数范围错误！左边界不能大于右边界！", QMessageBox.Yes, QMessageBox.Yes)
            return

        fault_left = self.fault_left_spin.value()
        fault_right = self.fault_right_spin.value()
        # 容错个数左边界不能大于右边界
        if fault_left > fault_right:
            QMessageBox.warning(self, "提示", "容错个数范围错误！左边界不能大于右边界！", QMessageBox.Yes, QMessageBox.Yes)
            return

        # 获取彩票号码个数
        prize_count = self.prize_spin.value()

        lottery_nums_group_a = []
        lottery_nums_group_b = []
        # 获取 A 输入框中的内容
        text_a = self.text_edit_A.toPlainText().strip().strip('\n')  # A框文本
        if filter_type != 5 and filter_type != 7:
            if not text_a:
                QMessageBox.warning(self, "提示", "A 框未输入彩票号码！", QMessageBox.Yes, QMessageBox.Yes)
                return
            conversion_a = text_to_nums(text_a, prize_count)
            if not conversion_a['flag']:
                QMessageBox.warning(self, "提示",
                                    "A 框第{}行彩票号码格式错误！每行需要包含{}个号码，号码之间用空格隔开，且不能存在数字之外的字符".format(conversion_a['data'],
                                                                                                self.prize_count),
                                    QMessageBox.Yes, QMessageBox.Yes)
                return
            lottery_nums_group_a = conversion_a['data']

        # 获取 B 框文本
        text_b = self.text_edit_B.toPlainText().strip().strip('\n')  # B框文本
        if filter_type != 4 and filter_type != 6:
            if not text_b:
                QMessageBox.warning(self, "提示", "B 框未输入彩票号码！", QMessageBox.Yes, QMessageBox.Yes)
                return
            conversion_b = text_to_nums(text_b, prize_count)
            if not conversion_b['flag']:
                QMessageBox.warning(self, "提示",
                                    "B 框第{}行彩票号码格式错误！每行需要包含{}个号码，号码之间用空格隔开，且不能存在数字之外的字符".format(conversion_b['data'],
                                                                                                self.prize_count),
                                    QMessageBox.Yes, QMessageBox.Yes)
                return
            lottery_nums_group_b = conversion_b['data']

        # 根据下拉列表选择的方式进行过滤
        match_result = []
        mismatch_result = []
        self.filter_btn.setDisabled(True)
        if filter_type == 0 or filter_type == 1:
            if filter_type == 1:
                lottery_nums_group_a, lottery_nums_group_b = lottery_nums_group_b, lottery_nums_group_a
            for idx, nums_a in enumerate(lottery_nums_group_a):
                QtWidgets.QApplication.processEvents()  # 刷新屏幕
                self.progress_bar_C.setValue(int((idx + 1) / len(lottery_nums_group_a) * 100))
                # 如果该组号码与 B 中每组号码都重复 left-right 个号，则加入到结果列表中
                if match_all(nums_a, lottery_nums_group_b, duplicate_left, duplicate_right):
                    match_result.append(nums_a)
                else:
                    mismatch_result.append(nums_a)

        elif filter_type == 2 or filter_type == 3:
            if filter_type == 3:
                lottery_nums_group_a, lottery_nums_group_b = lottery_nums_group_b, lottery_nums_group_a
            for idx, nums_a in enumerate(lottery_nums_group_a):
                QtWidgets.QApplication.processEvents()  # 刷新屏幕
                self.progress_bar_C.setValue(int((idx + 1) / len(lottery_nums_group_a) * 100))
                # 如果该组号码与 B 中任意一组号码重复 left-right 个号，则加入到结果列表中
                if match_any(nums_a, lottery_nums_group_b, duplicate_left, duplicate_right):
                    match_result.append(nums_a)
                else:
                    mismatch_result.append(nums_a)

        elif filter_type == 4 or filter_type == 5:
            all_nums = [('0' if idx < 9 else '') + str(idx + 1) for idx in range(self.total_count)]
            # 所有组合
            all_combinations = list(itertools.combinations(all_nums, prize_count))
            lottery_nums_group = lottery_nums_group_a if filter_type == 4 else lottery_nums_group_b
            for idx, nums in enumerate(all_combinations):
                QtWidgets.QApplication.processEvents()  # 刷新屏幕
                self.progress_bar_C.setValue(int((idx + 1) / len(lottery_nums_group) * 100))
                # 如果该组号码与 B 中每组号码都重复 left-right 个号，则加入到结果列表中
                if match_all(nums, lottery_nums_group, duplicate_left, duplicate_right):
                    match_result.append(nums)
                else:
                    mismatch_result.append(nums)
        elif filter_type == 6 or filter_type == 7:
            lottery_nums_group = lottery_nums_group_a if filter_type == 6 else lottery_nums_group_b

            n = len(lottery_nums_group)
            for idx, nums in enumerate(lottery_nums_group):
                QtWidgets.QApplication.processEvents()  # 刷新屏幕
                self.progress_bar_C.setValue(int((idx + 1) / n * 100))  # 更新进度条
                other_nums_group = lottery_nums_group[idx + 1: n] + lottery_nums_group[0: idx]  # 除当前号码外的其他组号码
                if match_any(nums, other_nums_group, duplicate_left, duplicate_right):
                    match_result.append(nums)
                else:
                    mismatch_result.append(nums)
        self.filter_btn.setDisabled(False)
        # 判断保留还是去除
        if self.exclude_radio_btn.isChecked():
            match_result, mismatch_result = mismatch_result, match_result

        # 容错左边界不能大于错误个数
        if fault_left > len(mismatch_result):
            QMessageBox.warning(self, "提示", "容错范围错误！未匹配结果仅有{}个，小于左边界 {}".format(len(mismatch_result), fault_left),
                                QMessageBox.Yes, QMessageBox.Yes)
            return
        filter_results = []
        # 如果容错个数不为0
        if fault_right > 0:
            mismatch_result = mismatch_result[0: fault_right] if fault_right < len(mismatch_result) else mismatch_result
            filter_results = match_result + mismatch_result
        else:
            filter_results = match_result

        # 如果选择了保留的注数
        if self.result_retain_checkbox.isChecked():
            result_count = self.result_spin.value()
            filter_results = filter_results[0: result_count] if result_count < len(
                filter_results) else filter_results
        # 显示总共多少注
        self.note_label_C.setText('注数： {}'.format(len(filter_results)))
        # 清空C框中的内容
        self.result_table_C.clearContents()
        self.result_table_C.setRowCount(len(filter_results))
        if filter_results:
            # 将结果显示在C中
            for idx, result in enumerate(filter_results):
                nums_item = QtWidgets.QTableWidgetItem(' '.join(result))
                nums_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.result_table_C.setItem(idx, 0, nums_item)
            QMessageBox.information(self, "提示", "过滤成功！", QMessageBox.Yes, QMessageBox.Yes)
        else:
            QMessageBox.warning(self, "提示", "过滤结果为空！".format(len(mismatch_result), fault_left),
                                QMessageBox.Yes, QMessageBox.Yes)

    def on_num_btn_click(self, btn):
        """
        数字按钮点击
        """
        sender = self.sender()
        if sender.isChecked():
            sender.setStyleSheet("""
                QPushButton {
                    background: #1E90FF;
                    color: #fff;
                }
            """)
            self.selected_num_btns.append(sender)
        else:
            sender.setStyleSheet("""
            QPushButton {
                background: #fff;
                color: #1c1e21;
                }
            """)
            self.selected_num_btns.remove(sender)

    def reset_analysis(self):
        """
        重置分析
        """
        # 所有按钮取消选中
        for btn in self.selected_num_btns:
            btn.setStyleSheet("""
            QPushButton {
                color: #1c1e21;
                }
            """)
            btn.setChecked(False)
        self.selected_num_btns = []
        # 清空分析结果
        self.analysis_result_tree.clear()

    def on_prize_analysize(self):
        """
        中奖分析
        """
        if len(self.selected_num_btns) == 0:
            QMessageBox.warning(self, "提示", '未选择中奖号码！', QMessageBox.Yes, QMessageBox.Yes)
            return

        # 选择的号码个数不能与彩票类型不符
        if len(self.selected_num_btns) != self.prize_count:
            QMessageBox.warning(self, "提示", '中奖号码个数应为{}个！'.format(self.prize_count), QMessageBox.Yes, QMessageBox.Yes)
            return

        prize_nums = [btn.text() for btn in self.selected_num_btns]  # 中奖号码
        # 中奖分析
        analysis_result = prize_analysize(self.filter_results, prize_nums)
        # 清空分析结果
        self.analysis_result_tree.clear()
        # 显示新的分析结果
        items = list(analysis_result.items())
        items.reverse()
        for key, value in items:
            tmp_root = QtWidgets.QTreeWidgetItem(self.analysis_result_tree)
            tmp_root.setText(0, '中{}个号： {} 注'.format(key, len(value)))
            for lottery in value:
                tmp_child = QtWidgets.QTreeWidgetItem(tmp_root)
                tmp_child.setText(1, str(lottery['id']))
                tmp_child.setText(2, ' '.join([str(num) for num in lottery['nums']]))
            self.analysis_result_tree.addTopLevelItem(tmp_root)
        QMessageBox.warning(self, "提示", '分析成功！', QMessageBox.Yes, QMessageBox.Yes)


if __name__ == '__main__':
    # 创建应用程序对象
    app = QtWidgets.QApplication(sys.argv)
    # 新建窗口
    gui = MainUi()
    # 显示在屏幕上
    gui.show()
    # 系统exit()方法确保应用程序干净的退出
    sys.exit(app.exec_())
