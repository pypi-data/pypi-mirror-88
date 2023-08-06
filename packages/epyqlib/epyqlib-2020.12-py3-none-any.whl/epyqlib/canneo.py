import can
from canmatrix import canmatrix
import copy
import decimal
import epyqlib.utils.general
import functools
import itertools
import locale
import logging
import math
from PyQt5.QtCore import QObject, QTimer, Qt
import re
import struct
import sys
import uuid

import attr
import epyqlib.utils.qt
import epyqlib.utils.units

# See file COPYING in this source tree
__copyright__ = "Copyright 2016, EPC Power Corp."
__license__ = "GPLv2+"


class OutOfRangeError(ValueError):
    pass


class UnableToPackError(Exception):
    pass


class NotFoundError(Exception):
    pass


nothing = object()


def strip_uuid_from_comment(comment):
    match = re.search(r"<uuid:([a-z0-9-]+)>", comment)

    if match is None:
        return comment, None

    uuid_object = uuid.UUID(match[1])

    stripped_comment = comment.replace(match[0], "").strip()

    return stripped_comment, uuid_object


@attr.s
class ReadWrite:
    readable = attr.ib()
    writable = attr.ib()


def strip_rw_from_comment(comment):
    match = re.search(r"<rw:([01]):([01])>", comment)

    if match is None:
        return comment, None

    rw = ReadWrite(
        readable=bool(int(match[1])),
        writable=bool(int(match[2])),
    )

    stripped_comment = comment.replace(match[0], "").strip()

    return stripped_comment, rw


@functools.lru_cache(4096)
def pack_bitstring(length, is_float, value, signed):
    if is_float:
        # TODO: CAMPid 097897541967932453154321546542175421549
        types = {32: ">f", 64: ">d"}

        float_type = types.get(length)

        if float_type is None:
            raise Exception(
                "float type only supports lengths in [{}]".format(
                    ", ".join([str(t) for t in types.keys()])
                )
            )

        (x,) = struct.pack(float_type, value)

        bitstring = "".join("{:08b}".format(b) for b in x)
    else:
        b = value.to_bytes(math.ceil(length / 8), byteorder="big", signed=signed)
        b = "{:0{}b}".format(int.from_bytes(b, byteorder="big"), length)
        bitstring = b[:length]

    return bitstring


@functools.lru_cache(4096)
def unpack_bitstring(length, is_float, is_signed, bits):
    if is_float:
        # TODO: CAMPid 097897541967932453154321546542175421549
        types = {32: ">f", 64: ">d"}

        float_type = types.get(length)

        if float_type is None:
            raise Exception(
                "float type only supports lengths in [{}]".format(
                    ", ".join([str(t) for t in types.keys()])
                )
            )

        (value,) = struct.unpack(
            float_type,
            bytes(int("".join(b), 2) for b in epyqlib.utils.general.grouper(bits, 8)),
        )
    else:
        value = int(bits, 2)

        if is_signed and bits[0] == "1":
            value -= 1 << len(bits)

    return value


@functools.lru_cache(4096)
def bytes_to_bitstrings(data):
    b = tuple("{:08b}".format(b) for b in data)
    little = "".join(reversed(b))
    big = "".join(b)

    return little, big


@functools.lru_cache(4096)
def bitstring_to_signal_list(signals, big, little):
    unpacked = []
    for signal in signals:
        if signal.little_endian:
            least = 64 - signal.start_bit
            most = least - signal.signal_size

            bits = little[most:least]
        else:
            most = signal.start_bit
            least = most + signal.signal_size

            bits = big[most:least]

        unpacked.append(signal.unpack_bitstring(bits))
    return unpacked


@functools.lru_cache(4096)
def signals_to_bytes(length, signals, data):
    little_bits = [None] * (length * 8)
    big_bits = list(little_bits)
    for value, signal in zip(data, signals):
        bits = signal.pack_bitstring(value)

        if signal.little_endian:
            least = 64 - signal.start_bit
            most = least - signal.signal_size

            little_bits[most:least] = bits
        else:
            most = signal.start_bit
            least = most + signal.signal_size

            big_bits[most:least] = bits
    little_bits = reversed(tuple(epyqlib.utils.general.grouper(little_bits, 8)))
    little_bits = tuple(itertools.chain(*little_bits))
    bitstring = "".join(
        next(x for x in (l, b, "0") if x is not None)
        # l if l != ' ' else (b if b != ' ' else '0')
        for l, b in zip(little_bits, big_bits)
    )
    return bytes(
        int("".join(b), 2) for b in epyqlib.utils.general.grouper(bitstring, 8)
    )


