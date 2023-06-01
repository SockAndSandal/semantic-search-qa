import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from Main import Main
import asyncio
import os
import threading

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print("File %s was just created" % event.src_path)
            main.create(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print("File %s was just modified" % event.src_path)
            main.delete(event.src_path)
            main.create(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print("File %s was just deleted" % event.src_path)
            main.delete(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            print("File %s was just renamed to %s" % (event.src_path, event.dest_path))
            main.delete(event.src_path)
            main.create(event.dest_path)

    def on_access(self, event):
        if not event.is_directory:
            print("File %s was just accessed (atime changed)" % event.src_path)


def checkChanges():

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()
   
    try:
        main.read()
        print("Actively checking...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def checkAccesstime():
    # Get a list of all files in the directory
    

    while True:
        file_list = os.listdir(folder_path)
        all_list = [folder_path+"/"+f for f in file_list]
        try:
            for f in all_list:
                atime_c = datetime.fromtimestamp(os.path.getatime(f)).strftime('%Y-%m-%d %H:%M:%S')
                atime_c = datetime.strptime(atime, '%Y-%m-%d %H:%M:%S').isoformat()
                try:
                    atime = main.getATIME(f,'atime')
                except:
                    continue
                print("ATIME:",atime, "FROM DB:",atime_c)
                if str(atime).replace("'","") != str(atime_c):
                    main.updateATIME(file=f, prop='atime', val=str(atime_c))
        except:
            continue
        time.sleep(20)



if __name__ == "__main__":
    folder_path = "/Users/ram/Desktop/Search-Directory"
    main = Main(folder_path=folder_path)
    
    t1 = threading.Thread(target=checkChanges)
    t2 = threading.Thread(target=checkAccesstime)

    t1.start()
    t2.start()

    # Wait for threads to finish
    t1.join()
    t2.join()
    



    
