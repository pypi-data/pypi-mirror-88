from _pytest.logging import LogCaptureFixture
from loguru import logger


def test_log_configuration(caplog: LogCaptureFixture) -> None:
    message = "Test message"

    logger.info(message)
    assert message in caplog.text