class Signal:
    # TODO: but some (progress bar, etc) require an int!
    value_changed = epyqlib.utils.qt.Signal(float)
    value_set = epyqlib.utils.qt.Signal(float)

    def __init__(self, signal, frame, connect=None, parent=None):
        # self.attributes = signal._attributes # {dict} {'GenSigStartValue': '0.0', 'LongName': 'Enable'}
        self.default_value = signal.initial_value
        self.long_name = signal.attributes.get("LongName", None)
        self.hexadecimal_output = signal.attributes.get("HexadecimalOutput", None)
        self.hexadecimal_output = self.hexadecimal_output is not None
        self.little_endian = signal.is_little_endian  # {int} 0
        self.comment = (
            signal.comment
        )  # {str} 'Run command.  When set to a value of \\'Enable\\', causes transition to grid forming or grid following mode depending on whether AC power is detected.  Must be set to \\'Disable\\' to leave POR or FAULTED state.'
        if self.comment is None:
            self.comment = ""
        # TODO: CAMPid 03549854754276996754265427 (repeated <summary> check)
        self.is_summary = "<summary>" in self.comment
        # TODO: maybe not use a string, but used to help with decimal places
        self.factor = signal.factor
        try:
            self.max = signal.max
        except ValueError:
            # TODO: default based on signal range
            self.max = None
        try:
            self.min = signal.min
        except ValueError:
            # TODO: default based on signal range
            self.min = None
        try:
            self.offset = signal.offset
        except ValueError:
            self.offset = 0

        if signal.multiplex == "Multiplexor":
            self.multiplex = True
        else:
            self.multiplex = signal.multiplex  # {NoneType} None

        self.raw_minimum, self.raw_maximum = signal.calculate_raw_range()

        self.name = signal.name  # {str} 'Enable_command'
        # self.receiver = signal.receiver # {str} ''
        self.signal_size = int(signal.size)  # {int} 2
        self.start_bit = int(signal.get_startbit())  # {int} 0
        self.unit = signal.unit  # {str} ''
        self.enumeration = {
            int(k): v for k, v in signal.values.items()
        }  # {dict} {'0': 'Disable', '2': 'Error', '1': 'Enable', '3': 'N/A'}
        self.enumeration_name = signal.enumeration
        self.signed = signal.is_signed
        if self.multiplex is True:
            self.signed = False
        self.float = signal.is_float

        self._format = None

        self.value = None
        self.scaled_value = None

        self.frame = frame
        if self.frame is not None:
            # TODO: put this into the frame!
            self.frame.signals.append(self)

        self.enumeration_format_re = {
            "re": r"^\[(\d+)\]",
            "format": "[{v}] {s}",
            "no_value_format": "{s}",
        }

        # TODO: make this configurable in the .sym?
        self.secret = self.name.casefold() in {"factoryaccess", "password"}

        self.decimal_places = None

        self._format = None

        (
            self.full_string,
            self.short_string,
            self.enumeration_text,
        ) = self.format_strings(value=self.value)
        if connect is not None:
            self.connect(connect)

        if signal.comment is None:
            self.parameter_uuid = None
            self.rw = None
        else:
            self.comment, self.parameter_uuid = strip_uuid_from_comment(
                self.comment,
            )
            self.comment, self.rw = strip_rw_from_comment(
                self.comment,
            )

    def __str__(self):
        return "{name}: sb:{start_bit}, osb:{ordering_start_bit}, len:{length}".format(
            name=self.name,
            start_bit=self.start_bit,
            ordering_start_bit=getattr(self, "ordering_start_bit", "-"),
            length=self.signal_size,
        )

    def last_received(self):
        return self.frame.last_received

    def to_human(self, value):
        return self.offset + (value * self.factor)

    def from_human(self, value):
        return round((value - self.offset) / self.factor)

    def get_human_value(self, for_file=False, column=None, value=nothing):
        if value is nothing:
            value = self.value

        # TODO: handle offset
        if value is None:
            return None

        value = self.to_human(value)

        return self.format_float(value, for_file=for_file)

    def calc_human_value(self, raw_value):
        # TODO: handle offset
        locale.setlocale(locale.LC_ALL, "")

        if isinstance(raw_value, str):
            enumeration_strings = self.enumeration_strings()
            if len(enumeration_strings) > 0:
                try:
                    index = enumeration_strings.index(raw_value)
                except ValueError:
                    enumeration_strings = self.enumeration_strings(include_values=True)
                    if len(enumeration_strings) > 0:
                        try:
                            index = enumeration_strings.index(raw_value)
                        except ValueError:
                            index = int(raw_value)

                value = index
            else:
                value = decimal.Decimal(locale.delocalize(raw_value))
        else:
            value = raw_value

        if value is not None:
            value = self.from_human(value)

        return value

    def check_human_value(self, raw_value, check_range=False):
        value = self.calc_human_value(raw_value)

        return self.check_value(
            value=value,
            check_range=check_range,
        )

    def set_human_value(self, raw_value, force=False, check_range=False):
        value = self.calc_human_value(raw_value)

        self.set_value(
            value=value,
            force=force,
            check_range=check_range,
        )

    def enumeration_string(self, value, include_value=False):
        format = (
            self.enumeration_format_re["format"]
            if include_value
            else self.enumeration_format_re["no_value_format"]
        )

        return format.format(v=value, s=self.enumeration[value])

    def enumeration_strings(self, include_values=False):
        items = list(self.enumeration)
        items.sort()
        items = [
            self.enumeration_string(i, include_value=include_values) for i in items
        ]

        return items

    def get_decimal_places(self):
        if self.decimal_places is None:
            if self.float:
                # TODO: these signals probably ought to have decimal places
                #       specified in the .sym, but that isn't supported yet
                #       anyways.
                self.decimal_places = 3
            else:
                x = self.factor
                # http://stackoverflow.com/a/3019027/228539
                max_digits = 14
                int_part = int(abs(x))
                magnitude = 1 if int_part == 0 else int(math.log10(int_part)) + 1
                if magnitude >= max_digits:
                    return (magnitude, 0)
                frac_part = abs(x) - int_part
                multiplier = 10 ** (max_digits - magnitude)
                frac_digits = multiplier + int(
                    multiplier * frac_part + decimal.Decimal("0.5")
                )
                while frac_digits % 10 == 0:
                    frac_digits /= 10
                scale = int(math.log10(frac_digits))

                self.decimal_places = scale

        return self.decimal_places

    def check_value(self, value, check_range=False, minimum=None, maximum=None):
        if minimum is None:
            minimum = self.min

        if maximum is None:
            maximum = self.max

        if type(value) is float and math.isnan(value):
            return False

        if check_range:
            human_value = self.to_human(value)
            if not minimum <= human_value <= maximum:
                raise OutOfRangeError(
                    "{} not in range [{}, {}]".format(
                        *[self.format_float(f) for f in (human_value, minimum, maximum)]
                    )
                )

        return True

    def set_value(
        self, value, force=False, check_range=False, minimum=None, maximum=None
    ):
        ok = Signal.check_value(
            self=self,
            value=value,
            check_range=check_range,
            minimum=minimum,
            maximum=maximum,
        )
        if not ok:
            return False

        value_parameter = value

        if self.value != value or force:
            self.value = value

            if value not in self.enumeration:
                # TODO: this should be a subclass or something
                if self.hexadecimal_output:
                    pass
                elif self.value is not None:
                    # TODO: CAMPid 9395616283654658598648263423685
                    # TODO: and _offset...

                    self.scaled_value = self.offset + (self.value * self.factor)

                    value = self.scaled_value

            (
                self.full_string,
                self.short_string,
                self.enumeration_text,
            ) = self.format_strings(value=value_parameter)

            if value_parameter is None:
                self.value_changed.emit(float("nan"))
            else:
                self.value_changed.emit(value)

        if value is not None:
            self.value_set.emit(value)

    def format_strings(self, value):
        if value is None or (type(value) is float and math.isnan(value)):
            full_string = "-"
            short_string = "-"
            enumeration_text = None
        else:
            enumeration_text = None

            try:
                # TODO: CAMPid 94562754956589992752348667
                enum_string = self.enumeration[value]
                full_string = self.enumeration_format_re["format"].format(
                    s=enum_string, v=value
                )
                enumeration_text = enum_string
                short_string = enum_string
            except KeyError:
                # TODO: this should be a subclass or something
                if self.hexadecimal_output:
                    format = "{{:0{}X}}".format(
                        math.ceil(self.signal_size / math.log2(16))
                    )
                    full_string = format.format(int(value))
                    short_string = full_string
                else:
                    # TODO: CAMPid 9395616283654658598648263423685
                    # TODO: and _offset...

                    scaled_value = self.offset + (value * self.factor)

                    full_string = self.format_float(scaled_value)
                    short_string = full_string

                    if self.unit is not None:
                        if len(self.unit) > 0:
                            full_string += " [{}]".format(self.unit)

        return full_string, short_string, enumeration_text

    def force_value_changed(self):
        value = self.scaled_value
        if value is None:
            value = 0
        self.value_changed.emit(value)

    def format_float(self, value=None, decimal_places=None, for_file=False):
        if self.secret:
            return "<secret>"

        # TODO: ack fix this since it's getting called with an actual None value...
        if value is None:
            value = self.scaled_value

        if value is None:
            formatted = "-"
        else:
            if decimal_places is None:
                decimal_places = self.get_decimal_places()

            if for_file:
                format = "{{:.{}f}}".format(self.get_decimal_places())
                formatted = format.format(value)
            else:
                format = "%.{}f".format(decimal_places)
                formatted = locale_format(format, value)

        return formatted

    def pack_bitstring(self, value=None):
        if value is None:
            value = self.value
        if value is None:
            value = 0

        try:
            return pack_bitstring(self.signal_size, self.float, value, self.signed)
        except OverflowError as e:
            names = (self.frame.name, self.frame.mux_name, self.name)
            name = ":".join(name for name in names if name is not None)
            raise UnableToPackError(
                "Unable to pack {value} into {name} with range "
                "[{minimum}, {maximum}]".format(
                    value=value,
                    name=name,
                    minimum=self.raw_minimum,
                    maximum=self.raw_maximum,
                )
            ) from e

    def unpack_bitstring(self, bits):
        return unpack_bitstring(self.signal_size, self.float, self.signed, bits)

    def some_packable_value(self):
        return self.unpack_bitstring(bits="0" * self.signal_size)


