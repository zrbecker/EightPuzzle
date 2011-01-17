from setuptools import setup

import sys
import os

APP = 'src/EightPuzzle.py'
APP_NAME = 'Eight Puzzle'
VERSION = '1.0'
DATA = ['data/funny-cat.jpg']

def build_with_py2app():
    setup(
        options=dict(
            py2app=dict(
                site_packages=True,
                resources=DATA,
                plist=dict(
                    CFBundleName               = APP_NAME,
                    CFBundleShortVersionString = VERSION,
                    CFBundleGetInfoString      = APP_NAME + ' ' + VERSION,
                    CFBundleExecutable         = APP_NAME,
                    CFBundleIdentifier         = 'com.zrbecker.' + APP_NAME,
                ),
            ),
        ),
        app=[APP]
    )

def build_with_py2exe():
    pass

if __name__ == '__main__':
    if 'py2app' in sys.argv:
        build_with_py2app()
    elif 'py2exe' in sys.argv:
        build_with_py2exe()
    else:
        setup()
