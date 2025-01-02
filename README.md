# Real-Time-File-Sync-with-SFTP
# Features
## Local File Monitoring: 
Monitors a specified local file for changes using the watchdog library.

## Real-Time Sync: 
Upon detecting changes, the script appends new lines from the local file to the remote file.

## SFTP Connection:
Establishes a secure connection to a remote server using paramiko for file transfer.

## Periodic Sync: 
Syncs files every 5 minutes (configurable).
## Error Handling:
Automatically retries in case of connection failures.

## Configuring the Script
SSH Server Details:

## Replace the hostname, port, username, and password with your server's credentials.

## File Paths:

Set local_file_path to the path of the local file you want to monitor.
Set remote_file_path to the path of the remote file you want to sync to.

## Interval:

Adjust the update_interval_seconds to set the sync interval (default: 5 minutes).

## install- pip install paramiko watchdog
