import sys
import time
import os
import requests
import psutil
import argparse
from dotenv import load_dotenv

load_dotenv()

def send_bark_notification(key, title, body):
    url = f"https://api.day.app/{key}/{title}/{body}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Notification sent successfully. Response: {response.text}")
    except Exception as e:
        print(f"Failed to send notification: {e}")

def monitor_process(pid, bark_key):
    if not psutil.pid_exists(pid):
        print(f"Error: Process with PID {pid} does not exist.")
        return

    print(f"Start monitoring process {pid}...")
    
    try:
        proc = psutil.Process(pid)
        process_name = proc.name()
        print(f"Monitoring process: {process_name} (PID: {pid})")

        while proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE:
            time.sleep(2)
            
    except psutil.NoSuchProcess:
        pass
    except Exception as e:
        print(f"An error occurred while monitoring: {e}")
        return

    print(f"Process {pid} has ended.")
    
    title = "Process Ended"
    body = f"The process {pid} has finished execution."
    send_bark_notification(bark_key, title, body)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor a Linux process and send notification via Bark when it ends.")
    
    # 创建互斥组，要么监控 PID，要么直接发送通知
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("pid", type=int, nargs="?", help="The PID of the process to monitor")
    group.add_argument("--notify-only", action="store_true", help="Send notification immediately without monitoring")

    parser.add_argument("--key", type=str, help="Your Bark API Key (optional if set in .env)", default=os.getenv("BARK_KEY"))
    parser.add_argument("--title", type=str, help="Notification title", default="Process Notification")
    parser.add_argument("--body", type=str, help="Notification body", default="Process event occurred.")
    
    args = parser.parse_args()
    
    if not args.key:
        print("Error: Bark Key not found. Please provide it via --key or set BARK_KEY in .env file.")
        sys.exit(1)
    
    if args.notify_only:
        send_bark_notification(args.key, args.title, args.body)
    elif args.pid:
        monitor_process(args.pid, args.key)
    else:
        parser.print_help()
