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

"""Human readable approximate time converters."""

import time


def time_ms():
    """Number of milliseconds elapsed since January 1, 1970 00:00:00 UTC."""
    return int(round(time.time() * 1000))


TIME_PERIODS = (
    # period, units, piece
    (0, "", 0),
    (3e3, "~ 1s", 0),
    (7500, "~ 5s", 0),
    (15e3, "~ 10s", 0),
    (25e3, "~ 20s", 0),
    (25e3, "~ 20s", 0),
    (45e3, "~ 30s", 0),
    (75e3, "~ 1min", 0),
    (27e5, "~ %dmin", 6e4),
    (864e5, "~ %dh", 36e5),
    (2592e6, "~ %dd", 864e5),
    # (3942e6, "~ 1month", 0),
    (3154e7, "~ %dmonths", 2628e6),
)


def distance_in_words_to_now(timestamp):
    """Human readable approximate timestamp converter like "~ 1s" '~ 2months'.

    Args:
        timestamp (int): milliseconds unixtime

    Returns:
        str: the distance in words
    """
    current_time = time_ms()
    if not timestamp:
        return ""
    return human_delta_time(current_time - timestamp)


def human_delta_time(delta):
    """Human readable approximate delta time converter like '~ 1s' '~ 2months'.

    Args:
        delta (int): milliseconds time delta between now and then

    Returns:
        str: approximate time
    """
    for period, units, piece in TIME_PERIODS:
        if delta < period:
            return units % round(delta / piece) if piece else units

    return "~ %dY" % round(delta / 3154e7)
