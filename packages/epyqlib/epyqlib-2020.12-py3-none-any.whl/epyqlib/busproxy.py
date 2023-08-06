#!/usr/bin/env python3

# TODO: get some docstrings in here!

import contextlib
import logging
import sys
import time
import typing

import attr
import can
import can.interfaces.pcan
from epyqlib.canneo import QtCanListener
import epyqlib.utils.qt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

# See file COPYING in this source tree
__copyright__ = "Copyright 2016, EPC Power Corp."
__license__ = "GPLv2+"


@attr.s(auto_attribs=True)
class BusSettings:
    type: str
    channel: str
    bitrate: int

    @classmethod
    def from_bus(cls, real_bus):
        available_bus_types = {
            getattr(sys.modules[module_string], name): id
            for id, [module_string, name] in can.interface.BACKENDS.items()
            if module_string in sys.modules
        }

        for attribute_name in ["channel", "channel_info"]:
            channel = getattr(real_bus, attribute_name, None)
            if channel is not None:
                break
        else:
            raise Exception(f"{real_bus}")

        return cls(
            type=available_bus_types[type(real_bus)], channel=channel, bitrate=500_000
        )

    def create_bus(self):
        real_bus = can.interface.Bus(
            bustype=self.type,
            channel=self.channel,
            bitrate=self.bitrate,
        )

        return real_bus


