from loguru import logger
import sys


def setlogger(filepath):
    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<level>{message}</level>"
        ),
        colorize=True,
    )
    logger.add(
        str(filepath),
        level="DEBUG",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        rotation="100 MB",
    )

    # кастомизируем цвета для уровней
    logger.level("WARNING", color="<bold><cyan>")
    logger.level("ERROR", color="<bold><red>")
    logger.level("SUCCESS", color="<bold><green>")
