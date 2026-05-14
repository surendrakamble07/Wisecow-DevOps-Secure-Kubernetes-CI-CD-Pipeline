#!/usr/bin/env python3
import requests
import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app_health.log'),
        logging.StreamHandler()
    ]
)

def check_application_health(url, timeout=10):
    """
    Check if application is UP or DOWN by testing HTTP status codes
    """
    try:
        response = requests.get(url, timeout=timeout)
        
        if 200 <= response.status_code < 300:
            logging.info(f"Application UP - Status: {response.status_code} - URL: {url}")
            return True
        elif 400 <= response.status_code < 500:
            logging.warning(f"Application DOWN - Client Error: {response.status_code} - URL: {url}")
            return False
        elif 500 <= response.status_code < 600:
            logging.error(f"Application DOWN - Server Error: {response.status_code} - URL: {url}")
            return False
        else:
            logging.warning(f"Application UNKNOWN - Status: {response.status_code} - URL: {url}")
            return False
            
    except requests.exceptions.ConnectionError:
        logging.error(f"Application DOWN - Connection Error - URL: {url}")
        return False
    except requests.exceptions.Timeout:
        logging.error(f"Application DOWN - Timeout Error - URL: {url}")
        return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Application DOWN - Request Error: {str(e)} - URL: {url}")
        return False

def main():
    # List of URLs to check (you can modify this list)
    urls_to_check = [
        "http://localhost:4499",  # Wisecow app
        "https://httpbin.org/status/200",  # Test endpoint
        "https://google.com",  # External service
    ]
    
    logging.info("=== Application Health Check Started ===")
    
    all_healthy = True
    for url in urls_to_check:
        if not check_application_health(url):
            all_healthy = False
    
    if all_healthy:
        logging.info("All applications are UP")
    else:
        logging.error("Some applications are DOWN")
        sys.exit(1)
    
    logging.info("=== Application Health Check Completed ===")

if __name__ == "__main__":
    main()
