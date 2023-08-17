import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileWatcher:
    class _Handler(FileSystemEventHandler):
        def __init__(self, watcher_instance):
            self.watcher_instance = watcher_instance

        def on_modified(self, event):
            if event.is_directory:
                return
            if os.path.splitext(event.src_path)[1] == ".py":
                self.watcher_instance.modified_files.append(event.src_path)

    def __init__(self, path_to_watch, callback, recursive=True):
        self.path_to_watch = path_to_watch
        self.callback = callback
        self.recursive = recursive
        self.observer = Observer()
        self.modified_files = []
        self.handler = self._Handler(self)

    def start(self):
        self.observer.schedule(
            self.handler, self.path_to_watch, recursive=self.recursive
        )
        self.observer.start()
        try:
            while True:
                time.sleep(1)
                if self.modified_files:
                    self.callback(self.modified_files)
                    self.modified_files.clear()
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def stop(self):
        self.observer.stop()
