import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(name="contract_analyzer"):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"analyzer_{datetime.now().strftime('%Y%m%d')}.log"
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger
logger = setup_logger()