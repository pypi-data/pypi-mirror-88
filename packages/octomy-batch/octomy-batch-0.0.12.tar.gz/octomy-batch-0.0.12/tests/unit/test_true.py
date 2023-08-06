import datetime
import time
import os
import logging
from fk.config import EnvironmentConfig
from fk.batch.BatchProcessor import BatchProcessor

logger = logging.getLogger(__name__)


def test_true():
    logger.info("Dummy unit test")
    return True


def get_mtime(filename):
    return os.path.getmtime(filename)


def set_mtime(filename, t):
    os.utime(filename, (t, t))


def create_dummy_file(filename, content, time=None):
    with open(filename, "w", encoding="utf-8") as file:
        written = file.write(content)
        assert written == len(content)
    if time:
        set_mtime(filename, time)
    actual_time = get_mtime(filename)
    logger.info(f"Created dummy file '{filename}' with content '{content}' and time {time} (actual {actual_time})")
    return actual_time


def test_processor():
    now = datetime.datetime.now().timestamp()
    config = EnvironmentConfig()
    config.apply_config_file("../../config.json", True)
    config.apply_dict({"batch-filter-root":"../fk_batch_filters"})
    config.verify()
    config.attrify()
    logger.info(config)
    bp = BatchProcessor(config)
    bp.verify()
    assert bp
