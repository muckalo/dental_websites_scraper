import datetime


def convert_date_str_to_date_obj(date_str, use_format="%Y-%m-%d"):
    return datetime.datetime.strptime(date_str, use_format).date()


def get_current_utc_date_obj():
    return datetime.date.today()


def get_current_utc_datetime_obj():
    return datetime.datetime.today()


def add_days_to_date_obj(date_obj, days):
    return date_obj + datetime.timedelta(days=days)


def add_hours_to_datetime_obj(datetime_obj, hours):
    return datetime_obj + datetime.timedelta(hours=hours)


def get_current_utc_date_or_datetime(only_date=False, use_format='%Y-%m-%d'):
    if only_date:
        return datetime.datetime.utcnow().strftime(use_format)
    else:
        f = "{} %H:%M:%S".format(use_format)
        return datetime.datetime.utcnow().strftime(f)


def get_current_utc_timestamp():
    return datetime.datetime.timestamp(datetime.datetime.utcnow())


def time_for_reset_between_midnight_and_one():
    current_utc_time = datetime.datetime.utcnow().time()
    time_midnight = datetime.time(0, 0)
    time_one_h = datetime.time(1, 0)
    if time_midnight < current_utc_time < time_one_h:
        return True
    return False
