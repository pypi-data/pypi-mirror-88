from Py2Crawl.exceptions import CanNotImportSentry
import logging

try:
    from sentry_sdk.integrations.logging import LoggingIntegration
    import sentry_sdk
except ImportError as e:
    raise CanNotImportSentry


def init_sentry(dsn: str):
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR
    )
    try:
        sentry_sdk.init(
            dsn=dsn,
            integrations=[sentry_logging]
        )
    except Exception as e:
        raise e
