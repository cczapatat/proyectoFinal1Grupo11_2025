def format_to_datetime_to_UTC(date_time):
    return date_time.split('.')[0].replace(' ', 'T')