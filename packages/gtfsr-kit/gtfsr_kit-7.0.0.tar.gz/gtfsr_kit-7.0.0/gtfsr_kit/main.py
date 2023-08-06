"""
For a definition of General Transit Feed Specification Realtime (GTFSR),
see https://developers.google.com/transit/gtfs-realtime/reference/.
"""
import datetime as dt
import json
from pathlib import Path

import pandas as pd
import numpy as np
from google.protobuf import json_format
from google.transit import gtfs_realtime_pb2
import gtfs_kit as gk


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def read_feed(path, *, from_json=False):
    """
    Given a path (string or Path object) to a GTFSR feed file,
    return the corresponding GTFS feed (FeedMessage instance).
    If ``from_json``, then assume the feed file is in JSON format;
    otherwise, assume the feed file is in Protocol Buffer format.
    """
    path = Path(path)
    feed = gtfs_realtime_pb2.FeedMessage()

    with path.open("rb") as src:
        if from_json:
            feed = json_format.Parse(src.read(), feed)
        else:
            feed.ParseFromString(src.read())

    return feed


def write_feed(feed, path, *, to_json=False):
    """
    Given a GTFSR feed (FeedMessage instance), write it to the given
    file path (string or Path object).
    If ``to_json``, then save the file as JSON;
    otherwise save it as Protocol Buffer.
    """
    path = Path(path)

    if to_json:
        with path.open("w") as tgt:
            tgt.write(json_format.MessageToJson(feed))
    else:
        with path.open("wb") as tgt:
            tgt.write(feed.SerializeToString())


def feed_to_dict(feed):
    """
    Convert the given GTFSR feed (FeedMessage instance) to a dictionary.
    """
    return json.loads(json_format.MessageToJson(feed))


def dict_to_feed(feed_dict):
    """
    Convert the given dictionary to a GTFSR feed (FeedMessage instance).
    """
    return json_format.Parse(json.dumps(feed_dict), gtfs_realtime_pb2.FeedMessage())


def timestamp_to_str(t, datetime_format=DATETIME_FORMAT, *, inverse=False):
    """
    Given a POSIX timestamp (integer) ``t``,
    format it as a datetime string in the given format.
    If ``inverse``, then do the inverse, that is, assume ``t`` is
    a datetime string in the given format and return its corresponding
    timestamp.
    If ``format is None``, then return ``t`` as a string
    (if not ``inverse``) or as an integer (if ``inverse``) directly.
    """
    if not inverse:
        if datetime_format is None:
            result = str(t)
        else:
            result = dt.datetime.fromtimestamp(t).strftime(datetime_format)
    else:
        if format is None:
            result = int(t)
        else:
            result = dt.datetime.strptime(t, datetime_format).timestamp()
    return result


def get_timestamp_str(feed, datetime_format=DATETIME_FORMAT):
    """
    Given a GTFSR feed (FeedMessage instance), return the timestamp
    of the feed as a date string in the given format.
    Note that an empty feed has an (unformatted) timestamp of 0.
    """
    return timestamp_to_str(feed.header.timestamp, datetime_format)


def extract_delays(feed):
    """
    Given a GTFSR feed (FeedMessage instance), extract the delays from
    the feed and return a DataFrame with the columns:

    - route_id
    - trip_id
    - stop_id
    - stop_sequence
    - arrival_delay
    - departure_delay

    If the feed has no trip updates, then return an empty DataFrame.
    """
    rows = []
    for e in feed.entity:
        if not e.HasField("trip_update"):
            continue
        tu = e.trip_update
        rid = tu.trip.route_id
        tid = tu.trip.trip_id
        stu = tu.stop_time_update
        for x in stu:
            stop_sequence = int(x.stop_sequence)
            stop_id = str(x.stop_id)
            delay = {}
            for key in ["arrival", "departure"]:
                if x.HasField(key):
                    delay[key] = getattr(x, key).delay
                else:
                    delay[key] = np.nan
            rows.append(
                (rid, tid, stop_sequence, stop_id, delay["arrival"], delay["departure"])
            )

    f = pd.DataFrame(
        rows,
        columns=[
            "route_id",
            "trip_id",
            "stop_sequence",
            "stop_id",
            "arrival_delay",
            "departure_delay",
        ],
    )
    f = f.sort_values(["route_id", "trip_id", "stop_sequence"])
    f.index = range(f.shape[0])
    return f


def combine_delays(delays_list):
    """
    Given a list of DataFrames of the form output by the function
    :func:`extract_delays`, combine them into a single DataFrame as
    follows and return the result.
    Concatenate ``delays_list`` and remove duplicate
    [route_id, trip_id, stop_sequence]
    entries by combining their non-null delay values into one entry.

    Warning: to ensure sensible output, don't include in ``delays_list``
    the same trips on different days.

    Return an empty DataFrame if ``delays_list`` is empty.
    """
    if not delays_list:
        return pd.DataFrame()

    f = pd.concat(delays_list)
    f = f.drop_duplicates()
    f = f.dropna(subset=["arrival_delay", "departure_delay"], how="all")
    cols = ["route_id", "trip_id", "stop_sequence"]
    f = f.sort_values(cols)
    # Backfill NaNs within each cols group.
    # Do this without groupby(), because that would create
    # too many groups.
    prev_tup = None
    new_rows = []
    dcols = ["arrival_delay", "departure_delay"]
    for __, row in f.iterrows():
        tup = row[cols].values
        if np.array_equal(tup, prev_tup):
            # A duplicate route-trip-stop row.
            # Its arrival delay or departure delay is non-null
            # by virtue of our preprocessing.
            # Use its non-null delays to backfill the previous row's delays
            # if necessary.
            if new_rows[-1][dcols].isnull().any():
                for dcol in dcols:
                    if pd.notnull(row[dcol]) and pd.isnull(new_rows[-1][dcol]):
                        new_rows[-1][dcol] = row[dcol]
        else:
            new_rows.append(row)
            prev_tup = tup
    f = pd.DataFrame(new_rows, index=range(len(new_rows)))
    return f


