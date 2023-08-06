import collections
import enum
import logging
import queue
import textwrap
import time

import attr
import twisted.internet.defer
import twisted.protocols.policies

import epyqlib.nv
import epyqlib.utils.general

__copyright__ = "Copyright 2016, EPC Power Corp."
__license__ = "GPLv2+"


logger = logging.getLogger(__name__)


class RequestTimeoutError(epyqlib.utils.general.ExpectedException):
    def __init__(self, state, item):
        message = "Protocol timed out while in state {} handling {}".format(
            state.name, item
        )

        super().__init__(message)
        self.state = state
        self.item = item

    def expected_message(self):
        return textwrap.dedent(
            """\
            Request timed out:
                {}, {}

            1. Confirm converter and adapter are on the same bus
            2. Confirm device file was loaded with node ID matching the converter's
            3. Possible parameter definition mismatch\
            """.format(
                self.state.name, self.item
            )
        )


class ReadOnlyError(Exception):
    pass


class SendFailedError(epyqlib.utils.general.ExpectedException):
    def expected_message(self):
        return "Send failed, make sure you are connected."


class CanceledError(Exception):
    pass


@enum.unique
class State(enum.Enum):
    idle = 0
    reading = 1
    writing = 2


@enum.unique
class Priority(enum.IntEnum):
    user = 0
    background = 1


@attr.s
class Request:
    priority = attr.ib()
    read = attr.ib(cmp=False)
    meta = attr.ib(cmp=False)
    signals = attr.ib(cmp=False)
    deferred = attr.ib(cmp=False)
    passive = attr.ib(cmp=False)
    all_values = attr.ib(cmp=False)
    frame = attr.ib(cmp=False)
    send_time = attr.ib(default=None)


