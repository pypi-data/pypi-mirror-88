"""
Collection of functions that transform javascript date objects into python
datetime objects and vice versa.
"""


import datetime as dt


JS_EPOCH = dt.datetime(1970, 1, 1)


def todaystr():
    return dt.datetime.now().strftime('%d-%m-%Y')


def now_iso():
    """
    The date-timestamp of the moment now is called in ISO 8601 format.
    """
    return dt.datetime.now().isoformat().split('.')[0] + 'Z'


def round_js_to_date(js_datetime):
    date_time = js_to_datetime(js_datetime)
    round_datetime = dt.datetime.combine(date_time.date(),
                                         dt.datetime.min.time())
    return datetime_to_js(round_datetime)


def datetime_to_js(date_time):
    if date_time is not None:
        return int((date_time - JS_EPOCH).total_seconds() * 1000)


def js_to_datetime(date_time):
    if date_time is not None:
        return JS_EPOCH + dt.timedelta(seconds=date_time/1000)


def js_to_datestring(js_date, iso=False):
    date_time = js_to_datetime(js_date)
    return datetime_to_datestring(date_time, iso)


def datetime_to_datestring(date_time, iso=False):
    if iso:
        return date_time.strftime('%Y-%m-%d')
    else:
        return date_time.strftime('%d-%m-%Y')


def datestring_to_js(date_string, iso=False):
    if iso:
        date_time = dt.datetime.strptime(date_string, '%Y-%m-%d')
    else:
        date_time = dt.datetime.strptime(date_string, '%d-%m-%Y')
    return datetime_to_js(date_time)
