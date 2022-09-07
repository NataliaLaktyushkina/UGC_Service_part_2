import logging

from fastapi import Request


class RequestIdFilter(logging.Filter):
    def filter(self, record) -> bool:  # type: ignore
        try:
            record.request_id = Request.headers.get('X-Request-Id')
            return True
        except AttributeError:
            return False
