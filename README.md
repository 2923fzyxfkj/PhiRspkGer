# Phira资源包生成器

一个基于Python和PyQt6的图形界面工具，用于生成Phira游戏的自定义资源包。

## 功能特性

- 现代化深色主题界面，美观易用，合理布局控件
- 支持导入各种游戏元素（Tap、Drag、Flick及其双押图像）
- 支持导入音频文件（打击音、结束音乐）
- 新增：支持"打击特效宽有几帧"和"打击特效高有几帧"设置
- 新增：支持上传打击特效图片
- 新增：界面支持滚动条，适应不同屏幕尺寸
- 自动生成info.yml配置文件
- 一键打包为ZIP格式资源包

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 运行主程序：
```bash
python main.py
```

2. 在界面中填写资源包的基本信息：
   - 资源包名称
   - 作者
   - 简介

3. 导入各类图像文件：
   - Tap图像和Tap双押图像
   - Drag图像和Drag双押图像
   - Flick图像和Flick双押图像

4. 导入音频文件：
   - 各类打击音
   - 结束音乐

5. 设置打击特效参数：
   - 特效总尺寸
   - 单帧尺寸
   - 持续时间
   - 缩放比例
   - 是否允许旋转
   - 特效网格行列数（新增）
   - 上传特效图片（新增）

6. 选择输出路径

7. 点击"开始生成"按钮

## 生成的资源包结构

生成的ZIP文件包含以下内容：
- click.png - Tap图像
- click_mh.png - Tap双押图像
- drag.png - Drag图像
- drag_mh.png - Drag双押图像
- flick.png - Flick图像
- flick_mh.png - Flick双押图像
- hitFx.png - 打击特效图像
- info.yml - 配置文件
- 各种音频文件

## info.yml配置说明

生成的info.yml文件包含以下字段：
- name: 资源包名称
- author: 作者
- description: 描述
- hitFx: 打击特效尺寸 [width, height]
- hitFxDuration: 特效持续时间
- hitFxScale: 特效缩放比例
- hitFxRotate: 是否允许特效旋转
- audio: 音频文件映射

## 多语言支持

本项目还提供了多种编程语言的实现版本，位于 `multilang/` 目录中：

- **C++版本**: 高性能，适合系统级应用
- **JavaScript/Node.js版本**: 跨平台，易于部署
- **Rust版本**: 内存安全，高性能
- **Lua版本**: 轻量级，嵌入性强
- **Java版本**: 跨平台，企业级应用

每个版本都实现了相同的核心功能，用户可根据自己的技术栈选择合适的版本。

## Android版本

本项目还提供了Android版本，使用Kivy框架开发，可通过以下方式构建：

1. 安装构建工具：
```bash
pip install buildozer cython
```

2. 准备构建环境（Linux/macOS环境下）：
```bash
buildozer init
```

3. 构建APK：
```bash
buildozer android debug
```

或者使用项目提供的构建脚本：
```bash
python build_apk.py
```

Android版本具有与桌面版相同的全部功能，包括：
- 基本信息设置
- 音频文件导入
- 图像文件导入
- 打击特效参数设置（包括新增的行列帧数和图片上传功能）
- Hold Atlas参数设置
- 资源包生成和导出

注意：由于PyQt6在Android上兼容性不佳，Android版本专门使用Kivy框架开发，更适合移动端部署。

## 开发说明

项目包含三个主要模块：
- `main.py`: 程序入口点
- `ui/main_window.py`: 用户界面和交互逻辑
- `core/resource_pack_generator.py`: 资源包生成核心逻辑

还有一个Android适配版本：
- `android_version.py`: Kivy界面，适用于移动设备

## 界面特色

- 深色主题设计，减少眼部疲劳
- 现代化控件样式，提升用户体验
- 统一的颜色搭配，专业美观
- 响应式布局，充分利用屏幕空间
- 优化的视觉层次，重要控件突出显示
- 滚动条支持，适应不同屏幕尺寸

## 系统要求

- Python 3.8+
- PyQt6
- Pillow
- PyYAML

对于Android构建：
- Linux/macOS系统（Windows需要WSL）
- Buildozer
- Android SDK/NDK