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

# 如果有媒体文件夹，添加 media 目录
add_data_dir('media', 'media')

# 如果使用 SQLite 数据库，确保数据库文件不被打包，以免覆盖用户数据
db_file = os.path.join(project_root, 'db.sqlite3')
if os.path.exists(db_file):
    datas.append((db_file, '.'))
else:
    print(f"Warning: Database file '{db_file}' does not exist, skipped.")
# 可以在初次运行时创建数据库，或者在打包前复制数据库文件到目标机器

a = Analysis(
    ['run_daphne.py'],
    pathex=[project_root],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='jyy_slide_web',
    debug=False,
    strip=False,
    upx=True,
    console=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='jyy_slide_web'
)