@functools.lru_cache(10000)
def locale_format(format, value):
    return locale.format_string(format, value, grouping=True)


class QtCanListener(can.Listener):
    message_received_signal = epyqlib.utils.qt.Signal(can.Message)

    def __init__(self, receiver=None, parent=None):
        can.Listener.__init__(self)

        if receiver is not None:
            self.receiver(receiver)

    def receiver(self, slot):
        self.message_received_signal.connect(slot)

    def on_message_received(self, msg):
        # TODO: Be careful since this is no longer being deep copied.
        #       It seems safe based on looking at the socketcan and
        #       pcan bus objects that construct a new Message() for
        #       each one received.  The Notifier loop just forgets
        #       about the message as soon as it is sent here.
        #
        #       This optimization is being justified by the 25% drop
        #       in CPU usage.

        self.message_received_signal.emit(msg)

    def move_to_thread(self, thread):
        signal = type(self).message_received_signal
        signal.qobject_host(self).moveToThread(thread)


class Frame(QtCanListener):
    send = epyqlib.utils.qt.Signal(can.Message, "PyQt_PyObject")

    def __init__(
        self,
        frame,
        multiplex_value=None,
        signal_class=Signal,
        set_value_to_default=True,
        mux_frame=None,
        strip_summary=True,
        parent=None,
    ):
        super().__init__(self.message_received, parent=parent)

        self.mux_frame = mux_frame

        self.id = frame.arbitration_id.id  # {int} 16755521
        # self.SignalGroups = frame.SignalGroups # {list} []
        self.size = frame.size  # {int} 8
        # self.Transmitter = frame.Transmitter # {list} []
        # self.attributes = frame.attributes # {dict} {'GenMsgCycleTime': '200'}
        self.cycle_time = frame.cycle_time if frame.cycle_time != 0 else None
        self.mux_name = frame.attributes.get("mux_name", None)
        self.sendable = frame.attributes.get("Sendable") == "True"
        self.receivable = frame.attributes.get("Receivable") == "True"
        self.comment = (
            frame.comment
        )  # {str} 'Operational commands are received by the module via control bits within this message.'
        if self.comment is None:
            self.comment = ""
        self.extended = bool(frame.arbitration_id.extended)  # {int} 1
        self.name = frame.name  # {str} 'CommandModeControl'
        # self.receiver = frame.receiver # {list} []
        # self.signals = frame.signals # {list} [<canmatrix.canmatrix.Signal object at 0x7fddf8053fd0>, <canmatrix.canmatrix.Signal object at 0x7fddf8054048>, <canmatrix.canmatrix.Signal object at 0x7fddf80543c8>, <canmatrix.canmatrix.Signal object at 0x7fddf8054470>, <canmatrix.canmatrix.Signal object

        self._cyclic_requests = {}
        self._cyclic_period = None
        self.user_send_control = True
        self.block_cyclic = False
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_and_send)

        self.format_str = None
        self.data = None
        self.last_received = None

        self.signals = []
        for signal in frame.signals:
            # TODO: CAMPid 03549854754276996754265427 (repeated <summary> check)
            skipping_summary_signal = (
                strip_summary
                and signal.comment is not None
                and "<summary>" in signal.comment
            )
            if skipping_summary_signal:
                continue

            if multiplex_value is None or str(signal.multiplex) == multiplex_value:
                neo_signal = signal_class(signal=signal, frame=self)

                factor = neo_signal.factor
                if factor is None:
                    factor = 1

                offset = neo_signal.offset
                if offset is None:
                    offset = decimal.Decimal("0")

                default_value = neo_signal.default_value
                if default_value is None:
                    default_value = 0

                if set_value_to_default:
                    neo_signal.set_human_value(offset + (default_value * factor))

        self.signals = tuple(self.signals)

        self.mux_value = None
        if self.mux_name is not None:
            for signal in self.signals:
                if not isinstance(signal.multiplex, bool):
                    self.mux_value = signal.multiplex
                    break

    def _update_and_send(self):
        if not self.block_cyclic:
            self._send(update=True)

    def signal_by_name(self, name):
        try:
            return next(s for s in self.signals if s.name == name)
        except StopIteration:
            return None

    def update_from_signals(self, function=None, data=None, only_return=False):
        if data is None:
            data = self

        data = self.pack(data, function=function)

        if not only_return:
            self.data = data

        return data

    def pack(self, data, function=None):
        if data == self:
            if function is None:
                function = lambda s: s.value
            data = []
            for signal in self.signals:
                try:
                    value = function(signal)
                except:
                    value = 0

                try:
                    value = int(value)
                except (TypeError, ValueError):
                    value = 0
                data.append(value)
            data = tuple(data)

        return signals_to_bytes(self.size, self.signals, data)

    def unpack(self, data, report_error=True, only_return=False):
        rx_length = len(data)
        if rx_length != self.size and report_error:
            print(
                "Received message 0x{self.id:08X} with length {rx_length}, expected {self.size}".format(
                    **locals()
                )
            )
        else:
            little, big = bytes_to_bitstrings(bytes(data))

            unpacked = bitstring_to_signal_list(self.signals, big, little)

            if only_return:
                return dict(zip(self.signals, unpacked))

            for s, v in zip(self.signals, unpacked):
                s.set_value(v)

    def _send(self, update=False):
        if update:
            self.data = self.pack(self)

        self.send.emit(self.to_message(), None)

    def _sent(self):
        pass

    def send_now(self, signals=None):
        self._send(update=True)

    def cyclic_request(self, caller, period):
        if period is None:
            try:
                del self._cyclic_requests[caller]
            except KeyError:
                pass
        else:
            # period will be able to converted to a float, test
            # sooner rather than later for easier debugging
            float(period)
            self._cyclic_requests[caller] = period

        periods = [float(v) for v in self._cyclic_requests.values()]
        new_period = min(periods) if len(periods) > 0 else None

        if new_period is not None:
            if new_period <= 0:
                new_period = None

        if new_period != self._cyclic_period:
            self._cyclic_period = new_period

            if self._cyclic_period is None:
                self.timer.stop()
            else:
                self.timer.setInterval(int(round(float(self._cyclic_period) * 1000)))
                if not self.timer.isActive():
                    self.timer.start()

    def to_message(self, data=None):
        if data is None:
            data = self.data

        return can.Message(
            extended_id=self.extended, arbitration_id=self.id, dlc=self.size, data=data
        )

    def message_received(self, msg):
        unpacked = False

        if msg.arbitration_id == self.id and bool(msg.is_extended_id) == self.extended:
            if self.mux_frame is None:
                self.unpack(msg.data)
                unpacked = True
            elif self.mux_frame is self:
                # print(self, self.name, self.mux_name, self.mux_frame, self.mux_frame.name, self.mux_frame.mux_name)

                unpacked = self.mux_frame.unpack(msg.data, only_return=True)
                (mux_signal,) = unpacked

                # TODO: this if added to avoid exceptions temporarily
                if mux_signal.value in self.multiplex_frames:
                    unpacked = self.multiplex_frames[mux_signal.value].message_received(
                        msg
                    )
            else:
                self.unpack(msg.data)
                unpacked = True

        if unpacked:
            self.last_received = msg.timestamp

        return unpacked

    def terminate(self):
        callers = tuple(r for r in self._cyclic_requests)
        for caller in callers:
            self.cyclic_request(caller, None)

        logging.debug("{} terminated".format(object.__repr__(self)))


