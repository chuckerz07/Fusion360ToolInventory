import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

# Set the path to the JSON file and the import script
folder_to_watch = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
json_file_name = "(name of your tool list.json)"  # JSON file to monitor
import_script = os.path.join(folder_to_watch, "import_tool_inventory.py")  # Import script path

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = 0  # Prevent duplicate triggers

    def on_modified(self, event):
        if event.src_path.endswith(json_file_name):
            current_time = time.time()
            if current_time - self.last_modified < 2:  # Avoid rapid triggers
                return
            self.last_modified = current_time

            print(f"{json_file_name} has been modified. Checking readiness...")

            # Confirm the file is ready
            file_path = os.path.join(folder_to_watch, json_file_name)
            for _ in range(5):  # Retry up to 5 times
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    break
                print(f"File {json_file_name} not ready. Retrying...")
                time.sleep(2)
            else:
                print(f"Error: {json_file_name} not ready after retries. Skipping update.")
                return

            print(f"{json_file_name} is ready. Running import_tool_inventory.py...")

            # Run the import script with the file path as an argument
            try:
                result = subprocess.run(
                    ["python", import_script, file_path],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(result.stdout)  # Output of the import script
            except subprocess.CalledProcessError as e:
                print(f"Error running import_tool_inventory.py: {e.stderr}")

if __name__ == "__main__":
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_to_watch, recursive=False)
    
    print(f"Monitoring {folder_to_watch} for changes to {json_file_name}...")
    
    observer.start()
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
