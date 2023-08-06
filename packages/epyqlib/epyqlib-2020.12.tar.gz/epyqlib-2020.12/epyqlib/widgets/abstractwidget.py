#!/usr/bin/env python3

# TODO: """DocString if there is one"""

from collections import OrderedDict

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtProperty, QEvent

import epyqlib.form
import epyqlib.utils.qt


# See file COPYING in this source tree
__copyright__ = "Copyright 2016, EPC Power Corp."
__license__ = "GPLv2+"


factors = OrderedDict(
    [("M", 6), ("k", 3), ("h", 2), ("da", 1), ("d", -1), ("c", -2), ("m", -3), ("", 0)]
)


def conversion_multiplier(old, new):
    old_factor = None
    new_factor = None

    for factor in factors:
        if old_factor is None and old.startswith(factor):
            old_factor = factor
        if new_factor is None and new.startswith(factor):
            new_factor = factor

    old_unit = old[len(old_factor) :]
    new_unit = new[len(new_factor) :]

    if old_unit != new_unit:
        raise Exception("Units do not match: old {}, new {}".format(old, new))

    return 10 ** (factors[old_factor] - factors[new_factor])


event_type_to_name = {
    getattr(QEvent, t): t
    for t in dir(QEvent)
    if isinstance(getattr(QEvent, t), QEvent.Type)
}


def signal_path_to_string(path):
    return ";".join(s.strip() for s in path).rstrip(";")


def string_to_signal_path(s):
    return [se.strip() for se in s.split(";")]


