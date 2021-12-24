from loguru import logger

from settings import settings


log_file = settings.USERINFO / 'records.log'

logger.add(log_file, rotation='1 MB', retention='1 month', enqueue=True)
