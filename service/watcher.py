import sys
sys.path.append("../")
from globals import collection, UPLOAD_DIR, ARCHIVED_DIR
import time
import pandas
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import shutil
import os
import asyncio

class CSVHandler(FileSystemEventHandler):
    """
    A handler class that processes CSV files when they are created in a monitored directory.
    """

    async def parse_file(self, file_path):
        """
        Parses the given CSV file, cleans the data, and inserts new records into the database.
        
        Args:
            `file_path (str)`: The path to the CSV file to be parsed.
        Returns:
            `None`
        """
        data_frame = pandas.read_csv(file_path)
        data = data_frame.to_dict(orient='records')

        for record in data:
            for key, value in record.items():
                if pandas.isna(value):
                    record[key] = None
            if not record['name'] or not record['event'] or not record['discipline']:
                data.remove(record)

        existing_records = collection.find({'name': {'$in': [record['name'] for record in data]}, 'event': {'$in': [record['event'] for record in data]}, 'discipline': {'$in': [record['discipline'] for record in data]}})
        existing_set = {(record['name'], record['event']) for record in existing_records}

        new_records = [record for record in data if (record['name'], record['event']) not in existing_set]
       
        if new_records:
            collection.insert_many(new_records)
            print(f"Inserted {len(new_records)} new records into the database.")
        else:
            print(f"Skipped insertion of records into the database.")
        
        if not os.path.exists(ARCHIVED_DIR):
            os.makedirs(ARCHIVED_DIR)

        shutil.move(file_path, os.path.join(ARCHIVED_DIR, os.path.basename(file_path)))

    def on_created(self, event):
        """
        Called when a file or directory is created.
        
        Args:
            `event (FileSystemEvent)`: The event object representing the file system event.
        Returns:
            `None`
        """
        if event.src_path.endswith('.csv'):
            print(f"Found new file: {event.src_path}")
            time.sleep(1)
            asyncio.run(self.parse_file(event.src_path))

if __name__ == "__main__":
    observer = Observer()
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    observer.schedule(CSVHandler(), path=UPLOAD_DIR, recursive=False)
    observer.start()
    print("Watching directory...")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()