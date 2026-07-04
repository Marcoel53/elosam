"""
ELOSam File Watcher (simple polling version)
"""

import time
import os
from datetime import datetime


class FileWatcher:
    def __init__(self, path="src", interval=3):
        self.path = path
        self.interval = interval
        self.last_state = {}

    def snapshot(self):
        state = {}
        for root, _, files in os.walk(self.path):
            for f in files:
                if f.endswith(".py"):
                    full = os.path.join(root, f)
                    state[full] = os.path.getmtime(full)
        return state

    def detect_changes(self):
        new_state = self.snapshot()
        changes = []

        for file, mtime in new_state.items():
            if file not in self.last_state:
                changes.append(("CREATED", file))
            elif self.last_state[file] != mtime:
                changes.append(("MODIFIED", file))

        self.last_state = new_state
        return changes