class BusProxy:
    went_offline = epyqlib.utils.qt.Signal()

    def __init__(
        self, bus=None, timeout=0.1, transmit=True, filters=None, auto_disconnect=True
    ):
        self.filters = filters
        self.auto_disconnect = auto_disconnect

        self.timeout = timeout
        self.notifier = NotifierProxy(self)
        self.real_notifier = None
        self.tx_notifier = NotifierProxy(None)
        self.bus: typing.Optional[BusSettings] = None
        self.bus_settings = None
        self.set_bus(bus)

        self._transmit = transmit

        self.flash_timer = QtCore.QTimer()
        self.flash_timer.setSingleShot(True)
        self.flash_timer.setInterval(10 * 1000)
        self.flash_timer.timeout.connect(self.stop_flashing)

    @contextlib.contextmanager
    def managed_real_bus(self, bustype, channel):
        real_bus = can.interface.Bus(bustype=bustype, channel=channel)
        try:
            self.set_bus(bus=real_bus)
            try:
                yield
            finally:
                self.terminate()
        finally:
            real_bus.shutdown()

    @property
    def transmit(self):
        return self._transmit

    @transmit.setter
    def transmit(self, transmit):
        self._transmit = transmit

    def send(self, msg, on_success=None):
        return self._send(msg, on_success=on_success)

    def send_passive(self, msg, on_success=None):
        return self._send(msg, on_success=on_success, passive=True)

    def _send(self, msg, on_success=None, passive=False):
        if self.bus is not None and (self._transmit or passive):
            # TODO: this (the silly sleep) is really hacky and shouldn't be needed but it seems
            #       to be to keep from forcing socketcan offbus.  the issue
            #       can be recreated with the following snippet.
            # import can
            # import time
            # bus = can.interface.Bus(bustype='socketcan', channel='can0')
            # msg = can.message.Message(arbitration_id=0x00FFAB80, bytearray([0, 0, 0, 0, 0, 0, 0, 0]))
            # for i in range(50):
            #   bus.send(msg)
            #   time.sleep(.0003)
            #
            #       which results in stuff like
            #
            # altendky@tp:/epc/bin$ can0; candump -L -x can0,#FFFFFFFF | grep -E '(0[04]FFAB(88|90|80)|can0 2)'
            # (1469135699.755374) can0 00FFAB80#0000000000000000
            # (1469135699.755462) can0 00FFAB80#0000000000000000
            # (1469135699.755535) can0 00FFAB80#0000000000000000
            # (1469135699.755798) can0 00FFAB80#0000000000000000
            # (1469135699.755958) can0 00FFAB80#0000000000000000
            # (1469135699.756132) can0 00FFAB80#0000000000000000
            # (1469135699.756446) can0 00FFAB80#0000000000000000
            # (1469135699.756589) can0 20000004#000C000000000000
            # (1469135699.756589) can0 20000004#0030000000000000
            # (1469135699.756731) can0 00FFAB80#0000000000000000
            # (1469135699.757004) can0 00FFAB80#0000000000000000
            # (1469135699.757187) can0 00FFAB80#0000000000000000
            # (1469135699.757308) can0 20000040#0000000000000000
            # (1469135699.757460) can0 00FFAB80#0000000000000000
            # (1469135699.757634) can0 00FFAB80#0000000000000000
            # (1469135699.757811) can0 00FFAB80#0000000000000000
            # (1469135699.757980) can0 00FFAB80#0000000000000000
            # (1469135699.758173) can0 00FFAB80#0000000000000000
            # (1469135699.758319) can0 00FFAB80#0000000000000000
            # (1469135699.758392) can0 00FFAB80#0000000000000000
            # (1469135699.758656) can0 00FFAB80#0000000000000000
            # (1469135699.758726) can0 00FFAB80#0000000000000000
            # (1469135699.758894) can0 00FFAB80#0000000000000000

            if isinstance(self.bus, can.BusABC):
                # TODO: this is a hack to allow detection of transmitted
                #       messages later
                msg.timestamp = None

                try:
                    # TODO: I would use message=message (or msg=msg) but:
                    #       https://bitbucket.org/hardbyte/python-can/issues/52/inconsistent-send-signatures
                    self.bus.send(msg)
                except can.CanError:
                    # TODO: specifically implemented for a transmit queue
                    #       full situation to avoid infinite dialogs
                    self.set_bus()

                # TODO: get a real value for sent, but for now python-can
                #       doesn't provide that info.  also, it would be async...
                sent = True

                time.sleep(0.0005)

                if sent:
                    self.tx_notifier.message_received(message=msg)

                    if on_success is not None:
                        on_success()
            else:
                # TODO: I would use message=message (or msg=msg) but:
                #       https://bitbucket.org/hardbyte/python-can/issues/52/inconsistent-send-signatures
                sent = self.bus._send(msg, on_success=on_success, passive=passive)

            if self.auto_disconnect:
                self.verify_bus_ok()

            # TODO: since send() doesn't always report failures this won't either
            #       fix that
            return sent

        return False

    def verify_bus_ok(self):
        if self.bus is None:
            # No bus, nothing to go wrong with it... ?
            ok = True
        else:
            if hasattr(self.bus, "StatusOk"):
                ok = self.bus.StatusOk()

                if not ok:
                    self.set_bus()
            else:
                ok = True
                # TODO: support socketcan
                if hasattr(self.bus, "verify_bus_ok"):
                    ok = self.bus.verify_bus_ok()

        return ok

    def shutdown(self):
        pass

    def flash(self):
        if self.bus is not None:
            result = self.bus.flash(True)
            self.flash_timer.start()
            return result

    def stop_flashing(self):
        if self.bus is not None:
            return self.bus.flash(False)

    def terminate(self):
        self.set_bus()
        logging.debug("{} terminated".format(object.__repr__(self)))

    def set_bus(self, bus=None):
        was_online = self.bus is not None

        if was_online:
            if isinstance(self.bus, can.BusABC):
                self.real_notifier.stop()
                time.sleep(1.1 * self.timeout)
            else:
                self.bus.notifier.remove(self.notifier)
                self.bus.tx_notifier.remove(self.tx_notifier)
            self.bus.shutdown()

        if isinstance(bus, can.BusABC):
            self.bus_settings = BusSettings.from_bus(real_bus=bus)
        elif bus is not None:
            # is being set to a proxy
            self.bus_settings = None

        self.bus = bus

        if self.bus is not None:
            self.set_filters(self.filters)
            if isinstance(self.bus, can.BusABC):
                self.real_notifier = can.Notifier(
                    bus=self.bus, listeners=[self.notifier], timeout=self.timeout
                )
            else:
                self.bus.notifier.add(self.notifier)
                self.bus.tx_notifier.add(self.tx_notifier)
                self.real_notifier = None
        else:
            self.real_notifier = None

        self.reset()

        if was_online and self.bus is None:
            self.went_offline.emit()

        if isinstance(self.bus, can.BusABC):
            self.notifier.move_to_thread(None)
            self.tx_notifier.move_to_thread(None)
        else:
            app = QApplication.instance()
            if app is not None:
                self.notifier.move_to_thread(app.thread())
                self.tx_notifier.move_to_thread(app.thread())

    def reset(self):
        if self.bus is not None:
            if isinstance(self.bus, can.interfaces.pcan.PcanBus):
                self.bus.reset()
                # TODO: do this a better way
                # Give PCAN a chance to actually reset and avoid immediate
                # send failures
                time.sleep(0.500)
            else:
                # TODO: support socketcan
                if hasattr(self.bus, "reset"):
                    self.bus.reset()

    def inner_proxy(self):
        maybe = self
        while True:
            if maybe.bus is None or isinstance(maybe.bus, can.BusABC):
                return maybe

            maybe = maybe.bus

    def reconnect(self):
        inner = self.inner_proxy()

        inner.set_bus()
        inner.set_bus(bus=self.bus_settings.create_bus())

    def set_filters(self, filters):
        self.filters = filters
        real_bus = self.bus
        if real_bus is not None:
            if hasattr(real_bus, "setFilters"):
                real_bus.setFilters(can_filters=filters)


class NotifierProxy(QtCanListener):
    def __init__(self, bus, listeners=[], filtered_ids=None, parent=None):
        super().__init__(receiver=self.message_received, parent=parent)

        # TODO: consider a WeakSet, though this may presently
        #       be keeping objects alive
        self.listeners = set(listeners)
        if filtered_ids is None:
            self.filtered_ids = None
        else:
            self.filtered_ids = set(filtered_ids)

    def message_received(self, message):
        if self.filtered_ids is None or message.arbitration_id in self.filtered_ids:
            for listener in tuple(self.listeners):
                listener.message_received_signal.emit(message)

    def add(self, listener):
        self.listeners.add(listener)

    def discard(self, listener):
        self.listeners.discard(listener)

    def remove(self, listener):
        self.listeners.remove(listener)


if __name__ == "__main__":
    import sys

    print("No script functionality here")
    sys.exit(1)  # non-zero is a failure
