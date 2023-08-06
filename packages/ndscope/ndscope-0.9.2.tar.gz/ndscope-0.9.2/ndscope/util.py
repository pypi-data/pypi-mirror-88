import collections

from gpstime import gpstime, GPSTimeException

from . import const


def gpstime_parse(time):
    if time is None:
        return None
    try:
        return gpstime.parse(time)
    except GPSTimeException:
        return None
    except ValueError:
        return None


def gpstime_str_gps(gt):
    if gt:
        return str(gt.gps())


def gpstime_str_greg(gt, fmt=const.DATETIME_FMT_OFFLINE):
    if gt is None:
        return
    return gt.astimezone(const.DATETIME_TZ).strftime(fmt)


RTime = collections.namedtuple(
    'RTime',
    ['years', 'days', 'hours', 'minutes', 'seconds', 'msec', 'usec', 'nsec'])


def seconds_time_str(s, prec):
    """format seconds into human-readable time string"""
    if s == 0:
        return '0'
    seconds, subsec = divmod(abs(s), 1)
    seconds = int(seconds)
    nsec = int(subsec * 1e9)
    usec, nsec = divmod(nsec, 1000)
    msec, usec = divmod(usec, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    years, days = divmod(days, 365)
    rt = RTime(years, days, hours, minutes, seconds, msec, usec, nsec)
    fl = [
        '{rt.years}y',
        '{rt.days}d',
        '{rt.hours}h',
        '{rt.minutes}m',
        #'{rt.seconds:.{prec}f}s'
        '{rt.seconds}s',
        '{rt.msec}ms',
        '{rt.usec}us',
        #'{rt.nsec:.{prec}f}ns',
        '{rt.nsec}ns',
    ]
    # this sets the overall scale, e.g. intial time unit
    if years > 0:
        si = 0
    elif days > 0:
        si = 1
    elif hours > 0:
        si = 2
    elif minutes > 0:
        si = 3
    elif seconds > 0:
        si = 4
    elif msec > 0:
        si = 5
    elif usec > 0:
        si = 6
    else:
        si = 7
    # this sets the precision, e.g. final time unit
    if prec >= 7:
        ei = 2
    elif prec >= 4:
        ei = 3
    elif prec >= 2:
        ei = 4
    elif prec >= 0:
        ei = 5
    elif prec >= -3:
        ei = 6
    elif prec >= -6:
        ei = 7
    else:
        ei = 8
    ei = max(ei, si+1)
    if prec > 0:
        prec = 0
    # write the full time string
    fmt = ' '.join(fl[si:ei])
    st = fmt.format(rt=rt, prec=-prec)
    if s < 0:
        st = '-' + st
    return st


def cells_to_tabspec(cells):
    """for a set of occupied cells, return a tabspec dict

    tabspec is keyed by [row, col, rowspan, colspan]

    """
    rows = [x[0] for x in cells]
    cols = [x[1] for x in cells]
    row = min(rows)
    col = min(cols)
    rowspan = len(set(rows))
    colspan = len(set(cols))
    return dict(
        row=row, col=col,
        rowspan=rowspan, colspan=colspan,
    )
