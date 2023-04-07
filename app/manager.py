#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from application import app, manager
from flask_script import Server
import www

##web server
manager.add_command(
    "runserver",
    Server(host='0.0.0.0',
           port=app.config['SERVER_PORT'],
           use_debugger=True,
           use_reloader=True))

def main():
    #app.run(host="0.0.0.0", debug=True)
    #通过manager方式就直接运行如下命令就好
    manager.run()


if __name__ == '__main__':
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()