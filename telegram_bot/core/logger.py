import logging
import sys

from telegram_bot.core.config import settings

logging.basicConfig(
    level=getattr(logging, settings.logging.log_level.upper(), logging.INFO),
    format=settings.logging.log_format,
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)
