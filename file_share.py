import time
import paramiko
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, local_file, remote_file, sftp_client):
        self.local_file = local_file
        self.remote_file = remote_file
        self.sftp_client = sftp_client
        self.last_line_number = 0

    def on_modified(self, event):
        if event.src_path.endswith(self.local_file):
            print(f"Local file {self.local_file} modified. Appending new entries to remote file...")
            with open(self.local_file, 'r') as local_file_obj:
                lines = local_file_obj.readlines()
                new_lines = lines[self.last_line_number:]
                
                with self.sftp_client.file(self.remote_file, 'a') as remote_file_obj:
                    for line in new_lines:
                        remote_file_obj.write(line)

                self.last_line_number = len(lines)
                
            print("New entries appended to remote file.")

def monitor_and_update(local_file, remote_file, hostname, port, username, password, interval_seconds):
    while True:
        try:
            with paramiko.Transport((hostname, port)) as transport:
                transport.connect(username=username, password=password)
                with paramiko.SFTPClient.from_transport(transport) as sftp:
                    with open(local_file, 'r') as local_file_obj:
                        local_content = local_file_obj.read()
                        with sftp.file(remote_file, 'w') as remote_file_obj:
                            remote_file_obj.write(local_content)
                    print("Initial file transfer completed.")

                    event_handler = FileChangeHandler(local_file, remote_file, sftp)
                    observer = Observer()
                    observer.schedule(event_handler, path='.', recursive=False)
                    observer.start()

                    try:
                        while True:
                            time.sleep(interval_seconds)
                    except KeyboardInterrupt:
                        observer.stop()

                    observer.join()

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

# Replace these values with your SSH server details and file paths
hostname = "182.79.97.204"
port = 22
username = "wlg"
password = "wlg@1234"
local_file_path = "/home/wlg/Record.csv"
remote_file_path = "/home/wlg/Downloads/Record.csv"
update_interval_seconds = 300  # 5 minutes

# Call the function to monitor and update the remote file in real-time
monitor_and_update(local_file_path, remote_file_path, hostname, port, username, password, update_interval_seconds)

