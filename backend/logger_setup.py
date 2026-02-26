import logging
from zoneinfo import ZoneInfo
from datetime import datetime


timezone = "Asia/Kolkata"
tz_suffix = "IST"

def custom_timezone_converter(*args):
    
    return datetime.now(tz=ZoneInfo(timezone)).timetuple()


logging.Formatter.converter = custom_timezone_converter

def setup_logging():
    # Root logger
    
    app_logger = logging.getLogger('backend') 
    app_logger.setLevel(logging.DEBUG)
    

    app_logger.propagate = False

    # Safety check to prevent duplicate logs if called multiple times
    if not app_logger.handlers:
        file_handler = logging.FileHandler('detailed_log.log')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            fmt='%(asctime)s - %(levelname)-8s - %(module)s.%(funcName)s:%(lineno)d - %(message)s',
            datefmt=f'%Y-%m-%d %H:%M:%S {tz_suffix}'
        )
        file_handler.setFormatter(file_format)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))

        # Adding both to the root
        app_logger.addHandler(file_handler)
        app_logger.addHandler(console_handler)
