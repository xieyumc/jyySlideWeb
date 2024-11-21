# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# 项目根目录
project_root = os.path.abspath(os.getcwd())

# 收集模块的所有子模块
hiddenimports = (
    collect_submodules('django') +
    collect_submodules('channels') +
    collect_submodules('daphne') +
    collect_submodules('jyy_slide_web') +
    collect_submodules('slideapp') +
    collect_submodules('whitenoise')
)

# 手动指定数据文件
datas = []

def add_data_dir(source_rel_path, target_rel_path):
    source_abs_path = os.path.join(project_root, source_rel_path)
    if os.path.exists(source_abs_path):
        datas.append((source_abs_path, target_rel_path))
    else:
        print(f"Warning: Directory '{source_abs_path}' does not exist, skipped.")

# 添加需要的资源目录
add_data_dir('slideapp/templates', 'slideapp/templates')
add_data_dir('slideapp/src/static', 'slideapp/src/static')
add_data_dir('slideapp/src/backup/template', 'slideapp/src/backup/template')
add_data_dir('jyy_slide_web', 'jyy_slide_web')

# 添加收集后的静态文件目录
add_data_dir('staticfiles', 'staticfiles')

# 添加媒体文件目录
add_data_dir('media', 'media')

# 添加 default_content.md 文件
default_content_path = os.path.join('slideapp', 'default_content.md')
if os.path.exists(default_content_path):
    datas.append((default_content_path, 'slideapp'))
else:
    print(f"Warning: File '{default_content_path}' does not exist, skipped.")

# 如果使用 SQLite 数据库，确保数据库文件不被打包，以免覆盖用户数据
db_file = os.path.join(project_root, 'db.sqlite3')
if os.path.exists(db_file):
    datas.append((db_file, '.'))
else:
    print(f"Warning: Database file '{db_file}' does not exist, skipped.")

# 创建打包分析对象
a = Analysis(
    ['run_daphne.py'],  # 主入口文件
    pathex=[project_root],  # 搜索路径
    binaries=[],  # 需要额外的二进制文件
    datas=datas,  # 数据文件
    hiddenimports=hiddenimports,  # 隐藏导入
    hookspath=[],  # 自定义hook路径
    runtime_hooks=[],  # 运行时hook
    excludes=[],  # 排除的模块
    cipher=block_cipher,  # 加密方法
    noarchive=False  # 是否生成单文件
)

# 创建 PyInstaller 打包步骤
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 可执行文件的配置
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='jyy_slide_web',  # 可执行文件名称
    debug=False,
    strip=False,
    upx=True,
    console=True  # 是否显示控制台窗口
)

# 打包成一个文件夹
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='jyy_slide_web'  # 输出文件夹名称
)