"""
Phira资源包生成器配置常量
"""

# 应用程序配置
APP_NAME = "Phira资源包生成器"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

# 默认特效参数
DEFAULT_FX_COLS = 8
DEFAULT_FX_ROWS = 8
DEFAULT_FX_TOTAL_WIDTH = 512
DEFAULT_FX_TOTAL_HEIGHT = 512
DEFAULT_FX_FRAME_WIDTH = 64
DEFAULT_FX_FRAME_HEIGHT = 64
DEFAULT_FX_DURATION = 0.55
DEFAULT_FX_SCALE = 1.0
DEFAULT_FX_ROTATE = True

# 默认Hold Atlas参数
DEFAULT_HOLD_ATLAS = [50, 50]
DEFAULT_HOLD_ATLAS_MH = [50, 95]

# 文件过滤器
AUDIO_FILTER = "音频文件 (*.wav *.mp3 *.ogg *.flac)"
IMAGE_FILTER = "图像文件 (*.png *.jpg *.jpeg *.gif *.bmp)"

# 文件映射
IMAGE_MAPPINGS = {
    'tap_image': 'click.png',
    'tap_mh_image': 'click_mh.png',
    'drag_image': 'drag.png',
    'drag_mh_image': 'drag_mh.png',
    'flick_image': 'flick.png',
    'flick_mh_image': 'flick_mh.png',
    'hold_image': 'hold.png',
    'hold_mh_image': 'hold_mh.png'
}

AUDIO_MAPPINGS = {
    'tap_sound': 'tap',
    'drag_sound': 'drag',
    'flick_sound': 'flick',
    'end_music': 'endMusic'
}

# 主题样式
DARK_THEME_STYLESHEET = """
    QMainWindow {
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                         stop: 0 #2c3e50, stop: 1 #1a1a2e);
    }
    QLabel {
        color: #ecf0f1;
        font-size: 13px;
        background: transparent;
    }
    QPushButton {
        background-color: #3498db;
        border: none;
        color: white;
        padding: 10px 15px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: bold;
        min-height: 30px;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
    QPushButton:pressed {
        background-color: #21618c;
    }
    QPushButton#browse_button {
        background-color: #9b59b6;
    }
    QPushButton#browse_button:hover {
        background-color: #8e44ad;
    }
    QPushButton#browse_button:pressed {
        background-color: #7d3c98;
    }
    QLineEdit {
        border: 2px solid #34495e;
        border-radius: 6px;
        padding: 8px;
        font-size: 13px;
        background-color: #34495e;
        color: #ecf0f1;
        selection-background-color: #3498db;
    }
    QLineEdit:focus {
        border: 2px solid #3498db;
    }
    QTextEdit {
        border: 2px solid #34495e;
        border-radius: 6px;
        font-size: 13px;
        background-color: #34495e;
        color: #ecf0f1;
        selection-background-color: #3498db;
    }
    QTextEdit:focus {
        border: 2px solid #3498db;
    }
    QGroupBox {
        font-weight: bold;
        font-size: 14px;
        border: 2px solid #3498db;
        border-radius: 8px;
        margin-top: 1ex;
        padding-top: 15px;
        background-color: rgba(52, 73, 94, 0.7);
        color: #ecf0f1;
    }
    QGroupBox:title {
        subcontrol-origin: margin;
        left: 20px;
        padding: 0 10px 0 10px;
        background-color: rgba(44, 62, 80, 0.7);
    }
    QSpinBox, QDoubleSpinBox {
        border: 2px solid #34495e;
        border-radius: 6px;
        padding: 8px;
        background-color: #34495e;
        color: #ecf0f1;
        min-width: 60px;
    }
    QSpinBox:focus, QDoubleSpinBox:focus {
        border: 2px solid #3498db;
    }
    QScrollBar:vertical {
        background: #34495e;
        width: 15px;
        border-radius: 7px;
    }
    QScrollBar::handle:vertical {
        background: #3498db;
        border-radius: 7px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background: #2980b9;
    }
"""