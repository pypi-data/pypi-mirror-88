#!/usr/bin/env python3

# TODO: """DocString if there is one"""

from PyQt5.QtCore import Qt, pyqtProperty
from PyQt5.QtGui import QColor

import epyqlib.widgets.abstractwidget
import epyqlib.mixins
import epyqlib.widgets.scale_ui


# See file COPYING in this source tree
__copyright__ = "Copyright 2016, EPC Power Corp."
__license__ = "GPLv2+"


class Scale(
    epyqlib.widgets.abstractwidget.AbstractWidget, epyqlib.mixins.OverrideRange
):
    def __init__(self, parent=None, in_designer=False):
        self.s_vertically_flipped = False

        # TODO: multiple inheritance *sigh* should get this for me eventually...
        self._min = 0
        self._max = 1

        self._breakpoints = [
            self._min + (self._max - self._min) * n for n in [0.10, 0.25, 0.75, 0.90]
        ]

        dark_red_transparent = QColor(Qt.darkRed)
        dark_red_transparent.setAlpha(0)
        dark_yellow_transparent = QColor(Qt.darkYellow)
        dark_yellow_transparent.setAlpha(0)
        dark_green_transparent = QColor(Qt.darkGreen)
        dark_green_transparent.setAlpha(0)

        self._colors = [
            dark_red_transparent,
            dark_yellow_transparent,
            dark_green_transparent,
            dark_yellow_transparent,
            dark_red_transparent,
        ]

        self._frame = None
        self._signal = None

        super().__init__(
            ui_class=epyqlib.widgets.scale_ui.Ui_Form,
            parent=parent,
            in_designer=in_designer,
        )

        self.update_configuration()

    @pyqtProperty(bool)
    def label_visible(self):
        return epyqlib.widgets.abstractwidget.AbstractWidget.label_visible.fget(self)

    @label_visible.setter
    def label_visible(self, new_visible):
        epyqlib.widgets.abstractwidget.AbstractWidget.label_visible.fset(
            self, new_visible
        )
        self.ui.units.setVisible(self.label_visible)
        self.update_metadata()

    @pyqtProperty(float)
    def lower_red_breakpoint(self):
        return self._breakpoints[0]

    @lower_red_breakpoint.setter
    def lower_red_breakpoint(self, breakpoint):
        self._breakpoints[0] = breakpoint
        self.update_configuration()

    @pyqtProperty(float)
    def lower_yellow_breakpoint(self):
        return self._breakpoints[1]

    @lower_yellow_breakpoint.setter
    def lower_yellow_breakpoint(self, breakpoint):
        self._breakpoints[1] = breakpoint
        self.update_configuration()

    @pyqtProperty(float)
    def upper_yellow_breakpoint(self):
        return self._breakpoints[2]

    @upper_yellow_breakpoint.setter
    def upper_yellow_breakpoint(self, breakpoint):
        self._breakpoints[2] = breakpoint
        self.update_configuration()

    @pyqtProperty(float)
    def upper_red_breakpoint(self):
        return self._breakpoints[3]

    @upper_red_breakpoint.setter
    def upper_red_breakpoint(self, breakpoint):
        self._breakpoints[3] = breakpoint
        self.update_configuration()

    @pyqtProperty(QColor)
    def lower_red_color(self):
        return self._colors[0]

    @lower_red_color.setter
    def lower_red_color(self, color):
        self._colors[0] = color
        self.update_configuration()

    @pyqtProperty(QColor)
    def lower_yellow_color(self):
        return self._colors[1]

    @lower_yellow_color.setter
    def lower_yellow_color(self, color):
        self._colors[1] = color
        self.update_configuration()

    @pyqtProperty(QColor)
    def green_color(self):
        return self._colors[2]

    @green_color.setter
    def green_color(self, color):
        self._colors[2] = color
        self.update_configuration()

    @pyqtProperty(QColor)
    def upper_yellow_color(self):
        return self._colors[3]

    @upper_yellow_color.setter
    def upper_yellow_color(self, color):
        self._colors[3] = color
        self.update_configuration()

    @pyqtProperty(QColor)
    def upper_red_color(self):
        return self._colors[4]

    @upper_red_color.setter
    def upper_red_color(self, color):
        self._colors[4] = color
        self.update_configuration()

    def set_value(self, value):
        self.ui.scale.setValue(value)

    def set_range(self, min=None, max=None):
        if self.override_range:
            min = self.minimum
            max = self.maximum

        self.ui.scale.setRange(min=float(min), max=float(max))

    def set_unit_text(self, units):
        self.ui.units.setText("[{}]".format(units))

    def update_configuration(self):
        try:
            self.ui.scale.setColorRanges(self._colors, self._breakpoints)
        except ValueError as e:
            print(e, file=sys.stderr)

        self.repaint()

    # s_flipped function allows for the qscale to be flipped or not when
    # in vertical orientation
    @pyqtProperty(bool)
    def s_flipped(self):
        return self.s_vertically_flipped

    @s_flipped.setter
    def s_flipped(self, value):
        self.s_vertically_flipped = value
        self.ui.scale.vertically_flipped = value


if __name__ == "__main__":
    import sys

    print("No script functionality here")
    sys.exit(1)  # non-zero is a failure
