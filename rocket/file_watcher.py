import glob
import os
import time

from typing import List
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from rocket.utils import gather_glob_paths


class FileWatcher:
    class _Handler(FileSystemEventHandler):
        def __init__(self, watcher_instance):
            self.watcher_instance = watcher_instance

        def on_modified(self, event):
            _current_glob_files = gather_glob_paths(self.watcher_instance.glob_paths)
            if event.src_path in _current_glob_files:
                self.watcher_instance.modified_files.add(event.src_path)
            elif event.is_directory:
                return
            elif os.path.splitext(event.src_path)[1] == ".py":
                self.watcher_instance.modified_files.add(event.src_path)

    def __init__(self, path_to_watch, callback, recursive=True, glob_paths: List[str] = None):
        self.path_to_watch = path_to_watch
        self.callback = callback
        self.recursive = recursive
        self.observer = Observer()
        self.modified_files = set()
        self.glob_paths = glob_paths
        if self.glob_paths is None:
            self.glob_paths = []
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
                    self.callback(list(self.modified_files))
                    self.modified_files.clear()
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def stop(self):
        self.observer.stop()
