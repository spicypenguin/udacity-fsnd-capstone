from datetime import datetime, timedelta


def years_since_date(start_date):
    if not start_date:
        return None

    now = datetime.utcnow()
    start = datetime.strptime(start_date, '%Y-%m-%d')

    return int((now - start).days / 365.25)


def convert_date_to_dateobj(date_input):
    expected_format = '%Y-%m-%d'
    try:
        return datetime.strptime(date_input, expected_format)
    except:
        return None
