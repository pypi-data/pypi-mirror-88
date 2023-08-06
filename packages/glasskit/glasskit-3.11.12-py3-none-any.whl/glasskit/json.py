from flask.json import JSONEncoder
from datetime import datetime, date
from werkzeug.http import http_date
from bson import ObjectId, Timestamp
from .uorm.models.base_model import BaseModel
from .uorm.db import ObjectsCursor
import simplejson


def default(o):  # pylint: disable=method-hidden
    if isinstance(o, ObjectId):
        return str(o)
    if isinstance(o, Timestamp):
        return o.time
    if isinstance(o, (ObjectsCursor, set)):
        return list(o)
    if isinstance(o, BaseModel):
        return o.to_dict()
    if isinstance(o, datetime):
        return http_date(o.utctimetuple())
    if isinstance(o, date):
        return http_date(o.timetuple())
    raise TypeError(f"{repr(o)} is not JSON serializable")


def dumps(o, default=default, **kwargs):
    return simplejson.dumps(o, default=default, **kwargs)


def loads(text: str, **kwargs):
    return simplejson.loads(text, **kwargs)


class GlasskitJSONEncoder(JSONEncoder):
    def __init__(self, *args, **kwargs):
        kwargs["default"] = default
        super().__init__(*args, **kwargs)

