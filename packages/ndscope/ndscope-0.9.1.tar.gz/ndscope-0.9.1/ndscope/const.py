import os
import re
from dateutil.tz import tzutc, tzlocal


# default NDS server
NDSSERVER = 'nds.ligo.caltech.edu:31200'


# date/time formatting for GPS conversion
if os.getenv('DATETIME_TZ') == 'LOCAL':
    DATETIME_TZ = tzlocal()
else:
    DATETIME_TZ = tzutc()
# FIXME: why does '%c' without explicit TZ give very wrong values??
#DATETIME_FMT = '%c'
DATETIME_FMT = '%a %b %d %Y %H:%M:%S %Z'
DATETIME_FMT_OFFLINE = '%Y/%m/%d %H:%M:%S %Z'


# default plot time window
DEFAULT_TIME_WINDOW_ONLINE = (-2, 0)
DEFAULT_TIME_WINDOW_OFFLINE = (-10, 10)


# percentage of full span to add as additional padding when fetching
# new data
DATA_SPAN_PADDING = 0.5


# max viewable seconds for the various trend data
TREND_MAX_SECONDS = {
    'raw': 120,
    'sec': 86400,
    # FIXME: this is too big
    'min': 52560000,
}


# number of lookback bytes available per channel
# 2**22:             4194304
# one week of 16 Hz: 4838400
# 60s of 16k Hz:     7864320
# 2**23:             8388608
DATA_LOOKBACK_LIMIT_BYTES = 2**22


CHANNEL_REGEXP = '^([a-zA-Z0-9-]+:)?[a-zA-Z0-9-_\.]+$'
CHANNEL_RE = re.compile(CHANNEL_REGEXP)
