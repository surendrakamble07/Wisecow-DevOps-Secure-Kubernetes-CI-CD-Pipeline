#!/usr/bin/env python3
import psutil
import logging
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('system_health.log'),
        logging.StreamHandler()
    ]
)

def check_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    if cpu_percent > 80:
        logging.warning(f"High CPU usage detected: {cpu_percent}%")
        return False
    logging.info(f"CPU usage: {cpu_percent}%")
    return True

def check_memory_usage():
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        logging.warning(f"High memory usage detected: {memory.percent}%")
        return False
    logging.info(f"Memory usage: {memory.percent}%")
    return True

def check_disk_usage():
    disk = psutil.disk_usage('/')
    disk_percent = (disk.used / disk.total) * 100
    if disk_percent > 80:
        logging.warning(f"High disk usage detected: {disk_percent:.2f}%")
        return False
    logging.info(f"Disk usage: {disk_percent:.2f}%")
    return True

def check_running_processes():
    process_count = len(psutil.pids())
    if process_count > 300:  # Adjust threshold as needed
        logging.warning(f"High number of running processes: {process_count}")
        return False
    logging.info(f"Running processes: {process_count}")
    return True

def main():
    logging.info("=== System Health Check Started ===")
    
    checks = [
        check_cpu_usage,
        check_memory_usage,
        check_disk_usage,
        check_running_processes
    ]
    
    all_healthy = True
    for check in checks:
        if not check():
            all_healthy = False
    
    if all_healthy:
        logging.info("System health: ALL CHECKS PASSED")
    else:
        logging.error("System health: SOME CHECKS FAILED")
    
    logging.info("=== System Health Check Completed ===")

if __name__ == "__main__":
    main()
