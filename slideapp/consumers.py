# slideapp/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
import tempfile
import os
import shutil
from .src.converter import converter
from django.conf import settings
from .models import Slide
from asgiref.sync import sync_to_async

class SlideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 获取 URL 中的 slide_id 参数
        self.slide_id = self.scope['url_route']['kwargs'].get('slide_id')
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'load':
            # 加载指定的 PPT 内容
            content = await self.get_slide_content()
            await self.send(text_data=json.dumps({
                'action': 'load',
                'content': content
            }))
        elif action == 'save':
            # 保存当前的 PPT 内容
            markdown_content = data['markdown']
            await self.save_slide_content(markdown_content)

            # 继续处理转换和预览
            html_content = await self.convert_markdown_to_html(markdown_content)
            await self.send(text_data=json.dumps({
                'action': 'preview',
                'html': html_content
            }))
        elif action == 'preview':
            # 仅生成预览，不保存
            markdown_content = data['markdown']
            html_content = await self.convert_markdown_to_html(markdown_content)
            await self.send(text_data=json.dumps({
                'action': 'preview',
                'html': html_content
            }))

    @sync_to_async
    def get_slide_content(self):
        slide = Slide.objects.get(id=self.slide_id)
        return slide.content

    @sync_to_async
    def save_slide_content(self, content):
        slide = Slide.objects.get(id=self.slide_id)
        slide.content = content

        # 跳过 YAML 元数据
        lines = content.split('\n')
        in_front_matter = False
        content_started = False
        title = '未命名幻灯片'

        for line in lines:
            stripped_line = line.strip()

            # 检查 YAML 分隔符 '---' 或 '+++'
            if stripped_line == '---' or stripped_line == '+++':
                if not in_front_matter:
                    in_front_matter = True
                else:
                    in_front_matter = False
                continue

            if in_front_matter:
                continue

            if stripped_line.startswith('#'):
                title = stripped_line.lstrip('#').strip()
                break

        slide.title = title
        slide.save()

    async def convert_markdown_to_html(self, markdown_content):
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

            return html_content