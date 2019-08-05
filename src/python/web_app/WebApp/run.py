#!/bin/env python
"""
Author: David Crook
Copyright: Microsoft Corporation 2019
"""

from webapp.app import create_app, socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=80)
#app.run(host='0.0.0.0', port=80)