@functools.lru_cache(1024)
def frame_by_id(id, frames):
    found = (f for f in frames if f.id == id and f.mux_name is None)

    try:
        (frame,) = found
    except ValueError:
        return None

    return frame


class Neo(QtCanListener):
    def __init__(
        self,
        matrix,
        frame_class=Frame,
        signal_class=Signal,
        rx_interval=0,
        bus=None,
        node_id_adjust=None,
        strip_summary=True,
        parent=None,
    ):
        super().__init__(self.message_received, parent=parent)

        self.bus = None

        self.frame_rx_timestamps = {}
        self.frame_rx_interval = rx_interval

        frames = []

        for frame in matrix.frames:
            if node_id_adjust is not None:
                frame.arbitration_id = canmatrix.canmatrix.ArbitrationId(
                    id=node_id_adjust(
                        message_id=frame.arbitration_id.id,
                        to_device=(
                            frame.attributes["Receivable"].casefold() == "false"
                        ),
                    ),
                    extended=frame.arbitration_id.extended,
                )
            multiplex_signal = None
            for signal in frame.signals:
                if signal.multiplex == "Multiplexor":
                    multiplex_signal = signal
                    break

            if multiplex_signal is None:
                neo_frame = frame_class(
                    frame=frame,
                    strip_summary=strip_summary,
                )
                # for signal in frame.signals:
                #     signal = signal_class(signal=signal, frame=neo_frame)
                #     signal.set_human_value(signal.default_value *
                #                            signal.factor[float])
                frames.append(neo_frame)
            else:
                # Make a frame with just the multiplexor entry for
                # parsing messages later
                multiplex_frame = canmatrix.Frame(
                    name=frame.name,
                    arbitration_id=frame.arbitration_id,
                    size=frame.size,
                    transmitters=list(frame.transmitters),
                    cycle_time=frame.cycle_time,
                )
                matrix_signal = canmatrix.Signal(
                    name=multiplex_signal.name,
                    start_bit=multiplex_signal.start_bit,
                    size=multiplex_signal.size,
                    is_little_endian=multiplex_signal.is_little_endian,
                    is_signed=multiplex_signal.is_signed,
                    factor=multiplex_signal.factor,
                    offset=multiplex_signal.offset,
                    min=multiplex_signal.min,
                    max=multiplex_signal.max,
                    unit=multiplex_signal.unit,
                    multiplex=multiplex_signal.multiplex,
                )
                multiplex_frame.add_signal(matrix_signal)
                multiplex_neo_frame = frame_class(
                    frame=multiplex_frame,
                    strip_summary=strip_summary,
                )
                multiplex_neo_frame.mux_frame = multiplex_neo_frame
                frames.append(multiplex_neo_frame)

                multiplex_neo_frame.multiplex_signal = multiplex_neo_frame.signals[0]

                multiplex_neo_frame.multiplex_frames = {}

                for multiplex_value, multiplex_name in multiplex_signal.values.items():
                    # For each multiplexed frame, make a frame with
                    # just those signals.
                    matrix_frame = canmatrix.Frame(
                        name=frame.name,
                        arbitration_id=frame.arbitration_id,
                        size=frame.size,
                        transmitters=list(frame.transmitters),
                        cycle_time=frame.cycle_time,
                    )
                    matrix_frame.add_attribute("mux_name", multiplex_name)
                    matrix_frame.add_comment(
                        multiplex_signal.comments[int(multiplex_value)]
                    )
                    matrix_signal = canmatrix.Signal(
                        name=multiplex_signal.name,
                        start_bit=multiplex_signal.start_bit,
                        size=multiplex_signal.size,
                        is_little_endian=multiplex_signal.is_little_endian,
                        is_signed=multiplex_signal.is_signed,
                        factor=multiplex_signal.factor,
                        offset=multiplex_signal.offset,
                        min=multiplex_signal.min,
                        max=multiplex_signal.max,
                        unit=multiplex_signal.unit,
                        multiplex=multiplex_signal.multiplex,
                    )
                    # neo_signal = signal_class(signal=matrix_signal, frame=multiplex_neo_frame)
                    matrix_frame.add_signal(matrix_signal)

                    for signal in frame.signals:
                        if signal.multiplex == multiplex_value:
                            matrix_frame.add_signal(signal)

                    neo_frame = frame_class(
                        frame=matrix_frame,
                        mux_frame=multiplex_neo_frame,
                        strip_summary=strip_summary,
                    )
                    for signal in neo_frame.signals:
                        if signal.multiplex is True:
                            signal.set_value(multiplex_value)
                    frames.append(neo_frame)
                    multiplex_neo_frame.multiplex_frames[multiplex_value] = neo_frame

        self.frames = tuple(frames)

        self.signal_from_uuid = {
            signal.parameter_uuid: signal
            for frame in self.frames
            for signal in frame.signals
            if signal.parameter_uuid is not None
        }

        if bus is not None:
            self.set_bus(bus=bus)

    def set_bus(self, bus):
        if self.bus is not None:
            raise Exception("Bus already set")

        self.bus = bus

        for frame in self.frames:
            frame.send.connect(self.bus.send)

    def frame_by_id(self, id):
        return frame_by_id(id, self.frames)

    def frame_by_name(self, name):
        try:
            return next(f for f in self.frames if f.name == name)
        except StopIteration:
            return None

    def signal_by_path(self, *elements):
        i = iter(elements)

        def get_next(i):
            try:
                return next(i)
            except StopIteration as e:
                raise NotFoundError(repr(elements)) from e

        element = get_next(i)

        frame = self.frame_by_name(element)

        if frame is None:
            raise NotFoundError(repr(elements))

        if hasattr(frame, "multiplex_frames"):
            element = get_next(i)

            frames = (
                f for f in frame.multiplex_frames.values() if f.mux_name == element
            )
            try:
                [frame] = frames
            except ValueError:
                raise NotFoundError(repr(elements))

        element = get_next(i)

        signal = frame.signal_by_name(element)
        if signal is None:
            raise NotFoundError(repr(elements))

        return signal

    def get_multiplex(self, message):
        base_frame = self.frame_by_id(message.arbitration_id)

        if not hasattr(base_frame, "multiplex_frames"):
            frame = base_frame
            multiplex_value = None
        else:
            # finish the multiplex thing
            base_frame.unpack(message.data, report_error=False)
            multiplex_value = base_frame.multiplex_signal.value
            try:
                frame = base_frame.multiplex_frames[multiplex_value]
            except KeyError:
                return (base_frame, None)

        return (frame, multiplex_value)

    def message_received(self, msg):
        frame = self.frame_by_id(msg.arbitration_id)
        if frame is not None:
            last = self.frame_rx_timestamps.get(frame, -self.frame_rx_interval)
            if msg.timestamp - last >= self.frame_rx_interval:
                self.frame_rx_timestamps[frame] = msg.timestamp
                frame.message_received_signal.emit(msg)

    def terminate(self):
        for frame in self.frames:
            frame.terminate()

        cached_functions = (
            pack_bitstring,
            unpack_bitstring,
            bytes_to_bitstrings,
            bitstring_to_signal_list,
            signals_to_bytes,
        )

        for f in cached_functions:
            logging.debug(
                "epyqlib.canneo.{}(): {}".format(
                    f.__name__,
                    f.cache_info(),
                )
            )
        logging.debug("{} terminated".format(object.__repr__(self)))


@functools.lru_cache(128)
def format_identifier(identifier, extended):
    f = "0x{{:0{}X}}"

    if extended:
        f = f.format(8)
    else:
        f = f.format(3)

    return f.format(identifier)


@functools.lru_cache(1024)
def format_data(data):
    return " ".join(["{:02X}".format(byte) for byte in data])
