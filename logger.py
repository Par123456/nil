import logging
from datetime import datetime
import os
from colorama import Fore, Style, init

init()

class Logger:
    def __init__(self):
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(
            log_dir,
            f'bot_{datetime.now().strftime("%Y-%m-%d")}.log'
        )
        
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def info(self, message: str, data: dict = None):
        log_msg = f"{message} {data if data else ''}"
        print(f"{Fore.BLUE}{log_msg}{Style.RESET_ALL}")
        logging.info(log_msg)

    def error(self, message: str, error: Exception = None):
        log_msg = f"{message} {str(error) if error else ''}"
        print(f"{Fore.RED}{log_msg}{Style.RESET_ALL}")
        logging.error(log_msg)

    def success(self, message: str, data: dict = None):
        log_msg = f"{message} {data if data else ''}"
        print(f"{Fore.GREEN}{log_msg}{Style.RESET_ALL}")
        logging.info(log_msg)