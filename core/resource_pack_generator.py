"""
Phira资源包生成器核心逻辑
负责处理资源包生成的各种操作
"""
import os
import shutil
import zipfile
import tempfile
from PIL import Image
import yaml
from config.constants import IMAGE_MAPPINGS, AUDIO_MAPPINGS


class ResourcePackGenerator:
    def __init__(self, params):
        self.params = params
        self.temp_dir = None

    def generate(self):
        """
        生成资源包的主要方法
        返回: (success: bool, message: str)
        """
        try:
            # 创建临时目录
            self.temp_dir = tempfile.mkdtemp(prefix='phira_pack_')
            
            # 复制基本图像文件
            self.copy_basic_images()
            
            # 处理打击特效
            self.process_hit_effects()
            
            # 生成info.yml文件
            self.generate_info_yml()
            
            # 打包为ZIP文件
            zip_path = self.create_zip_package()
            
            # 清理临时目录
            self.cleanup()
            
            return True, zip_path
            
        except Exception as e:
            # 如果出错也要清理临时目录
            if self.temp_dir:
                self.cleanup()
            return False, str(e)

    def copy_basic_images(self):
        """复制基础图像文件"""
        for param_key, dest_filename in IMAGE_MAPPINGS.items():
            src_path = self.params.get(param_key)
            if src_path and os.path.exists(src_path):
                dest_path = os.path.join(self.temp_dir, dest_filename)
                shutil.copy2(src_path, dest_path)

    def process_hit_effects(self):
        """处理打击特效"""
        # 检查是否提供了特效图片
        if self.params['hit_fx_image'] and os.path.exists(self.params['hit_fx_image']):
            # 如果提供了特效图片，则复制该图片到目标目录
            dest_path = os.path.join(self.temp_dir, 'hit_fx.png')
            shutil.copy2(self.params['hit_fx_image'], dest_path)
        else:
            # 如果没有提供特效图片，则创建一个示例特效图像
            total_width = self.params['fx_total_width']
            total_height = self.params['fx_total_height']
            frame_width = self.params['fx_frame_width']
            frame_height = self.params['fx_frame_height']
            
            # 计算网格
            cols = self.params['fx_cols']
            rows = self.params['fx_rows']
            total_frames = cols * rows
            
            fx_image_path = os.path.join(self.temp_dir, 'hitFx.png')
            
            # 创建一个示例特效图像
            fx_img = Image.new('RGBA', (total_width, total_height), (255, 255, 255, 0))
            
            # 在每个帧位置绘制不同颜色的方块以示区分
            for row in range(rows):
                for col in range(cols):
                    x = col * frame_width
                    y = row * frame_height
                    
                    # 根据位置计算颜色
                    r = (row * 30) % 256
                    g = (col * 50) % 256
                    b = ((row + col) * 20) % 256
                    
                    for i in range(frame_width):
                        for j in range(frame_height):
                            fx_img.putpixel((x + i, y + j), (r, g, b, 255))
            
            fx_img.save(fx_image_path)

    def generate_info_yml(self):
        """生成info.yml文件"""
        info_data = {
            'name': self.params['name'],
            'author': self.params['author'],
            'description': self.params['description'],
            'hitFx': [self.params['fx_cols'], self.params['fx_rows']],
            'hitFxDuration': self.params['fx_duration'],
            'hitFxScale': self.params['fx_scale'],
            'hitFxRotate': self.params['fx_rotate']
        }
        
        # 添加holdAtlas参数（如果存在）
        if 'hold_atlas_x' in self.params and 'hold_atlas_y' in self.params:
            info_data['holdAtlas'] = [self.params['hold_atlas_x'], self.params['hold_atlas_y']]
        if 'hold_atlas_mh_x' in self.params and 'hold_atlas_mh_y' in self.params:
            info_data['holdAtlasMH'] = [self.params['hold_atlas_mh_x'], self.params['hold_atlas_mh_y']]
        
        # 如果有音频文件，添加到info.yml中
        audio_files = {}
        for param_key, audio_key in AUDIO_MAPPINGS.items():
            src_path = self.params.get(param_key)
            if src_path and os.path.exists(src_path):
                audio_files[audio_key] = os.path.basename(src_path)
                # 复制音频文件
                dest_path = os.path.join(self.temp_dir, os.path.basename(src_path))
                shutil.copy2(src_path, dest_path)
        
        if audio_files:
            info_data['audio'] = audio_files
        
        # 写入info.yml文件
        info_yml_path = os.path.join(self.temp_dir, 'info.yml')
        with open(info_yml_path, 'w', encoding='utf-8') as f:
            yaml.dump(info_data, f, default_flow_style=False, allow_unicode=True)

    def create_zip_package(self):
        """创建ZIP压缩包"""
        output_dir = self.params['output_path']
        package_name = f"{self.params['name'].replace(' ', '_')}_ResourcePack.zip"
        zip_path = os.path.join(output_dir, package_name)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.temp_dir)
                    zipf.write(file_path, arcname)
        
        return zip_path

    def cleanup(self):
        """清理临时目录"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)