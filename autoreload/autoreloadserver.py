# -*- coding: utf-8 -*-

"""
    WebSocket server for detecting file modification.
"""

import argparse
import traceback

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

server = None
clients = set()


class RefreshEventHandler(FileSystemEventHandler):
    def __init__(self, message):
        self.message = message

    def on_any_event(self, event):
        target_extensions = [
            '.css',
            '.jpg',
            '.js',
            '.html',
            '.png',
            '.py',
        ]
        for extension in target_extensions:
            if event.src_path.lower().endswith(extension):
                print 'Modification detected:', event.src_path
                for client in clients:
                    client.sendMessage(self.message)
                break


class FileModificationDetector(WebSocket):
    def handleConnected(self):
        print self.address, 'connected'
        clients.add(self)

    def handleClose(self):
        if self in clients:
            clients.remove(self)


def main(args):
    observer = Observer()
    path = args.dir
    event_handler = RefreshEventHandler(args.message.decode('utf-8'))
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    server = None
    try:
        server = SimpleWebSocketServer('', args.port, FileModificationDetector)
        print 'WebSocket server starts on 127.0.0.1:{}'.format(args.port)
        server.serveforever()
    except:
        pass

    if server:
        server.close()
        print ''
        print ''
        print 'Closed server.'
    else:
        print traceback.format_exc()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dir',
        dest='dir',
        help='Folder to be watched.',
        required=True,
    )
    parser.add_argument(
        '-p', '--port',
        default=16000,
        dest='port',
        help='Server port.',
        type=int,
    )
    parser.add_argument(
        '-m', '--message',
        default='reload',
        dest='message',
        help='Message to be sent to clients.',
        type=str,
    )
    args = parser.parse_args()
    main(args)
