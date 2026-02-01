#import necessary packages/functions
import os
import pyodbc
from PyQt5 import QtWidgets
from ui.event_select import Ui_enter_event 
from ui.new_event import Ui_NewEventWindow

#creates the "Event Select App" Class from the Ui_enter_event class
class EventSelectApp(QtWidgets.QMainWindow, Ui_enter_event):
    #creates instances of EventSelectApp Class.  Initializes it, offers opportunity to add info into instance
    def __init__(self):
        #super to inherit class info from Ui_enter_event)
        super().__init__()
        #sets up the Ui_enter_event ui
        self.setupUi(self)
        #when new_event button clicked, load create_new_event
        self.new_event.clicked.connect(self.create_new_event)
        #when return_menu button clicked, load return_to_menu
        self.return_menu.clicked.connect(self.return_to_menu)
        #when selecting a row from the event table 
        self.event_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.load_event_data()  # Call your data loading method
        self.edit_event.clicked.connect(self.on_edit_event)
    
    def on_edit_event(self):
        if(self.event_table.currentRow() < 0):
            QtWidgets.QMessageBox.warning(self, "Error","Please select an event to edit.")
            return
        
        selected_row = self.event_table.currentRow()
        station_select = self.event_table.item(selected_row,0).text()
        haul_select = self.event_table.item(selected_row,1).text()
        haul_date_select = self.event_table.item(selected_row,2).text()

        self.edit_event_window = QtWidgets.QMainWindow()
        ui = Ui_NewEventWindow()
        ui.setupUi(self.edit_event_window)
        ui.station.setText(station_select)
        ui.haul.setText(haul_select)
        ui.date.setText(haul_date_select)
        ui.add_event.setText("Save Changes")
        ui.add_event.clicked.connect(lambda: self.save_edited_event(ui, station_select, haul_select, haul_date_select))
        ui.return_to_event_select.clicked.connect(self.edit_event_window.close)
        self.edit_event_window.show()
        
    def save_edited_event(self, ui, old_station, old_haul, old_haul_date):
        new_station = ui.station.toPlainText().strip()
        new_haul = ui.haul.toPlainText().strip()
        new_haul_date = ui.date.toPlainText().strip()

        if not new_station or not new_haul or not new_haul_date:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        # Database connection
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(script_dir, "SableSpecimen_DB.accdb")
        connStr = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            r"DBQ=" + db_path + ";")
        try:
            conn = pyodbc.connect(connStr)
            cursor = conn.cursor()

            # Update the Event table (adjust column names if needed)
            cursor.execute("UPDATE Event SET Station=?, Haul=?, Haul_Date=? WHERE Station=? AND Haul=? AND Haul_Date=?", (new_station, new_haul, new_haul_date, old_station, old_haul, old_haul_date))
            conn.commit()

            # Reload the event data
            self.load_event_data()

            # Close the edit window
            self.edit_event_window.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error updating event: {e}")
        finally:
            conn.close()


    def load_event_data(self):
        # Database connection and query
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(script_dir, "SableSpecimen_DB.accdb")
        connStr = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=" + db_path + ";")
        conn = pyodbc.connect(connStr)
        cursor = conn.cursor()
        
        # Query the event_table (adjust table name and columns as needed)
        cursor.execute("SELECT * FROM Event")  # Example query
        rows = cursor.fetchall()
        
        # Populate the table
        self.event_table.setRowCount(len(rows))
        self.event_table.setColumnCount(3)  # Adjust based on your columns
        self.event_table.setHorizontalHeaderLabels(['Station', 'Haul', 'Haul Date'])  # Column headers
        
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.event_table.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(value)))
        
        conn.close()

    def create_new_event(self):
        self.new_event_window = QtWidgets.QMainWindow()
        ui = Ui_NewEventWindow()
        ui.setupUi(self.new_event_window)
        
        # Connect the Add Event button
        ui.add_event.clicked.connect(lambda: self.save_new_event(ui))
        
        # Connect the return button
        ui.return_to_event_select.clicked.connect(self.new_event_window.close)
        
        self.new_event_window.show()

    def save_new_event(self, ui):
        station = ui.station.toPlainText().strip()
        haul = ui.haul.toPlainText().strip()
        haul_date = ui.date.toPlainText().strip()
        
        if not station or not haul or not haul_date:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return
        
        # Database connection
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(script_dir, "SableSpecimen_DB.accdb")
        connStr = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            r"DBQ=" + db_path + ";")
        try:
            conn = pyodbc.connect(connStr)
            cursor = conn.cursor()
            
            # Insert into Event table (adjust column names if needed)
            cursor.execute("INSERT INTO Event (Station, Haul, Haul_Date) VALUES (?, ?, ?)", (station, haul, haul_date))
            conn.commit()
            
            QtWidgets.QMessageBox.information(self, "Success", "New event saved successfully.")
            
            # Optionally, refresh the event table in the main window
            try:
                self.load_event_data()
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Refresh Error", f"Failed to refresh table: {str(e)}")
            
            # Clear the input fields for next entry
            ui.station.clear()
            ui.haul.clear()
            ui.date.clear()
            
            
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Failed to save event: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
        self.new_event_window.close()

    def return_to_menu(self):
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = EventSelectApp()
    window.show()
    sys.exit(app.exec_())