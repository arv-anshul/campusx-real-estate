from datetime import datetime


def _json_default(o: object):
    if isinstance(o, datetime):
        return o.isoformat()
