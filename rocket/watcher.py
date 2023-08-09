import os

from watchdog.events import FileSystemEventHandler


class Watcher(FileSystemEventHandler):

    def __init__(self, observer):
        self.modified_files = []
        self.observer = observer

    def on_modified(self, event):
        if event.is_directory:
            return
        if os.path.splitext(event.src_path)[1] == '.py':
            self.modified_files.append(event.src_path)
            self.observer.stop()