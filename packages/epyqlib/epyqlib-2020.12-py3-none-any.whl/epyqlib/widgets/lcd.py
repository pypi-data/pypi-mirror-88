#!/usr/bin/env python3

# TODO: """DocString if there is one"""

import epyqlib.widgets.abstractwidget
import epyqlib.widgets.lcd_ui


# See file COPYING in this source tree
__copyright__ = "Copyright 2016, EPC Power Corp."
__license__ = "GPLv2+"


class Lcd(epyqlib.widgets.abstractwidget.AbstractWidget):
    def __init__(self, parent=None, in_designer=False):
        super().__init__(
            ui_class=epyqlib.widgets.lcd_ui.Ui_Form,
            parent=parent,
            in_designer=in_designer,
        )

        self._frame = None
        self._signal = None

    def set_value(self, value):
        if self.signal_object is not None:
            if len(self.signal_object.enumeration) > 0:
                value = self.signal_object.full_string
            else:
                value = self.signal_object.format_float()
        elif value is None:
            # TODO: quit hardcoding this and it's better implemented elsewhere
            value = "{0:.2f}".format(0)
        else:
            # TODO: quit hardcoding this and it's better implemented elsewhere
            value = "{0:.2f}".format(value)

        self.ui.lcd.display(value)


if __name__ == "__main__":
    import sys

    print("No script functionality here")
    sys.exit(1)  # non-zero is a failure
