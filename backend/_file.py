import pathlib
import threading
import os
import json
from datetime import datetime
from csv import DictWriter

class File:
    # root_path = pathlib.Path().resolve()  # get absolution path of current root path
    root_path = r"static\uploads"  # get absolution path of current root path
    global_lock = threading.Lock()

    '''create a directory if not existed
    '''    
    # region[mkdir]
    @staticmethod
    def mkdir(
        dir: str | None = None,             # str : in which directory
        new_folder: str = datetime.now(),   # new folder to be created:
    ):
        # if no specified dir, then get choose current root
        dir = dir if os.path.isabs(dir) else os.path.join(File.root_path,dir)

        # stringfy folder name if given datetime
        new_folder = new_folder if isinstance(
            new_folder, str) else new_folder.strftime("%Y%m%d")

        # creat "\{new_folder}" in  "\log" in the direcotry, if it is not exist
        dir = os.path.join(dir, new_folder)
        if dir and not os.path.exists(dir):
            os.makedirs(dir)
        return dir
    # endregion   


    '''save a dictionary to a file
    '''
    # region[save_dict]
    @staticmethod
    def save_dict(
        dict: dict,                     # dictionary to be saved
        key_str: str | None = None,  # a key string in the file name for easy search
        dt: datetime | None = None,     # datetime of the save
        ext: str = 'json',              # file extension
    ):
        dt = dt if dt else datetime.now()
        key_str = f"_{key_str}" if key_str else ''

        # filename for the saved log
        file_name = f"{dt.strftime('%Y%m%d_%H%M%S%f')[:-3]}{key_str}.{ext}"
        dir = File.mkdir(dir="log", new_folder=dt)
        with open(os.path.join(dir, file_name), 'w') as f:
            json.dump(dict, f, indent=4)
        return file_name
    # endregion   


    '''add dictionary to a csv file
    '''
    # region[csv_add_records]
    @staticmethod
    def csv_add_records(records, file):
        if not isinstance(records,list):
            records = [records]
        with File.global_lock:
            with open(file, "a", newline='') as f_object:
                dictwriter_object = DictWriter(f_object, fieldnames=records[0].keys())
                if not os.stat(file).st_size:
                    dictwriter_object.writeheader()
                dictwriter_object.writerows(records)
    # endregion