class AbstractWidget(QtWidgets.QWidget):
    trigger_action = pyqtSignal()

    def __init__(self, ui_class=None, parent=None, in_designer=False):
        self.in_designer = in_designer
        super().__init__(parent=parent)

        self.ui = None

        self.left = None
        self.right = None

        self.signal_object = None

        self._label_override = ""
        self._tool_tip_override = ""
        self._override_units = ""

        self._conversion_multiplier = 1
        self._decimal_places = -1

        self._signal_path = [""] * 3
        self._display_units = ""
        self._action = ""

        if ui_class is None:
            self.ui = None
        else:
            self.ui = ui_class()
            self.ui.setupUi(self)

        self.set_signal(force_update=True)

        self.ignore = False

    @pyqtProperty(str)
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        self._action = action

    @pyqtProperty(str)
    def display_units(self):
        return self._display_units

    @display_units.setter
    def display_units(self, units):
        self._display_units = units
        self.update_metadata()

    def changeEvent(self, event):
        QtWidgets.QWidget.changeEvent(self, event)
        if event.type() == QEvent.ParentChange:
            self.update_metadata()

    def update_metadata(self):
        if not self.in_designer:
            return

        from PyQt5.QtDesigner import QDesignerFormWindowInterface

        parent = self

        self.set_signal(force_update=True)

        expected_type = epyqlib.form.EpcForm
        while parent is not None:
            if isinstance(parent, expected_type):
                parent.update_widget(self)
                break
            elif isinstance(parent, QDesignerFormWindowInterface):
                # Probably getting deleted so we can ignore
                break
            else:
                parent = parent.parent()
        else:
            raise Exception(
                "No valid {} widget found while searching parents".format(
                    "epyqlib.form.EpcForm"  # expected_type.__class__.__name__
                )
            )

    def set_signal_path(self, path):
        if len(path) > len(self._signal_path):
            raise Exception(
                "Passed path has length {} which is longer than the supported "
                "limit of {}: {}".format(
                    len(path),
                    len(self._signal_path),
                    path,
                )
            )

        self._signal_path = list(path) + [""] * (len(self._signal_path) - len(path))

    @pyqtProperty("QString")
    def signal_path(self):
        return signal_path_to_string(self._signal_path)

    @signal_path.setter
    def signal_path(self, value):
        self.set_signal_path(string_to_signal_path(value))
        self.update_metadata()

    @pyqtProperty(int)
    def decimal_places(self):
        return self._decimal_places

    @decimal_places.setter
    def decimal_places(self, decimal_places):
        self._decimal_places = decimal_places
        self.update_metadata()

    @pyqtProperty("QString")
    def label_override(self):
        return self._label_override

    @label_override.setter
    def label_override(self, new_label_override):
        expanded = str(new_label_override)
        expanded = expanded.encode("utf8").decode("unicode_escape")
        self._label_override = expanded
        if self.ui is not None:
            self.ui.label.setText(self.label_override)
        self.update_metadata()

    @pyqtProperty("QString")
    def tool_tip_override(self):
        return self._tool_tip_override

    @tool_tip_override.setter
    def tool_tip_override(self, new_tool_tip_override):
        self._tool_tip_override = str(new_tool_tip_override)
        self.update_tool_tip()
        self.update_metadata()

    @pyqtProperty(bool)
    def label_visible(self):
        if self.ui is not None:
            return self.ui.label.isVisibleTo(self.parent())

        return False

    @label_visible.setter
    def label_visible(self, new_visible):
        if self.ui is not None:
            self.ui.label.setVisible(new_visible)
            self.update_metadata()

    @pyqtProperty(bool)
    def units_visible(self):
        if self.ui is not None:
            if hasattr(self.ui, "units"):
                return self.ui.units.isVisibleTo(self.parent())

        return False

    @units_visible.setter
    def units_visible(self, new_visible):
        if self.ui is not None:
            if hasattr(self.ui, "units"):
                self.ui.units.setVisible(new_visible)
                self.update_metadata()

    def containing_layout(self):
        parent = self.parent()

        if parent is None:
            layout = None
        else:
            for layout in parent.findChildren(QtWidgets.QGridLayout):
                index = layout.indexOf(self)
                if index != -1:
                    break
            else:
                layout = None

        if layout == None:
            index = None

        return layout, index

    # TODO: CAMPid 943989817913241236127998452684328
    def set_label(self, new_signal=None):
        if self.ui is not None:
            if len(self.label_override) > 0:
                override = self.label_override
            else:
                override = None

            custom = self.set_label_custom(new_signal=new_signal)

            label_choices = [override, custom]

            if new_signal is not None:
                label_choices.extend([new_signal.long_name, new_signal.name])

            label_choices.append("-")

            label = next(l for l in label_choices if l is not None)

            self.ui.label.setText(label)

            if not self.label_visible:
                layout, index = self.containing_layout()

                # TODO: CAMPid 938914912312674213467977981547743
                if index is not None:
                    row, column, row_span, column_span = layout.getItemPosition(index)
                    # TODO: search in case of colspan
                    left = None
                    for offset in range(1, column + 1):
                        left_column = column - offset
                        left_layout_item = layout.itemAtPosition(row, left_column)

                        if left_layout_item is not None:
                            left_temp = left_layout_item.widget()
                            left_index = layout.indexOf(left_temp)
                            _, _, _, column_span = layout.getItemPosition(left_index)

                            if left_temp is not None:
                                if column_span < offset:
                                    break

                                left = left_temp

                    if isinstance(left, QtWidgets.QLabel):
                        left.setText(label)
                        self.left = left

    def set_label_custom(self, new_signal=None):
        return None

    @pyqtProperty(str)
    def override_units(self):
        return self._override_units

    @override_units.setter
    def override_units(self, units):
        self._override_units = units

        # TODO: CAMPid 0932498324014012080143014320
        if self.signal_object is not None and len(self.override_units) > 0:
            self._conversion_multiplier = conversion_multiplier(
                old=self.signal_object.unit, new=self.override_units
            )

    def set_units(self, units):
        if units is None:
            units = "-"
        if len(self.override_units) > 0:
            units = self.override_units

        self.set_unit_text(units)

        if self.ui is not None:
            if not self.units_visible:
                layout, index = self.containing_layout()

                # TODO: CAMPid 938914912312674213467977981547743
                if index is not None:
                    row, column, row_span, column_span = layout.getItemPosition(index)
                    right = layout.itemAtPosition(row, column + column_span)
                    if right is not None:
                        right = right.widget()
                        if isinstance(right, QtWidgets.QLabel):
                            right.setText(units)
                            self.right = right

    def set_unit_text(self, units):
        if self.ui is not None:
            self.ui.units.setText(units)

    def set_full_string(self, string):
        pass

    def set_range(self, min=None, max=None):
        pass

    def update_connection(self, signal=None):
        if signal is not self.signal_object:
            if self.signal_object is not None:
                self.signal_object.value_changed.disconnect(self.meta_set_value)

            if signal is not None:
                signal.value_changed.connect(self.meta_set_value)

            # TODO: CAMPid 0932498324014012080143014320
            if signal is not None and len(self.override_units) > 0:
                self._conversion_multiplier = conversion_multiplier(
                    old=signal.unit, new=self.override_units
                )
            else:
                self._conversion_multiplier = 1

    def meta_set_value(self, value):
        self.set_value(value)

    def set_signal(self, signal=None, force_update=False):
        if signal is not self.signal_object or force_update:
            self.set_label(new_signal=signal)
            if signal is not None:
                self.set_units(signal.unit)
                self.set_value(None)
            else:
                self.set_units(None)

            self.update_tool_tip(new_signal=signal)

            self.update_connection(signal)
            self.signal_object = signal

            if signal is not None:
                self.set_range(min=signal.min, max=signal.max)

                signal.force_value_changed()

    def update_tool_tip(self, new_signal=None):
        signal = self.signal_object if new_signal is None else new_signal

        if len(self.tool_tip_override) > 0:
            tip = self.tool_tip_override
        elif signal is not None:
            tip = signal.comment
        else:
            tip = ""

        elements = []

        if signal is not None:
            name = signal.long_name
            if name is None:
                name = signal.name
            if name is not None:
                elements.append("Name: {}".format(name))

        elements.append("Description: {}".format(tip))
        if hasattr(self, "_signal_path"):
            elements.append("Path: {}".format(" : ".join(self._signal_path)))
        contents = "<br><br>".join(elements)
        complete = '<div align="left">{}</div>'.format(contents)
        self.setToolTip(complete)
        for widget in [self.left, self.right]:
            if widget is not None:
                widget.setToolTip(complete)


if __name__ == "__main__":
    import sys

    print("No script functionality here")
    sys.exit(1)  # non-zero is a failure
