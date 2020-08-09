# Copyright (c) 2020 Maxim Barabash
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time as _time
from datetime import datetime, timedelta, tzinfo

ISO_8601 = "%Y-%m-%dT%H:%M:%S.%f%z"
ZERO = timedelta(0)

STDOFFSET = timedelta(seconds=-_time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds=-_time.altzone)
else:
    DSTOFFSET = STDOFFSET

DSTDIFF = DSTOFFSET - STDOFFSET


class LocalTimezone(tzinfo):
    """A class capturing the platform's idea of local time."""

    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    @staticmethod
    def _isdst(dt):
        time_tuple = (
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            dt.second,
            dt.weekday(),
            0,
            -1,
        )
        stamp = _time.mktime(time_tuple)
        localtime = _time.localtime(stamp)
        return localtime.tm_isdst > 0


Local = LocalTimezone()


def format_date(timestamp, template="%B %dth, %Y"):
    date = datetime.fromtimestamp(timestamp / 1000.0, Local)
    return date.strftime(template)
