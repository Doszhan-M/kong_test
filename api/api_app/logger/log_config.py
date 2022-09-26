import logging
from os import getenv
from sys import stderr, stdout
from pygelf import GelfHttpHandler
from colorlog import ColoredFormatter
from logging.handlers import TimedRotatingFileHandler


class CustomLogger:
    color_formatter = ColoredFormatter(
        "%(yellow)s%(asctime)-8s%(reset)s - %(log_color)s%(levelname)-1s%(reset)s - %(cyan)s%(message)s (%(black)s%(filename)s:%(lineno)d)",
        # reset=True,
        datefmt='%H:%M:%S',
        log_colors={
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'light_yellow',
            'ERROR': 'bold_red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    @classmethod
    def color_stream_handler(self):
        stream_handler = logging.StreamHandler(stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(self.color_formatter)
        return stream_handler

    @staticmethod
    def common_file_handler():
        file_handler = TimedRotatingFileHandler(
            filename='logger/logs/common.log', when='MIDNIGHT', backupCount=30,)
        file_handler.setLevel(logging.INFO)
        format = "%(asctime)s - %(levelname)s -%(message)s (%(filename)s:%(lineno)d)"
        formatter = logging.Formatter(format, '%H:%M:%S')
        file_handler.setFormatter(formatter)
        return file_handler

    @staticmethod
    def error_file_handler():
        file_handler = TimedRotatingFileHandler(
            filename='logger/logs/error.log', when='MIDNIGHT', backupCount=2,)
        file_handler.setLevel(logging.ERROR)
        format = "%(asctime)s - %(levelname)s -%(message)s (%(filename)s:%(lineno)d)"
        formatter = logging.Formatter(format, '%H:%M:%S')
        file_handler.setFormatter(formatter)
        return file_handler

    @staticmethod
    def gelf_handler():
        gelf_handler = GelfHttpHandler(
            host=getenv["GRAYLOG_IP"],
            port=getenv["GRAYLOG_PORT"])
        return gelf_handler

    def set_logger(self):
        ''' Переопределить логгеры uvicorn и fastapi 
        '''
        handlers = [
            self.color_stream_handler(),
            self.common_file_handler(),
            self.error_file_handler(), 
        ]
        logging.basicConfig(handlers=handlers, level=logging.INFO)
        for _log in [
            'fastapi',
            'uvicorn.access',
            'uvicorn',
            'uvicorn.error',
        ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = handlers
            _logger.propagate = False
            
        return logging.getLogger('fastapi')