def build_augmented_stop_times(gtfsr_feeds, gtfs_feed, date):
    """
    Given a list of GTFSR feeds (FeedMessage instances), a GTFS feed
    (GTFSTK Feed instance), and a date (YYYYMMDD string), return
    a DataFrame of GTFS stop times for trips scheduled on the given date
    and containing two extra columns, ``'arrival_delay'`` and
    ``'departure_delay'``, which are delay values in seconds
    for that stop time according to the GTFSR feeds given.

    If no GTFSR feeds are given or if their dates don't alight with
    the given date, then the resulting delay fields will be all NaN.
    """
    # Get scheduled stop times for date
    st = gk.get_stop_times(gtfs_feed, date)

    # Get GTFSR timestamps pertinent to date.
    # Use datetime format YYYYMMDDHHMMSS to be compatible with GTFS dates
    datetime_format = "%Y%m%d%H%M%S"
    start_time = "000000"
    start_datetime = date + start_time
    # Plus 20 minutes fuzz:
    end_time = gk.timestr_to_seconds(st["departure_time"].max()) + 20 * 60
    if end_time >= 24 * 3600:
        end_date = str(int(date) + 1)
    else:
        end_date = date
    end_time = gk.timestr_to_seconds(end_time, inverse=True)
    end_time = gk.timestr_mod24(end_time)
    end_time = end_time.replace(":", "")
    end_datetime = end_date + end_time

    # Extract delays
    delays_frames = [
        extract_delays(f)
        for f in gtfsr_feeds
        if start_datetime <= get_timestamp_str(f, datetime_format) <= end_datetime
    ]

    # Combine delays
    delays = combine_delays(delays_frames)
    if delays.empty:
        # Assign NaNs to delays
        ast = st.assign(arrival_delay=np.nan).assign(departure_delay=np.nan)
    else:
        del delays["route_id"]

        # Merge with stop times
        ast = st.merge(delays, how="left", on=["trip_id", "stop_id", "stop_sequence"])

    return ast.sort_values(["trip_id", "stop_sequence"])


def interpolate_delays(
    augmented_stop_times, dist_threshold, delay_threshold=3600, delay_cols=None
):
    """
    Given an augment stop times DataFrame as output by the function
    :func:`build_augmented_stop_times`, a distance threshold (float)
    in the same units as the ``'shape_dist_traveled'`` column of
    ``augmented_stop_times``, if that column is present, and a delay
    threshold (integer number of seconds), alter the delay values
    of the augmented stop times as follows.

    Drop all delays with absolute value more than ``delay_threshold``
    seconds.
    For each trip and for each delay type (arrival delay or departure
    delay) do the following.
    If the trip has all null values for the delay type,
    then leave the values as is.
    Otherwise:

    - If the first delay is more than ``dist_threshold`` distance units
      from the first stop, then set the first stop delay to zero
      (charitably);
      otherwise set the first stop delay to the first delay.
    - If the last delay is more than ``dist_threshold`` distance units
      from the last stop, then set the last stop delay to zero
      (charitably); otherwise set the last stop delay to the last delay.
    - Linearly interpolate the remaining stop delays by distance.

    Return the resulting DataFrame.

    If a list of delay column names is given in ``delay_cols``,
    then alter those columns instead of the ``arrival_delay`` and
    ``departure_delay`` columns.
    This is useful if the given stop times have extra delay columns.
    """
    f = augmented_stop_times.copy()

    if delay_cols is None or not set(delay_cols) <= set(f.columns):
        delay_cols = ["arrival_delay", "departure_delay"]

    # Return f if nothing to do
    if (
        "shape_dist_traveled" not in f.columns
        or not f["shape_dist_traveled"].notnull().any()
        or all([f[col].count() == f[col].shape[0] for col in delay_cols])
    ):
        return f

    # Nullify fishy delays
    for col in delay_cols:
        f.loc[abs(f[col]) > delay_threshold, col] = np.nan

    # Fill null delays
    def fill(group):
        # Only columns that have at least one nonnull value.
        fill_cols = []
        for col in delay_cols:
            if group[col].count() >= 1:
                fill_cols.append(col)

        for col in fill_cols:
            # Set first and last delays
            for i in [0, -1]:
                j = group[col].dropna().index[i]
                dist_diff = abs(
                    group["shape_dist_traveled"].iat[i]
                    - group["shape_dist_traveled"].loc[j]
                )
                if dist_diff > dist_threshold:
                    group[col].iat[i] = 0
                else:
                    group[col].iat[i] = group[col].loc[j]

            # Interpolate remaining delays
            ind = np.where(group[col].notnull())[0]
            group[col] = np.interp(
                group["shape_dist_traveled"],
                group.iloc[ind]["shape_dist_traveled"],
                group.iloc[ind][col],
            )

        return group

    f = f.groupby("trip_id").apply(fill)

    # Round
    f[delay_cols] = f[delay_cols].round(0)

    return f
