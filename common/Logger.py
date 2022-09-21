from loguru import logger

logger.add("./log/info.log", format="{time} | {level} | {message}", filter="", level="INFO", rotation="50 MB")
logger.add("./log/debug.log", filter="", level="DEBUG", rotation="10 MB")
logger.add("./log/main.log", filter="__main__", level="DEBUG", rotation="100 MB")
