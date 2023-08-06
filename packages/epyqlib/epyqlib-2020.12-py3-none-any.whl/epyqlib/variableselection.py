import pathlib

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSortFilterProxyModel, Qt
import twisted.internet.threads

import epyqlib.cmemoryparser
import epyqlib.datalogger
import epyqlib.utils.qt
import epyqlib.utils.twisted
import epyqlib.variableselection_ui


# See file COPYING in this source tree
__copyright__ = "Copyright 2017, EPC Power Corp."
__license__ = "GPLv2+"


class VariableSelection(QtWidgets.QWidget):
    def __init__(self, parent=None, in_designer=False):
        super().__init__(parent=parent)

        self.in_designer = in_designer

        self.ui = epyqlib.variableselection_ui.Ui_Form()
        self.ui.setupUi(self)

        self.ui.load_binary_button.clicked.connect(self.load_binary)
        self.ui.save_selection_button.clicked.connect(self.save_selection)
        self.ui.load_selection_button.clicked.connect(self.load_selection)
        self.ui.update_parameters_button.clicked.connect(self.update_parameters)
        self.ui.process_raw_log_button.clicked.connect(self.process_raw_log)
        self.ui.process_raw_log_button.setEnabled(False)

        self.ui.view.ui.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.view.ui.tree_view.customContextMenuRequested.connect(self.context_menu)

        self.progress = None

    def set_signal_paths(
        self,
        reset_signal_path,
        recording_signal_path,
        configuration_is_valid_signal_path,
    ):
        self.ui.reset_button.set_signal_path(reset_signal_path)
        self.ui.logging_led.set_signal_path(recording_signal_path)
        self.ui.configuration_is_valid_led.set_signal_path(
            configuration_is_valid_signal_path
        )

    def set_model(self, model):
        self.ui.view.set_model(model)

    def set_sorting_enabled(self, enabled):
        self.ui.view.set_sorting_enabled(enabled)

    def sort_by_column(self, column, order):
        self.ui.view.sort_by_column(column=column, order=order)

    def save_selection(self):
        filters = [("EPC Variable Selection", ["epv"]), ("All Files", ["*"])]
        filename = epyqlib.utils.qt.file_dialog(filters, save=True, parent=self)

        if filename is not None:
            model = self.nonproxy_model()
            model.save_selection(filename=filename)

    def load_selection(self):
        filters = [("EPC Variable Selection", ["epv"]), ("All Files", ["*"])]
        filename = epyqlib.utils.qt.file_dialog(filters, parent=self)

        if filename is not None:
            model = self.nonproxy_model()
            model.load_selection(filename=filename)

    # TODO: CAMPid 07943342700734207878034207087
    def nonproxy_model(self):
        model = self.ui.view.model
        while isinstance(model, QSortFilterProxyModel):
            model = model.sourceModel()

        return model

    def load_binary(self):
        filters = [("TICOFF Binaries", ["out"]), ("All Files", ["*"])]
        filename = epyqlib.utils.qt.file_dialog(filters, parent=self)

        if filename is not None:
            # TODO: CAMPid 9632763567954321696542754261546
            self.progress = epyqlib.utils.qt.progress_dialog(parent=self)
            self.progress.setLabelText("Loading binary...")

            model = self.nonproxy_model()

            self.progress.show()

            d = twisted.internet.threads.deferToThread(
                epyqlib.cmemoryparser.process_file, filename=filename
            )
            d.addCallback(model.update_from_loaded_binary)
            d.addCallback(
                epyqlib.utils.twisted.detour_result,
                self.ui.process_raw_log_button.setEnabled,
                True,
            )
            d.addBoth(epyqlib.utils.twisted.detour_result, self.progress_cleanup)
            d.addErrback(epyqlib.utils.twisted.errbackhook)

    def progress_cleanup(self):
        self.progress.close()
        self.progress.deleteLater()
        self.progress = None

    def update_parameters(self):
        model = self.nonproxy_model()
        model.update_parameters(parent=self)

    def process_raw_log(self):
        filters = [("Raw", ["raw"]), ("All Files", ["*"])]
        raw_filename = epyqlib.utils.qt.file_dialog(filters, parent=self)

        if raw_filename is not None:
            filters = [("CSV", ["csv"]), ("All Files", ["*"])]
            csv_guess = str(
                pathlib.Path(raw_filename).with_suffix("." + filters[0][1][0])
            )
            csv_filename = epyqlib.utils.qt.file_dialog(
                filters, save=True, parent=self, dir=csv_guess
            )

            if csv_filename is not None:
                with open(raw_filename, "rb") as f:
                    data = f.read()

                model = self.nonproxy_model()

                self.progress = epyqlib.utils.qt.progress_dialog(parent=self)
                self.progress.setLabelText("Processing Raw Log...")

                self.progress.show()

                d = model.parse_log(data=data, csv_path=csv_filename)
                d.addBoth(epyqlib.utils.twisted.detour_result, self.progress_cleanup)
                d.addErrback(epyqlib.utils.twisted.errbackhook)

    def context_menu(self, position):
        index = self.ui.view.ui.tree_view.indexAt(position)
        index = self.ui.view.ui.tree_view.model().mapToSource(index)

        if not index.isValid():
            return

        node = self.nonproxy_model().node_from_index(index)

        menu = QtWidgets.QMenu()
        read_action = menu.addAction("Read")

        action = menu.exec(self.ui.view.ui.tree_view.viewport().mapToGlobal(position))

        if action is None:
            pass
        elif action is read_action:
            self.nonproxy_model().read(variable=node)
