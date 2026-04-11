#!/usr/local/bin/managed_python3

from docklib import Dock
import os

app_to_add = '/Applications/GIMP.app'

def main():
    if os.path.exists(app_to_add):
        # Based on example from https://github.com/homebysix/docklib?tab=readme-ov-file#add-microsoft-word-to-the-right-side-of-the-dock
        dock = Dock()
        item = dock.makeDockAppEntry(app_to_add)
        dock.items["persistent-apps"].append(item)
        dock.save()

if __name__ == "__main__":
    main()
