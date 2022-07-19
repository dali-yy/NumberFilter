from PyQt5 import QtCore, QtGui, QtWidgets

class CountWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # 设置应用名称
        self.setWindowTitle("过滤结果号码出现次数统计")
        # 设置窗口大小
        self.resize(600, 400)
        # 显示统计次数的表格
        self.count_table = QtWidgets.QTableWidget()
        self.count_table.setObjectName('count_table')
        self.count_table.setColumnCount(2)
        self.count_table.setColumnWidth(0, 200)
        self.count_table.setColumnWidth(1, 350)
        self.count_table.setHorizontalHeaderLabels(['号码', '出现次数'])
        # 布局

