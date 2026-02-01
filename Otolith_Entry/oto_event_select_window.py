from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from ui.oto_event_select import Ui_Select_Event
from Otolith_Entry.otolith_main import OtolithEntryApp
import os
import pyodbc


class OtolithEventDialog(QDialog, Ui_Select_Event):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.select_button.clicked.connect(self.handle_select)
        self.cancel_button.clicked.connect(self.close)
        self.event_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.load_oto_event_data()

    def load_oto_event_data(self):
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(script_dir, "SableSpecimen_DB.accdb")
        connStr = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            r"DBQ=" + db_path + ";")
        conn = pyodbc.connect(connStr)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Event")
        rows = cursor.fetchall()

        self.event_table.setRowCount(len(rows))
        self.event_table.setColumnCount(3)
        self.event_table.setHorizontalHeaderLabels(['Station', 'Haul', 'Haul Date'])

        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.event_table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))

        self.event_table.scrollToBottom()

        conn.close()

    def handle_select(self):
        # Get the selected row
        selected_rows = self.event_table.selectionModel().selectedRows()
        
        if selected_rows:
            row_idx = selected_rows[0].row()
            
            # Get the values from the selected row
            self.selected_station = self.event_table.item(row_idx, 0).text()
            self.selected_haul = self.event_table.item(row_idx, 1).text()

            self.otolith_entry_window = OtolithEntryApp(
                self.selected_station,
                self.selected_haul,
                parent=self)
            self.otolith_entry_window.show()

            self.accept()  # Close dialog with "accepted" status
        else:
            # Optional: show a warning if nothing is selected
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select an event.")