class Protocol(twisted.protocols.policies.TimeoutMixin):
    def __init__(self, timeout=1):
        self._deferred = None

        self._state = State.idle
        self._previous_state = self._state

        self._active = False

        self._request_memory = None
        self._timeout = timeout

        self.requests = queue.PriorityQueue()

        self.cancel_queued = False

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        logger.debug("Entering state {}".format(new_state))
        self._previous_state = self._state
        self._state = new_state

    def makeConnection(self, transport):
        self._transport = transport
        logger.debug("Protocol.makeConnection(): {}".format(transport))

    def _start_transaction(self):
        if self._active:
            raise Exception("Protocol is already active")

        self._active = True

    def _transaction_over(self):
        self.setTimeout(None)
        import twisted.internet

        twisted.internet.reactor.callLater(0, self._transaction_over_after_delay)
        d = self._deferred
        self._deferred = None
        self._request_memory = None
        self.state = State.idle
        return d

    def _transaction_over_after_delay(self):
        self._active = False
        self._get()

    def read(
        self,
        nv_signal,
        meta,
        priority=Priority.background,
        passive=False,
        all_values=False,
    ):
        return self._read_write_request(
            nv_signals=(nv_signal,),
            read=True,
            meta=meta,
            priority=priority,
            passive=passive,
            all_values=all_values,
        )

    def read_multiple(
        self,
        nv_signals,
        meta,
        priority=Priority.background,
        passive=False,
        all_values=False,
    ):
        # TODO: make sure all signals are from the same frame
        return self._read_write_request(
            nv_signals=nv_signals,
            read=True,
            meta=meta,
            priority=priority,
            passive=passive,
            all_values=all_values,
        )

    def write(
        self,
        nv_signal,
        meta,
        priority=Priority.background,
        passive=False,
        ignore_read_only=False,
        all_values=False,
    ):
        # TODO: make sure all signals are from the same frame
        if nv_signal.frame.read_write.min > 0:
            if ignore_read_only:
                return
            else:
                raise ReadOnlyError()

        return self._read_write_request(
            nv_signals=(nv_signal,),
            read=False,
            meta=meta,
            priority=priority,
            passive=passive,
            all_values=all_values,
        )

    def write_multiple(
        self,
        nv_signals,
        meta,
        priority=Priority.background,
        passive=False,
        ignore_read_only=False,
        all_values=False,
    ):
        if tuple(nv_signals)[0].frame.read_write.min > 0:
            if ignore_read_only:
                return
            else:
                raise ReadOnlyError()

        if not isinstance(nv_signals, dict):
            nv_signals = {
                s: (
                    s.value
                    if meta == epyqlib.nv.MetaEnum.value
                    else getattr(s.meta, meta.name).value
                )
                for s in nv_signals
            }

        return self._read_write_request(
            nv_signals=nv_signals,
            read=False,
            meta=meta,
            priority=priority,
            passive=passive,
            all_values=all_values,
        )

    def _read_write_request(
        self, nv_signals, read, meta, priority, passive, all_values
    ):
        deferred = twisted.internet.defer.Deferred()

        if not isinstance(nv_signals, dict):
            nv_signals = {
                s: (
                    s.value
                    if meta == epyqlib.nv.MetaEnum.value
                    else getattr(s.meta, meta.name).value
                )
                for s in nv_signals
            }

        frame = tuple(nv_signals.keys())[0].frame

        self._put(
            Request(
                read=read,
                meta=meta,
                signals=nv_signals,
                deferred=deferred,
                priority=priority,
                passive=passive,
                all_values=all_values,
                frame=frame,
            )
        )

        return deferred

    def _put(self, request):
        self.requests.put(request)
        self._get()

    def _get(self):
        if not self._active:
            while True:
                try:
                    request = self.requests.get(block=False)
                except queue.Empty:
                    self.cancel_queued = False
                else:
                    if self.cancel_queued:
                        request.deferred.errback(CanceledError())
                    elif request.read:
                        self._read_write(request)
                    else:
                        self._read_before_write(request)

                if not self.cancel_queued:
                    break

    def _read_before_write(self, request):
        if isinstance(request.signals, dict):
            nonskip = request.signals
        else:
            nonskip = {
                s: (
                    s.value
                    if request.meta == epyqlib.nv.MetaEnum.value
                    else getattr(s.meta, request.meta.name).value
                )
                for s in request.signals
            }

        skip_signals = set(request.frame.parameter_signals) - set(nonskip.keys())

        if len(skip_signals) == 0:
            try:
                self._read_write(request)
            except Exception as e:
                request.deferred.errback(e)
        else:
            d = twisted.internet.defer.Deferred()
            d.callback(None)

            def read_then_write(args, nonskip=nonskip):
                values, meta = args
                data = {k: v for k, v in nonskip.items()}
                for s, v in values.items():
                    s = s.set_signal
                    if s in request.frame.parameter_signals:
                        if s not in data:
                            data[s] = s.from_human(v)

                return self.write_multiple(
                    nv_signals=data,
                    meta=request.meta,
                    all_values=True,
                )

            def write_response(args, nonskip=nonskip, request=request):
                values, meta = args
                data = {
                    signal.status_signal: values[signal.status_signal]
                    for signal in nonskip
                }

                request.deferred.callback((data, request.meta))

            d.addCallback(
                lambda _: self.read_multiple(
                    request.frame.parameter_signals, meta=request.meta, all_values=True
                )
            )
            d.addCallback(read_then_write)
            d.addCallback(write_response)
            d.addErrback(lambda e: request.deferred.errback(e))

    def _read_write(self, request):
        self._deferred = request.deferred
        try:
            self._start_transaction()
            self.state = State.reading if request.read else State.writing

            (read_write,) = (
                k
                for k, v in request.frame.read_write.enumeration.items()
                if v == ("Read" if request.read else "Write")
            )

            data = collections.OrderedDict()
            for signal in request.frame.signals:
                if signal is request.frame.read_write:
                    data[signal] = read_write
                elif signal.enumeration_name == "Meta":
                    data[signal] = request.meta.value
                elif signal not in request.frame.parameter_signals:
                    data[signal] = signal.value
                elif signal in request.signals and not request.read:
                    data[signal] = request.signals[signal]
                else:
                    data[signal] = None

                if data[signal] is None:
                    v = next(
                        v
                        for v in (
                            signal.from_human(signal.default_value),
                            signal.from_human(signal.min),
                            signal.from_human(signal.max),
                            0,
                        )
                        if v is not None
                    )
                    data[signal] = v

                data[signal] = int(data[signal])

            data = request.frame.update_from_signals(
                data=data.values(),
                only_return=True,
            )

            if request.passive:
                write = self._transport.write_passive
            else:
                write = self._transport.write

            self._request_memory = request

            if not write(request.frame.to_message(data)):
                self.send_failed()
                return

            request.send_time = time.time()

            self.setTimeout(self._timeout)
        except Exception as e:
            self.errback(e)

    def dataReceived(self, msg):

        if not self._active:
            return

        if self._deferred is None:
            return

        request = self._request_memory
        if request is None:
            return

        if not (
            msg.arbitration_id == request.frame.status_frame.id
            and (bool(msg.is_extended_id) == request.frame.status_frame.extended)
        ):
            return

        status_signal = tuple(request.signals)[0].status_signal

        if status_signal is None:
            return

        signals = status_signal.frame.unpack(msg.data, only_return=True)

        mux = status_signal.set_signal.frame.mux.value
        (response_mux_value,) = (
            v for k, v in signals.items() if k.name.endswith("_MUX")
        )
        if response_mux_value != mux:
            return
        meta_mux_value = tuple(
            v for k, v in signals.items() if k.enumeration_name == "Meta"
        )
        if len(meta_mux_value) == 1:
            (meta_mux_value,) = meta_mux_value
            if meta_mux_value != request.meta.value:
                print(" -- skipping due to unmatched meta")
                return

        response_read_write_value = signals[status_signal.frame.command_signal]
        # TODO: handle the enumeration
        if response_read_write_value != request.read:
            return

        self.setTimeout(None)

        if request.all_values:
            status_signals = {s.status_signal for s in request.signals}
            value = {
                s: s.to_human(value=v)
                for s, v in signals.items()
                if s in status_signals
            }
        else:
            raw_value = signals[status_signal]
            value = status_signal.to_human(value=raw_value)

        self.callback(value, request.meta)

    def send_failed(self):
        self.cancel_queued = True
        deferred = self._transaction_over()
        deferred.errback(SendFailedError())

    def timeoutConnection(self):
        request = self._request_memory
        # TODO: report all requested signals
        signal = tuple(request.signals)[0]
        mux_name = signal.frame.mux_name

        e = RequestTimeoutError(
            state=self.state,
            item=(
                f"{mux_name}:{signal.name} "
                f"({request.meta.name}, {request.send_time}, {time.time()}"
            ),
        )

        logger.debug(str(e))
        if self._previous_state in [State.idle]:
            self.state = self._previous_state
        deferred = self._transaction_over()
        deferred.errback(e)

    def callback(self, payload, meta):
        deferred = self._transaction_over()
        logger.debug("calling back for {}".format(deferred))
        deferred.callback((payload, meta))

    def errback(self, payload):
        deferred = self._transaction_over()
        logger.debug("erring back for {}".format(deferred))
        logger.debug("with payload {}".format(payload))
        deferred.errback(payload)

    def cancel(self):
        deferred = self._transaction_over()
        deferred.cancel()
