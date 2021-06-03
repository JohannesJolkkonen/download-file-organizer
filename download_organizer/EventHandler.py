import shutil
from datetime import datetime
from pathlib import Path 

from watchdog.events import FileSystemEventHandler
from download_organizer.extensions import extensions

def rename_file(src, dest):
    """
    Helper function for renaming files in their destination. 
    """
    # Add index to filename if a duplicate name is present
    if Path(dest / src.name).exists():
        index = 0
        while True:
            index += 1
            new_name = dest / f'{src.stem}_{index}{src.suffix}'
            if not Path(dest / new_name).exists():
                return dest / new_name
    else: 
        return dest / src.name

def write_log(child, destination_path):
    shutil.move(child, destination_path)
    log_path = Path.home() / 'Downloads' / 'activity_log.txt'
    with open(log_path, 'r+') as f:
        content = f.read()
        f.seek(0,0)
        line = f'Moved {child.name} to {destination_path} -- Timestamp: {datetime.now()}'
        f.write(line + '\n' + content)


class EventHandler(FileSystemEventHandler):
    def __init__(self, watch_path: Path, destination_root: Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

    ### When changes are made to directory, loop over all files and move them based on file extension.
    def on_modified(self, event):
        for child in self.watch_path.iterdir():
            if child.is_file() and child.suffix.lower() in extensions and child.name != 'activity_log.txt':
                destination_path = self.destination_root / extensions[child.suffix.lower()]
                destination_path = rename_file(src=child, dest=destination_path)
                try:
                    write_log(child, destination_path)
                except Exception as e:
                    print(e)



        