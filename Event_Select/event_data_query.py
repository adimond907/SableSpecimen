#import necessary packages/functions
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
        self.edit_event.clicked.connect(self.edit_event)
    
    def edit_event(self):
        self.close()


    def load_event_data(self):
        # Database connection and query
        connStr = (
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
        r"DBQ=C:\Users\jadim\OneDrive\Documents\TestDB.accdb;")
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
        connStr = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            r"DBQ=C:\Users\jadim\OneDrive\Documents\TestDB.accdb;")
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

    def return_to_menu(self):
        self.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = EventSelectApp()
    window.show()
    sys.exit(app.exec_())