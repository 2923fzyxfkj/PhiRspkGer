"""
Phira资源包生成器的UI界面
"""
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QFileDialog, QTextEdit, QGroupBox, QGridLayout,
                             QMessageBox, QSpinBox, QDoubleSpinBox, QScrollArea)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette
from PIL import Image
import core.resource_pack_generator
from config.constants import (
    APP_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, DARK_THEME_STYLESHEET,
    DEFAULT_FX_COLS, DEFAULT_FX_ROWS, DEFAULT_FX_TOTAL_WIDTH, DEFAULT_FX_TOTAL_HEIGHT,
    DEFAULT_FX_FRAME_WIDTH, DEFAULT_FX_FRAME_HEIGHT, DEFAULT_FX_DURATION, 
    DEFAULT_FX_SCALE, DEFAULT_FX_ROTATE, AUDIO_FILTER, IMAGE_FILTER, AUDIO_MAPPINGS,
    DEFAULT_HOLD_ATLAS, DEFAULT_HOLD_ATLAS_MH
)


class GenerateWorker(QThread):
    """用于在后台生成资源包的线程"""
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, params):
        super().__init__()
        self.params = params

    def run(self):
        try:
            generator = resource_pack_generator.ResourcePackGenerator(self.params)
            success, message = generator.generate()
            self.finished_signal.emit(success, message)
        except Exception as e:
            self.finished_signal.emit(False, f"生成过程中发生错误: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 创建一个滚动区域作为中央部件
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # 创建内容小部件
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        
        # 设置主窗口属性
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # 设置现代化的深色主题样式
        self.setStyleSheet(DARK_THEME_STYLESHEET)
        
        # 设置内容小部件的布局
        main_layout = QVBoxLayout(content_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加标题
        title_label = QLabel("Phira资源包生成器")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            margin: 15px; 
            color: #ecf0f1;
            background: transparent;
            border: none;
        """)
        main_layout.addWidget(title_label)
        
        # 基本信息组
        basic_info_group = self.create_basic_info_group()
        main_layout.addWidget(basic_info_group)
        
        # 音频文件组
        audio_group = self.create_audio_group()
        main_layout.addWidget(audio_group)
        
        # 图片文件组
        images_group = self.create_images_group()
        main_layout.addWidget(images_group)
        
        # 特效参数组
        fx_group = self.create_fx_group()
        main_layout.addWidget(fx_group)
        
        # Hold Atlas参数组
        hold_atlas_group = self.create_hold_atlas_group()
        main_layout.addWidget(hold_atlas_group)
        
        # 输出路径组
        output_group = self.create_output_group()
        main_layout.addWidget(output_group)
        
        # 控制按钮组
        button_layout = QHBoxLayout()
        
        self.generate_button = QPushButton("开始生成")
        self.generate_button.setObjectName("generate_button")
        self.generate_button.setStyleSheet("""
            QPushButton#generate_button {
                background-color: #2ecc71;
                font-weight: bold;
                min-height: 40px;
                font-size: 14px;
                padding: 12px 20px;
            }
            QPushButton#generate_button:hover {
                background-color: #27ae60;
            }
            QPushButton#generate_button:pressed {
                background-color: #219653;
            }
        """)
        self.generate_button.clicked.connect(self.start_generation)
        button_layout.addWidget(self.generate_button)
        
        self.clear_button = QPushButton("清空")
        self.clear_button.setObjectName("clear_button")
        self.clear_button.setStyleSheet("""
            QPushButton#clear_button {
                background-color: #e74c3c;
                font-weight: bold;
                min-height: 40px;
                font-size: 14px;
                padding: 12px 20px;
            }
            QPushButton#clear_button:hover {
                background-color: #c0392b;
            }
            QPushButton#clear_button:pressed {
                background-color: #a93226;
            }
        """)
        self.clear_button.clicked.connect(self.clear_all_fields)
        button_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(button_layout)
        
        # 日志输出框
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setMaximumHeight(150)
        self.log_text_edit.setReadOnly(True)
        main_layout.addWidget(QLabel("日志输出:"))
        main_layout.addWidget(self.log_text_edit)
        
        # 设置中央部件
        self.setCentralWidget(scroll_area)
        
        # 初始化生成器工作线程
        self.worker = None
        
    def create_basic_info_group(self):
        group = QGroupBox("基本信息")
        layout = QGridLayout()
        
        # 资源包名称
        layout.addWidget(QLabel("资源包名称:"), 0, 0)
        self.name_line_edit = QLineEdit()
        layout.addWidget(self.name_line_edit, 0, 1, 1, 2)  # 跨越两列
        
        # 资源包作者
        layout.addWidget(QLabel("资源包作者:"), 0, 3)
        self.author_line_edit = QLineEdit()
        layout.addWidget(self.author_line_edit, 0, 4, 1, 2)  # 跨越两列
        
        # 资源包简介
        layout.addWidget(QLabel("资源包简介:"), 1, 0)
        self.description_text_edit = QTextEdit()
        self.description_text_edit.setMaximumHeight(60)
        layout.addWidget(self.description_text_edit, 1, 1, 1, 5)  # 跨越所有剩余列
        
        group.setLayout(layout)
        return group
    
    def create_audio_group(self):
        group = QGroupBox("音频文件")
        layout = QVBoxLayout()  # 改为垂直布局
        
        # 第一行：Tap打击音和Drag打击音
        row1_layout = QHBoxLayout()
        # Tap打击音
        tap_label = QLabel("Tap打击音:")
        tap_label.setFixedWidth(80)
        row1_layout.addWidget(tap_label)
        self.tap_sound_line_edit = QLineEdit()
        self.tap_sound_line_edit.setMinimumWidth(200)
        row1_layout.addWidget(self.tap_sound_line_edit)
        self.tap_sound_button = QPushButton("浏览...")
        self.tap_sound_button.setObjectName("browse_button")
        self.tap_sound_button.clicked.connect(lambda: self.browse_file(self.tap_sound_line_edit, "选择Tap打击音", AUDIO_FILTER))
        row1_layout.addWidget(self.tap_sound_button)
        
        # Drag打击音
        drag_label = QLabel("Drag打击音:")
        drag_label.setFixedWidth(80)
        row1_layout.addWidget(drag_label)
        self.drag_sound_line_edit = QLineEdit()
        self.drag_sound_line_edit.setMinimumWidth(200)
        row1_layout.addWidget(self.drag_sound_line_edit)
        self.drag_sound_button = QPushButton("浏览...")
        self.drag_sound_button.setObjectName("browse_button")
        self.drag_sound_button.clicked.connect(lambda: self.browse_file(self.drag_sound_line_edit, "选择Drag打击音", AUDIO_FILTER))
        row1_layout.addWidget(self.drag_sound_button)
        row1_layout.addStretch()  # 添加弹性空间
        layout.addLayout(row1_layout)
        
        # 第二行：Flick打击音和结束音乐
        row2_layout = QHBoxLayout()
        # Flick打击音
        flick_label = QLabel("Flick打击音:")
        flick_label.setFixedWidth(80)
        row2_layout.addWidget(flick_label)
        self.flick_sound_line_edit = QLineEdit()
        self.flick_sound_line_edit.setMinimumWidth(200)
        row2_layout.addWidget(self.flick_sound_line_edit)
        self.flick_sound_button = QPushButton("浏览...")
        self.flick_sound_button.setObjectName("browse_button")
        self.flick_sound_button.clicked.connect(lambda: self.browse_file(self.flick_sound_line_edit, "选择Flick打击音", AUDIO_FILTER))
        row2_layout.addWidget(self.flick_sound_button)
        
        # 结束音乐
        end_label = QLabel("结束音乐:")
        end_label.setFixedWidth(80)
        row2_layout.addWidget(end_label)
        self.end_music_line_edit = QLineEdit()
        self.end_music_line_edit.setMinimumWidth(200)
        row2_layout.addWidget(self.end_music_line_edit)
        self.end_music_button = QPushButton("浏览...")
        self.end_music_button.setObjectName("browse_button")
        self.end_music_button.clicked.connect(lambda: self.browse_file(self.end_music_line_edit, "选择结束音乐", AUDIO_FILTER))
        row2_layout.addWidget(self.end_music_button)
        row2_layout.addStretch()  # 添加弹性空间
        layout.addLayout(row2_layout)
        
        group.setLayout(layout)
        return group
    
    def create_images_group(self):
        group = QGroupBox("图像文件")
        layout = QVBoxLayout()  # 改为垂直布局
        
        # 第一行：Tap图像和Tap双押图像
        row1_layout = QHBoxLayout()
        # Tap图像
        tap_label = QLabel("Tap图像:")
        tap_label.setFixedWidth(80)
        row1_layout.addWidget(tap_label)
        self.tap_image_line_edit = QLineEdit()
        self.tap_image_line_edit.setMinimumWidth(200)
        row1_layout.addWidget(self.tap_image_line_edit)
        self.tap_image_button = QPushButton("浏览...")
        self.tap_image_button.setObjectName("browse_button")
        self.tap_image_button.clicked.connect(lambda: self.browse_file(self.tap_image_line_edit, "选择Tap图像", IMAGE_FILTER))
        row1_layout.addWidget(self.tap_image_button)
        
        # Tap双押图像
        tap_mh_label = QLabel("Tap双押图像:")
        tap_mh_label.setFixedWidth(100)
        row1_layout.addWidget(tap_mh_label)
        self.tap_mh_image_line_edit = QLineEdit()
        self.tap_mh_image_line_edit.setMinimumWidth(200)
        row1_layout.addWidget(self.tap_mh_image_line_edit)
        self.tap_mh_image_button = QPushButton("浏览...")
        self.tap_mh_image_button.setObjectName("browse_button")
        self.tap_mh_image_button.clicked.connect(lambda: self.browse_file(self.tap_mh_image_line_edit, "选择Tap双押图像", IMAGE_FILTER))
        row1_layout.addWidget(self.tap_mh_image_button)
        row1_layout.addStretch()  # 添加弹性空间
        layout.addLayout(row1_layout)
        
        # 第二行：Drag图像和Drag双押图像
        row2_layout = QHBoxLayout()
        # Drag图像
        drag_label = QLabel("Drag图像:")
        drag_label.setFixedWidth(80)
        row2_layout.addWidget(drag_label)
        self.drag_image_line_edit = QLineEdit()
        self.drag_image_line_edit.setMinimumWidth(200)
        row2_layout.addWidget(self.drag_image_line_edit)
        self.drag_image_button = QPushButton("浏览...")
        self.drag_image_button.setObjectName("browse_button")
        self.drag_image_button.clicked.connect(lambda: self.browse_file(self.drag_image_line_edit, "选择Drag图像", IMAGE_FILTER))
        row2_layout.addWidget(self.drag_image_button)
        
        # Drag双押图像
        drag_mh_label = QLabel("Drag双押图像:")
        drag_mh_label.setFixedWidth(100)
        row2_layout.addWidget(drag_mh_label)
        self.drag_mh_image_line_edit = QLineEdit()
        self.drag_mh_image_line_edit.setMinimumWidth(200)
        row2_layout.addWidget(self.drag_mh_image_line_edit)
        self.drag_mh_image_button = QPushButton("浏览...")
        self.drag_mh_image_button.setObjectName("browse_button")
        self.drag_mh_image_button.clicked.connect(lambda: self.browse_file(self.drag_mh_image_line_edit, "选择Drag双押图像", IMAGE_FILTER))
        row2_layout.addWidget(self.drag_mh_image_button)
        row2_layout.addStretch()  # 添加弹性空间
        layout.addLayout(row2_layout)
        
        # 第三行：Flick图像和Flick双押图像
        row3_layout = QHBoxLayout()
        # Flick图像
        flick_label = QLabel("Flick图像:")
        flick_label.setFixedWidth(80)
        row3_layout.addWidget(flick_label)
        self.flick_image_line_edit = QLineEdit()
        self.flick_image_line_edit.setMinimumWidth(200)
        row3_layout.addWidget(self.flick_image_line_edit)
        self.flick_image_button = QPushButton("浏览...")
        self.flick_image_button.setObjectName("browse_button")
        self.flick_image_button.clicked.connect(lambda: self.browse_file(self.flick_image_line_edit, "选择Flick图像", IMAGE_FILTER))
        row3_layout.addWidget(self.flick_image_button)
        
        # Flick双押图像
        flick_mh_label = QLabel("Flick双押图像:")
        flick_mh_label.setFixedWidth(100)
        row3_layout.addWidget(flick_mh_label)
        self.flick_mh_image_line_edit = QLineEdit()
        self.flick_mh_image_line_edit.setMinimumWidth(200)
        row3_layout.addWidget(self.flick_mh_image_line_edit)
        self.flick_mh_image_button = QPushButton("浏览...")
        self.flick_mh_image_button.setObjectName("browse_button")
        self.flick_mh_image_button.clicked.connect(lambda: self.browse_file(self.flick_mh_image_line_edit, "选择Flick双押图像", IMAGE_FILTER))
        row3_layout.addWidget(self.flick_mh_image_button)
        row3_layout.addStretch()  # 添加弹性空间
        layout.addLayout(row3_layout)
        
        # 第四行：Hold图像和Hold双押图像
        row4_layout = QHBoxLayout()
        # Hold图像
        hold_label = QLabel("Hold图像:")
        hold_label.setFixedWidth(80)
        row4_layout.addWidget(hold_label)
        self.hold_image_line_edit = QLineEdit()
        self.hold_image_line_edit.setMinimumWidth(200)
        row4_layout.addWidget(self.hold_image_line_edit)
        self.hold_image_button = QPushButton("浏览...")
        self.hold_image_button.setObjectName("browse_button")
        self.hold_image_button.clicked.connect(lambda: self.browse_file(self.hold_image_line_edit, "选择Hold图像", IMAGE_FILTER, is_hold=True))
        row4_layout.addWidget(self.hold_image_button)
        
        # Hold双押图像
        hold_mh_label = QLabel("Hold双押图像:")
        hold_mh_label.setFixedWidth(100)
        row4_layout.addWidget(hold_mh_label)
        self.hold_mh_image_line_edit = QLineEdit()
        self.hold_mh_image_line_edit.setMinimumWidth(200)
        row4_layout.addWidget(self.hold_mh_image_line_edit)
        self.hold_mh_image_button = QPushButton("浏览...")
        self.hold_mh_image_button.setObjectName("browse_button")
        self.hold_mh_image_button.clicked.connect(lambda: self.browse_file(self.hold_mh_image_line_edit, "选择Hold双押图像", IMAGE_FILTER, is_hold_mh=True))
        row4_layout.addWidget(self.hold_mh_image_button)
        row4_layout.addStretch()  # 添加弹性空间
        layout.addLayout(row4_layout)
        
        group.setLayout(layout)
        return group
    
    def create_fx_group(self):
        group = QGroupBox("打击特效参数")
        layout = QVBoxLayout()  # 改为垂直布局
        
        # 第一行：特效宽有几帧 和 特效高有几帧
        row1_layout = QHBoxLayout()
        # 特效宽有几帧
        label1 = QLabel("打击特效宽有几帧:")
        label1.setFixedWidth(120)
        row1_layout.addWidget(label1)
        self.fx_cols_spinbox = QSpinBox()
        self.fx_cols_spinbox.setRange(1, 50)
        self.fx_cols_spinbox.setValue(DEFAULT_FX_COLS)
        row1_layout.addWidget(self.fx_cols_spinbox)
        
        # 特效高有几帧
        label2 = QLabel("打击特效高有几帧:")
        label2.setFixedWidth(120)
        row1_layout.addWidget(label2)
        self.fx_rows_spinbox = QSpinBox()
        self.fx_rows_spinbox.setRange(1, 50)
        self.fx_rows_spinbox.setValue(DEFAULT_FX_ROWS)
        row1_layout.addWidget(self.fx_rows_spinbox)
        row1_layout.addStretch()  # 添加弹性空间
        layout.addLayout(row1_layout)
        
        # 第二行：特效总长度 和 特效总宽度
        row2_layout = QHBoxLayout()
        # 特效总长度
        label3 = QLabel("打击特效总长度:")
        label3.setFixedWidth(100)
        row2_layout.addWidget(label3)
        self.fx_total_width_spinbox = QSpinBox()
        self.fx_total_width_spinbox.setRange(1, 2000)
        self.fx_total_width_spinbox.setValue(DEFAULT_FX_TOTAL_WIDTH)
        row2_layout.addWidget(self.fx_total_width_spinbox)
        
        # 特效总宽度
        label4 = QLabel("打击特效总宽度:")
        label4.setFixedWidth(100)
        row2_layout.addWidget(label4)
        self.fx_total_height_spinbox = QSpinBox()
        self.fx_total_height_spinbox.setRange(1, 2000)
        self.fx_total_height_spinbox.setValue(DEFAULT_FX_TOTAL_HEIGHT)
        row2_layout.addWidget(self.fx_total_height_spinbox)
        row2_layout.addStretch()  # 添加弹性空间
        layout.addLayout(row2_layout)
        
        # 第三行：特效帧长度 和 特效帧宽度
        row3_layout = QHBoxLayout()
        # 特效帧长度
        label5 = QLabel("单帧长度:")
        label5.setFixedWidth(80)
        row3_layout.addWidget(label5)
        self.fx_frame_width_spinbox = QSpinBox()
        self.fx_frame_width_spinbox.setRange(1, 2147483647)
        self.fx_frame_width_spinbox.setValue(DEFAULT_FX_FRAME_WIDTH)
        row3_layout.addWidget(self.fx_frame_width_spinbox)
        
        # 特效帧宽度
        label6 = QLabel("单帧宽度:")
        label6.setFixedWidth(80)
        row3_layout.addWidget(label6)
        self.fx_frame_height_spinbox = QSpinBox()
        self.fx_frame_height_spinbox.setRange(1, 2147483647)
        self.fx_frame_height_spinbox.setValue(DEFAULT_FX_FRAME_HEIGHT)
        row3_layout.addWidget(self.fx_frame_height_spinbox)
        row3_layout.addStretch()  # 添加弹性空间
        layout.addLayout(row3_layout)
        
        # 第四行：特效持续时间 和 特效缩放
        row4_layout = QHBoxLayout()
        # 特效持续时间
        label7 = QLabel("特效持续时间:")
        label7.setFixedWidth(100)
        row4_layout.addWidget(label7)
        self.fx_duration_spinbox = QDoubleSpinBox()
        self.fx_duration_spinbox.setRange(0.1, 5.0)
        self.fx_duration_spinbox.setSingleStep(0.05)
        self.fx_duration_spinbox.setValue(DEFAULT_FX_DURATION)
        row4_layout.addWidget(self.fx_duration_spinbox)
        
        # 特效缩放
        label8 = QLabel("特效缩放:")
        label8.setFixedWidth(80)
        row4_layout.addWidget(label8)
        self.fx_scale_spinbox = QDoubleSpinBox()
        self.fx_scale_spinbox.setRange(0.1, 5.0)
        self.fx_scale_spinbox.setSingleStep(0.1)
        self.fx_scale_spinbox.setValue(DEFAULT_FX_SCALE)
        row4_layout.addWidget(self.fx_scale_spinbox)
        row4_layout.addStretch()  # 添加弹性空间
        layout.addLayout(row4_layout)
        
        # 第五行：特效是否旋转 和 打击特效图片标签
        row5_layout = QHBoxLayout()
        label9 = QLabel("特效可旋转:")
        label9.setFixedWidth(80)
        row5_layout.addWidget(label9)
        self.fx_rotate_checkbox = QPushButton("是")
        self.fx_rotate_checkbox.setCheckable(True)
        self.fx_rotate_checkbox.setChecked(DEFAULT_FX_ROTATE)
        self.fx_rotate_checkbox.clicked.connect(lambda: self.fx_rotate_checkbox.setText("是" if self.fx_rotate_checkbox.isChecked() else "否"))
        self.fx_rotate_checkbox.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                border: 2px solid #27ae60;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 60px;
            }
            QPushButton:checked {
                background-color: #e74c3c;
                border: 2px solid #c0392b;
            }
        """)
        row5_layout.addWidget(self.fx_rotate_checkbox)
        
        # 打击特效图片标签（留空位置，下一行放实际控件）
        label10 = QLabel("打击特效图片:")
        label10.setFixedWidth(100)
        row5_layout.addWidget(label10)
        row5_layout.addStretch()  # 添加弹性空间
        layout.addLayout(row5_layout)
        
        # 第六行：上传打击特效图片（单独一行，因为路径输入框需要更多空间）
        row6_layout = QHBoxLayout()
        self.hit_fx_image_line_edit = QLineEdit()
        self.hit_fx_image_line_edit.setPlaceholderText("选择打击特效图片文件")
        row6_layout.addWidget(self.hit_fx_image_line_edit)
        self.hit_fx_image_button = QPushButton("浏览...")
        self.hit_fx_image_button.setObjectName("browse_button")
        self.hit_fx_image_button.clicked.connect(lambda: self.browse_file(self.hit_fx_image_line_edit, "选择打击特效图片", IMAGE_FILTER))
        row6_layout.addWidget(self.hit_fx_image_button)
        row6_layout.addStretch()  # 添加弹性空间
        layout.addLayout(row6_layout)
        
        group.setLayout(layout)
        return group
    
    def create_hold_atlas_group(self):
        group = QGroupBox("Hold Atlas参数")
        layout = QHBoxLayout()
        
        # Hold Atlas X坐标
        layout.addWidget(QLabel("holdAtlas X:"))
        self.hold_atlas_x_spinbox = QSpinBox()
        self.hold_atlas_x_spinbox.setRange(0, 200)
        self.hold_atlas_x_spinbox.setValue(DEFAULT_HOLD_ATLAS[0])
        layout.addWidget(self.hold_atlas_x_spinbox)
        
        # Hold Atlas Y坐标
        layout.addWidget(QLabel("holdAtlas Y:"))
        self.hold_atlas_y_spinbox = QSpinBox()
        self.hold_atlas_y_spinbox.setRange(0, 200)
        self.hold_atlas_y_spinbox.setValue(DEFAULT_HOLD_ATLAS[1])
        layout.addWidget(self.hold_atlas_y_spinbox)
        
        # Hold Atlas MH X坐标
        layout.addWidget(QLabel("holdAtlasMH X:"))
        self.hold_atlas_mh_x_spinbox = QSpinBox()
        self.hold_atlas_mh_x_spinbox.setRange(0, 200)
        self.hold_atlas_mh_x_spinbox.setValue(DEFAULT_HOLD_ATLAS_MH[0])
        layout.addWidget(self.hold_atlas_mh_x_spinbox)
        
        # Hold Atlas MH Y坐标
        layout.addWidget(QLabel("holdAtlasMH Y:"))
        self.hold_atlas_mh_y_spinbox = QSpinBox()
        self.hold_atlas_mh_y_spinbox.setRange(0, 200)
        self.hold_atlas_mh_y_spinbox.setValue(DEFAULT_HOLD_ATLAS_MH[1])
        layout.addWidget(self.hold_atlas_mh_y_spinbox)
        
        layout.addStretch()  # 添加弹性空间
        group.setLayout(layout)
        return group
    
    def create_output_group(self):
        group = QGroupBox("输出设置")
        layout = QHBoxLayout()
        
        layout.addWidget(QLabel("输出路径:"))
        self.output_path_line_edit = QLineEdit()
        self.output_path_button = QPushButton("浏览...")
        self.output_path_button.setObjectName("browse_button")
        self.output_path_button.clicked.connect(self.browse_output_directory)
        layout.addWidget(self.output_path_line_edit)
        layout.addWidget(self.output_path_button)
        
        group.setLayout(layout)
        return group
    
    def browse_file(self, line_edit, dialog_title, file_filter, is_hold=False, is_hold_mh=False):
        """浏览文件对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, dialog_title, "", file_filter
        )
        if file_path:
            line_edit.setText(file_path)
            
            # 如果是hold或hold_mh图像，则自动计算atlas坐标
            if is_hold or is_hold_mh:
                try:
                    # 获取图像尺寸
                    with Image.open(file_path) as img:
                        width, height = img.size
                        
                        # 计算中心坐标，作为atlas坐标
                        center_x = width // 2
                        center_y = height // 2
                        
                        # 限制在合理范围内
                        center_x = min(center_x, 200)
                        center_y = min(center_y, 200)
                        
                        if is_hold:
                            # 设置holdAtlas坐标
                            self.hold_atlas_x_spinbox.setValue(center_x)
                            self.hold_atlas_y_spinbox.setValue(center_y)
                        elif is_hold_mh:
                            # 设置holdAtlasMH坐标
                            self.hold_atlas_mh_x_spinbox.setValue(center_x)
                            self.hold_atlas_mh_y_spinbox.setValue(center_y)
                            
                except Exception as e:
                    print(f"无法读取图像文件: {e}")
                    # 如果读取失败，使用默认值
                    if is_hold:
                        self.hold_atlas_x_spinbox.setValue(DEFAULT_HOLD_ATLAS[0])
                        self.hold_atlas_y_spinbox.setValue(DEFAULT_HOLD_ATLAS[1])
                    elif is_hold_mh:
                        self.hold_atlas_mh_x_spinbox.setValue(DEFAULT_HOLD_ATLAS_MH[0])
                        self.hold_atlas_mh_y_spinbox.setValue(DEFAULT_HOLD_ATLAS_MH[1])
    
    def browse_output_directory(self):
        """浏览输出目录对话框"""
        directory = QFileDialog.getExistingDirectory(
            self, "选择输出目录", ""
        )
        if directory:
            self.output_path_line_edit.setText(directory)
    
    def start_generation(self):
        """开始生成资源包"""
        # 收集所有参数
        params = {
            'name': self.name_line_edit.text().strip(),
            'author': self.author_line_edit.text().strip(),
            'description': self.description_text_edit.toPlainText().strip(),
            
            'tap_sound': self.tap_sound_line_edit.text().strip(),
            'drag_sound': self.drag_sound_line_edit.text().strip(),
            'flick_sound': self.flick_sound_line_edit.text().strip(),
            'end_music': self.end_music_line_edit.text().strip(),
            
            'tap_image': self.tap_image_line_edit.text().strip(),
            'tap_mh_image': self.tap_mh_image_line_edit.text().strip(),
            'drag_image': self.drag_image_line_edit.text().strip(),
            'drag_mh_image': self.drag_mh_image_line_edit.text().strip(),
            'flick_image': self.flick_image_line_edit.text().strip(),
            'flick_mh_image': self.flick_mh_image_line_edit.text().strip(),
            'hold_image': self.hold_image_line_edit.text().strip(),
            'hold_mh_image': self.hold_mh_image_line_edit.text().strip(),
            
            'fx_cols': self.fx_cols_spinbox.value(),
            'fx_rows': self.fx_rows_spinbox.value(),
            'fx_total_width': self.fx_total_width_spinbox.value(),
            'fx_total_height': self.fx_total_height_spinbox.value(),
            'fx_frame_width': self.fx_frame_width_spinbox.value(),
            'fx_frame_height': self.fx_frame_height_spinbox.value(),
            'fx_duration': self.fx_duration_spinbox.value(),
            'fx_scale': self.fx_scale_spinbox.value(),
            'fx_rotate': self.fx_rotate_checkbox.isChecked(),
            'hit_fx_image': self.hit_fx_image_line_edit.text().strip(),
            
            'hold_atlas_x': self.hold_atlas_x_spinbox.value(),
            'hold_atlas_y': self.hold_atlas_y_spinbox.value(),
            'hold_atlas_mh_x': self.hold_atlas_mh_x_spinbox.value(),
            'hold_atlas_mh_y': self.hold_atlas_mh_y_spinbox.value(),
            
            'output_path': self.output_path_line_edit.text().strip()
        }
        
        # 验证必要参数
        if not params['name']:
            QMessageBox.warning(self, "警告", "请输入资源包名称")
            return
        if not params['output_path']:
            QMessageBox.warning(self, "警告", "请选择输出路径")
            return
            
        # 禁用生成按钮，防止重复点击
        self.generate_button.setEnabled(False)
        self.log_text_edit.append("开始生成资源包...")
        
        # 创建并启动工作线程
        self.worker = GenerateWorker(params)
        self.worker.progress_signal.connect(self.update_log)
        self.worker.finished_signal.connect(self.on_generation_finished)
        self.worker.start()
    
    def update_log(self, message):
        """更新日志"""
        self.log_text_edit.append(message)
    
    def on_generation_finished(self, success, message):
        """生成完成回调"""
        self.generate_button.setEnabled(True)
        self.log_text_edit.append(message)
        
        if success:
            QMessageBox.information(self, "成功", f"资源包生成成功！\n位置：{message}")
        else:
            QMessageBox.critical(self, "错误", f"资源包生成失败：{message}")
    
    def clear_all_fields(self):
        """清空所有字段"""
        reply = QMessageBox.question(
            self, "确认", "确定要清空所有输入吗？", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.name_line_edit.clear()
            self.author_line_edit.clear()
            self.description_text_edit.clear()
            
            self.tap_sound_line_edit.clear()
            self.drag_sound_line_edit.clear()
            self.flick_sound_line_edit.clear()
            self.end_music_line_edit.clear()
            
            self.tap_image_line_edit.clear()
            self.tap_mh_image_line_edit.clear()
            self.drag_image_line_edit.clear()
            self.drag_mh_image_line_edit.clear()
            self.flick_image_line_edit.clear()
            self.flick_mh_image_line_edit.clear()
            self.hold_image_line_edit.clear()
            self.hold_mh_image_line_edit.clear()
            
            self.output_path_line_edit.clear()
            
            self.fx_cols_spinbox.setValue(DEFAULT_FX_COLS)
            self.fx_rows_spinbox.setValue(DEFAULT_FX_ROWS)
            self.fx_total_width_spinbox.setValue(DEFAULT_FX_TOTAL_WIDTH)
            self.fx_total_height_spinbox.setValue(DEFAULT_FX_TOTAL_HEIGHT)
            self.fx_frame_width_spinbox.setValue(DEFAULT_FX_FRAME_WIDTH)
            self.fx_frame_height_spinbox.setValue(DEFAULT_FX_FRAME_HEIGHT)
            self.fx_duration_spinbox.setValue(DEFAULT_FX_DURATION)
            self.fx_scale_spinbox.setValue(DEFAULT_FX_SCALE)
            self.fx_rotate_checkbox.setChecked(DEFAULT_FX_ROTATE)
            self.fx_rotate_checkbox.setText("是")
            self.hit_fx_image_line_edit.clear()
            
            # 重置Hold Atlas参数
            self.hold_atlas_x_spinbox.setValue(DEFAULT_HOLD_ATLAS[0])
            self.hold_atlas_y_spinbox.setValue(DEFAULT_HOLD_ATLAS[1])
            self.hold_atlas_mh_x_spinbox.setValue(DEFAULT_HOLD_ATLAS_MH[0])
            self.hold_atlas_mh_y_spinbox.setValue(DEFAULT_HOLD_ATLAS_MH[1])
            
            self.log_text_edit.clear()
            self.log_text_edit.append("已清空所有字段")