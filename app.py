#! /usr/bin/env python3

from pathlib import Path
from time import sleep

from watchdog.observers import Observer
from download_organizer.EventHandler import EventHandler

if __name__ == '__main__':
    watch_path = Path.home() / 'Downloads'
    destination_root = Path.home() / 'Downloads'
    event_handler = EventHandler(watch_path, destination_root)

    observer = Observer()
    observer.schedule(event_handler, f'{watch_path}', recursive=True)
    print(f'Running observer with watchpath: {watch_path} and destination: {destination_root}\n')
    observer.start()

    try:
        while True:
            sleep(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
