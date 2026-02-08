"""
Phira资源包生成器
基于Python和PyQt6的图形界面应用程序
"""
import sys
import os
# 添加项目根目录到Python路径，以便正确导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()