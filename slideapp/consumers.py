from channels.generic.websocket import AsyncWebsocketConsumer
import json
import tempfile
import os
import shutil
from .src.converter import converter
from django.conf import settings  # 导入 settings

class SlideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        markdown_content = data['markdown']

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建临时 Markdown 文件
            temp_md_file_path = os.path.join(temp_dir, 'temp.md')
            with open(temp_md_file_path, 'w', encoding='utf-8') as temp_md_file:
                temp_md_file.write(markdown_content)

            # 调用转换器
            converter(temp_md_file_path)

            # 读取生成的 HTML 文件
            output_html_path = os.path.join(temp_dir, 'dist', 'index.html')
            with open(output_html_path, 'r', encoding='utf-8') as html_file:
                html_content = html_file.read()

            # 修改静态文件路径
            html_content = html_content.replace('./static/', '/static/')
            html_content = html_content.replace('./img/', '/static/img/')

            # 复制生成的图片到静态文件目录
            source_img_dir = os.path.join(temp_dir, 'dist', 'img')
            dest_img_dir = os.path.join(settings.BASE_DIR, 'static', 'img')

            if os.path.exists(source_img_dir):
                if not os.path.exists(dest_img_dir):
                    os.makedirs(dest_img_dir)
                for filename in os.listdir(source_img_dir):
                    shutil.copy(os.path.join(source_img_dir, filename), dest_img_dir)

            # 发送 HTML 内容回前端
            await self.send(text_data=json.dumps({
                'html': html_content
            }))