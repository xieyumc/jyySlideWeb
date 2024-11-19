import os
from daphne.cli import CommandLineInterface

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jyy_slide_web.settings')
    CommandLineInterface().run(['-b', '0.0.0.0', '-p', '10001', 'jyy_slide_web.asgi:application'])
