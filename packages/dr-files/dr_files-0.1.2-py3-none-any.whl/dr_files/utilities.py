import csv
import logging
import math
import os
import struct
import typing

import nptdms
import numpy as np
from scipy.io import wavfile

from dr_files.pb.headers_pb2 import MeasurementHeader

LINE_BUFFER = 1000
MAX_SHORT = 32767.0
ENGINEERING_UNITS_MAP = {
    "custom": 0,
    "V(default)": 1,
    "Pa": 2,
    "g": 3,
    "m/s^2": 4,
    "m/s": 5,
    "m": 6,
    "in/s^2": 7,
    "in/s": 8,
    "in": 9,
    "mil/s": 10,
    "mil": 11,
    "mm/s": 12,
    "mm": 13,
    "micron/s": 14,
    "micron": 15,
    "rad/s^2": 16,
    "rad/s": 17,
    "rad": 18,
    "strain": 19,
    "N": 20,
    "A": 21,
    "RPM": 22,
    "cycle/s^2": 23,
    "Hz": 24,
    "cycle": 25,
    "deg/s^2": 26,
    "deg/s": 27,
    "deg": 28,
}


def dr_to_int_stream(file_path: os.PathLike,) -> (MeasurementHeader, typing.List[int]):
    """
    Reads a Mechbase file found in file_path, returning a tuple with the header and a stream of
    integers.
    """
    with open(file_path, "rb") as fin:
        # Read header
        header: MeasurementHeader = _proto_read(fin, MeasurementHeader)
        return header, list(_read_dr_int_stream(fin))


def dr_to_raw_values(file_path: str,) -> (MeasurementHeader, typing.List[np.array]):
    """
    Reads a Mechbase file found in file_path, returning a tuple with the header and a list of numpy
    arrays with the integer values of the signals.
    """
    header, int_stream = dr_to_int_stream(file_path)

    signals = list(map(lambda _: list(), range(len(header.channels))))
    for index, data_point in enumerate(int_stream):
        signals[index % len(signals)].append(data_point)

    # Convert signal and return
    return header, list(map(np.array, signals))


def dr_to_values(file_path: str) -> (MeasurementHeader, typing.List[np.array]):
    """
    Reads a Mechbase file found in file_path, returning a tuple with the header and a list of numpy
    arrays with the actual measurement values.
    """
    header, raw_signals = dr_to_raw_values(file_path)
    signals = list()
    converters = list(map(value_converter, header.channels))

    for index, s in enumerate(raw_signals):
        signals.append(
            np.array(list(map(converters[index % len(converters)], raw_signals[index])))
        )
    return header, signals


def dr_to_csv(file_path: os.PathLike, out_file_path: os.PathLike):
    """
    Reads a Mechbase file found in file_path, converts it to CSV and writes it at out_file_path.
    """
    header, signals = dr_to_values(file_path)
    h_row = ["Time"]
    for i in range(len(header.channels)):
        h_row.append(f"Channel {i + 1}")
    with open(out_file_path, "w+") as fout:
        w = csv.writer(fout)
        w.writerow(h_row)
        rows = []

        time = 0
        for index, _ in enumerate(signals[0]):
            row = [time]
            time += 1 / header.sample_rate
            for s in signals:
                row.append(s[index])
            rows.append(row)
            if len(rows) > LINE_BUFFER:
                w.writerows(rows)
                rows = []

        w.writerows(rows)


def dr_to_wav(file_path: os.PathLike, out_file_path: os.PathLike):
    """
    Reads a Mechbase file found in file_path, returning a tuple with the header and a numpy array of the signal.
    """
    header, raw_signals = dr_to_raw_values(file_path)
    if len(header.channels) > 1:
        logging.warning(
            f'Converting dr file "{out_file_path}" to wav "{out_file_path}", but dr file has more than a channel'
        )
    wavfile.write(out_file_path, header.sample_rate, np.array(raw_signals[0], np.int16))


def dr_to_tdms(
    file_path: os.PathLike,
    out_file_path: os.PathLike,
    engineering_units_code: str = "",
):
    header, raw_signals = dr_to_raw_values(file_path)
    channels = header.channels

    signals = []
    for index, signal in enumerate(raw_signals):
        multiplier = channels[index].reference / MAX_SHORT
        signals.append(np.array(list(map(lambda v: v * multiplier, signal))))

    root_obj = nptdms.RootObject()
    group_obj = nptdms.GroupObject("MEASUREMENT")
    channel_objs = []
    engineering_unit_label = engineering_units_code
    engineering_units = 0
    if engineering_units_code in ENGINEERING_UNITS_MAP:
        engineering_units = ENGINEERING_UNITS_MAP[engineering_units_code]

    for index, signal in enumerate(signals):
        channel_obj = nptdms.ChannelObject(
            "MEASUREMENT",
            str(index),
            data=signal,
            properties={
                "db_reference": channels[index].db_reference,
                "engineering_unit_label": engineering_unit_label,
                "engineering_units": engineering_units,
                "offset": channels[index].offset,
                "pregain": channels[index].pregain,
                "sensitivity": channels[index].sensitivity,
                "wf_increment": 1.0 / header.sample_rate,
                "wf_samples": len(signal),
            },
        )
        channel_objs.append(channel_obj)
    with nptdms.TdmsWriter(out_file_path) as tdms_file:
        channel_objs.insert(0, group_obj)
        channel_objs.insert(0, root_obj)
        tdms_file.write_segment(channel_objs)


def value_converter(header: MeasurementHeader.ChannelHeader):
    """
    Returns a generator function, which converts a stream of integer values to actual measurement
    values using the given header.
    """
    multiplier = header.reference / MAX_SHORT

    def fun(value):
        offset = header.offset
        if not offset:
            offset = 0.0
        value = (value * multiplier + offset) * 1000.0 / header.sensitivity
        if header.db_reference > 0.0:
            if value == 0:
                value = 0.0000001
            value = 20 * math.log10(abs(value) / header.db_reference)
            if header.pregain > 0.0:
                value += header.pregain
        return value

    return fun


def _read_dr_int_stream(fin):
    """
    Reads a file and converts it to a stream of bytes.
    """
    while True:
        bt = fin.read(2)
        if not bt:
            break

        value = struct.unpack("<h", bt)[0]
        yield value


def _proto_read(stream, clazz):
    bt = stream.read(2)
    proto_size = struct.unpack("<h", bt)[0]
    proto = clazz()
    msg_buf = stream.read(proto_size)
    proto.ParseFromString(msg_buf)
    return proto


def _proto_write(stream, proto):
    bt = proto.SerializeToString()
    stream.write(struct.pack("<h", len(bt)))
    stream.write(bt)
