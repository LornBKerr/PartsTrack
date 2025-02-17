"""
Base class for the Parts System dialogs.

File:       base_dialog.py
Author:     Lorn B Kerr
Copyright:  (c) 2020 - 2023 Lorn B Kerr
License:    MIT, see file License
Version:    1.0.0
"""

from lbk_library import DataFile as PartsFile
from lbk_library.gui import Dialog
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView, QMainWindow, QTableWidget, QTableWidgetItem

from elements import Order, OrderLineSet

file_version = "1.0.0"
changes = {
    "1.0.0": "Initial release",
    "1.0.1": "Revised Dialog import from lbk_library to lbk_library.gui",
}


class BaseDialog(Dialog):
    """
    Base class for the Parts System dialogs.

    Holds common functions used by all the editing dialogs in the parts
    parts file program.
    """

    PART_ORDER_COL_NAMES = [
        "Order",
        "Date",
        "Source",
        "Line",
        "Part Number",
        "Cost Each",
        "Quantity",
        "Remarks",
    ]
    """ Names of the Order Table columns for the Item and Part dialogs."""

    PART_ORDER_COL_WIDTHS = [60, 100, 60, 40, 120, 70, 100, 1]
    """ Widths of the Order Table columns for the Item and Part dialogs."""

    def __init__(
        self, parent: QMainWindow, parts_file: PartsFile, operation: int
    ) -> None:
        """
        Initialize the DialogBase.

        Parameters:
            parent(QMainWindow):  the parent window owning this dialog.
            parts_file (PartsFile): reference to the parts file for this item.
        """
        super().__init__(parent, parts_file, operation)
        self.form = None

    def get_parts_file(self) -> PartsFile:
        """Alias for Dialog.get_datafile() function for consistent naming."""
        return self.get_datafile()

    def set_table_header(
        self,
        table: QTableWidget,
        col_names: list[str],
        col_widths: list[int],
        stretch_column: int = None,
    ) -> None:
        """
        Set the header column names for a QTable.

        Parameters:
            table (QTableWidget): The QTableWidget to set the headers.
            col_names (lits[str]): the names of the columns
            col_widths (list[int]): the column widths
            stretch_column (int): the column number to stretch to fill
                the remaining table width.
        """
        table.setColumnCount(len(col_names))
        table.setHorizontalHeaderLabels(col_names)
        for i in range(0, len(col_widths)):
            table.setColumnWidth(i, col_widths[i])
        if stretch_column is not None:
            table.horizontalHeader().setSectionResizeMode(
                stretch_column, QHeaderView.ResizeMode.Stretch
            )

    def save_buttons_enable(self, enable: bool) -> None:
        """
        Enable/Disable the save buttons.

        Parameters:
            enable (Boolean) True if the buttons should be enabled,
                False is not
        """
        self.form.save_new_button.setEnabled(enable)
        self.form.save_done_button.setEnabled(enable)

    def fill_order_table_fields(self, part_number: str) -> None:
        """
        Fill the order listing with the order lines for the current part.

        Parameters:
            part_number (String) The current part part number.
        """
        order_lines = OrderLineSet(
            self.get_parts_file(), "part_number", part_number, "order_number"
        )
        if not part_number:
            order_lines.set_property_set([])
        table = self.form.order_table
        table.setRowCount(order_lines.get_number_elements())
        row = 0
        for order_line in order_lines:
            order = Order(self.get_parts_file(), order_line.get_order_number())
            entry = QTableWidgetItem(order_line.get_order_number())
            entry.setTextAlignment(
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
            )
            table.setItem(row, 0, entry)

            entry = QTableWidgetItem(order.get_date())
            entry.setTextAlignment(
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
            )
            table.setItem(row, 1, entry)

            table.setItem(row, 2, QTableWidgetItem(order.get_source()))
            entry = QTableWidgetItem(str(order_line.get_line()))
            entry.setTextAlignment(
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
            )
            table.setItem(row, 3, entry)

            entry = QTableWidgetItem(order_line.get_part_number())
            table.setItem(row, 4, entry)

            entry = QTableWidgetItem(format(float(order_line.get_cost_each()), ".2f"))
            entry.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            table.setItem(row, 5, entry)
            entry = QTableWidgetItem(str(order_line.get_quantity()))
            entry.setTextAlignment(
                Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
            )
            table.setItem(row, 6, entry)

            table.setItem(row, 7, QTableWidgetItem(order_line.get_remarks()))
            row += 1
