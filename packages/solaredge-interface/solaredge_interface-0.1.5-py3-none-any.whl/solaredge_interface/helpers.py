
import pytz
import datetime
import dateutil.parser
from dateutil import rrule

from typing import Dict, Iterable
import pandas as pd


def parse_energydetails(d: Dict) -> pd.DataFrame:
    def to_series(_d: Dict) -> Iterable[pd.Series]:
        for meter in _d['energyDetails']['meters']:
            name = meter['type']
            _df = pd.DataFrame.from_dict(meter['values'])
            if _df.empty:
                yield pd.Series(name=name)
                continue
            _df = _df.set_index('date')
            _df.index = pd.DatetimeIndex(_df.index)
            ts = _df.value
            ts.name = name
            ts = ts.dropna()
            yield ts

    all_series = to_series(d)
    df = pd.concat(all_series, axis=1)
    return df


def get_energy_details_dataframe(self, site_id, start_time, end_time, meters=None, time_unit="DAY"):
    """
    Request Energy Details for a certain site and timeframe as a Pandas DataFrame
    Parameters
    ----------
    site_id : int
    start_time : str | dt.date | dt.datetime
        Can be any date or datetime object (also pandas.Timestamp)
        Timezone-naive objects will be treated as local time at the site
    end_time : str | dt.date | dt.datetime
        See `start_time`
    meters : [str]
        default None
        list with any combination of these terms: PRODUCTION, CONSUMPTION, SELFCONSUMPTION, FEEDIN, PURCHASED
    time_unit : str
        default DAY
        options: QUARTER_OF_AN_HOUR, HOUR, DAY, WEEK, MONTH, YEAR
        Note that this method works around the usage restrictions by requesting chunks of data
    Returns
    -------
    pandas.DataFrame
    """
    from .parsers import parse_energydetails
    import pandas as pd

    tz = self.get_timezone(site_id=site_id)
    if meters:
        meters = ','.join(meters)

    # use a generator to do some lazy loading and to (hopefully) save some memory when requesting large periods of time
    def generate_frames():
        # work around the usage restrictions by creating intervals to request data in
        for start, end in self.intervalize(time_unit=time_unit, start=start_time, end=end_time):
            # format start and end in the correct string notation
            start, end = [self._fmt_date(date_obj=time, fmt='%Y-%m-%d %H:%M:%S', tz=tz) for time in [start, end]]
            j = self.get_energy_details(site_id=site_id, start_time=start, end_time=end, meters=meters,
                                        time_unit=time_unit)
            frame = parse_energydetails(j)
            yield frame

    frames = generate_frames()
    df = pd.concat(frames)
    df = df.drop_duplicates()
    df = df.tz_localize(tz)
    return df


def get_timezone(self, site_id):
    """
    Get the timezone of a certain site (eg. 'Europe/Brussels')

    Parameters
    ----------
    site_id : int

    Returns
    -------
    str
    """
    details = self.get_details(site_id=site_id)
    tz = details['details']['location']['timeZone']
    return tz


def _fmt_date(date_obj, fmt, tz=None):
    """
    Convert any input to a valid datestring of format
    If you pass a localized datetime, it is converted to tz first

    Parameters
    ----------
    date_obj : str | dt.date | dt.datetime

    Returns
    -------
    str
    """
    if isinstance(date_obj, str):
        try:
            dt.datetime.strptime(date_obj, fmt)
        except ValueError:
            date_obj = dateutil.parser.parse(date_obj)
        else:
            return date_obj
    if hasattr(date_obj, 'tzinfo') and date_obj.tzinfo is not None:
        if tz is None:
            raise ValueError('Please supply a target timezone')
        _tz = pytz.timezone(tz)
        date_obj = date_obj.astimezone(_tz)

    return date_obj.strftime(fmt)


def intervalize(time_unit, start, end):
    """
    Create pairs of start and end with regular intervals, to deal with usage restrictions on the API
    e.g. requests with `time_unit="DAY"` are limited to 1 year, so when `start` and `end` are more
    than 1 year apart, pairs of timestamps will be generated that respect this limit.

    Parameters
    ----------
    time_unit : str
        options: QUARTER_OF_AN_HOUR, HOUR, DAY, WEEK, MONTH, YEAR
    start : dt.datetime | pd.Timestamp
    end : dt.datetime | pd.Timestamp

    Returns
    -------
    ((pd.Timestamp, pd.Timestamp))
    """
    import pandas as pd

    if time_unit in {"WEEK", "MONTH", "YEAR"}:
        # no restrictions, so just return start and end
        return [(start, end)]
    elif time_unit == "DAY":
        rule = rrule.YEARLY
    elif time_unit in {"QUARTER_OF_AN_HOUR", "HOUR"}:
        rule = rrule.MONTHLY
    else:
        raise ValueError('Unknown interval: {}. Choose from QUARTER_OF_AN_HOUR, HOUR, DAY, WEEK, MONTH, YEAR')

    res = []
    for day in rrule.rrule(rule, dtstart=start, until=end):
        res.append(pd.Timestamp(day))
    res.append(end)
    res = sorted(set(res))
    res = pairwise(res)
    return res


