# Import the EventSelectApp class from the Event_Select module, which handles event data querying and display
from Event_Select.event_data_query import EventSelectApp
from Otolith_Entry.oto_event_select_window import OtolithEventDialog
# Import the Ui_MainWindow class from the ui module, which contains the UI setup for the main menu
from ui.main_menu import Ui_MainWindow
# Import necessary PyQt5 widgets: QApplication for the application instance and QMainWindow for the main window
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtGui import QPixmap
from Otolith_Entry.otolith_main import OtolithEntryApp

# Import sys module for system-level operations like exiting the application
import sys

# Define the MainWindow class, inheriting from QMainWindow (provides window functionality) and Ui_MainWindow (provides UI setup)
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Call the parent class constructors to initialize the window and UI
        super().__init__()
        # Set up the UI elements defined in Ui_MainWindow (loads the main menu interface)
        self.setupUi(self)
        # Connect the event_button's clicked signal to the open_event_select method
        self.event_button.clicked.connect(self.open_event_select)
        self.enter_otolith.clicked.connect(self.open_otolith_dialog)

    def open_otolith_dialog(self):
        dialog = OtolithEventDialog(self)
        # exec_() returns QDialog.Accepted (1) if self.accept() was called
        if dialog.exec_() == QDialog.Accepted:
            # Now we create the window as an attribute of MainWindow
            # This prevents it from being garbage collected
            self.otolith_entry_window = OtolithEntryApp(
                dialog.selected_station,
                dialog.selected_haul,
                parent=self
            )
            self.otolith_entry_window.show()

    def open_event_select(self):
        # Create an instance of EventSelectApp, which loads and displays event data in a table
        self.event_select = EventSelectApp()
        # Show the EventSelectApp window
        self.event_select.show()

# This block runs only if the script is executed directly (not imported as a module)
if __name__ == "__main__":
    # Create the QApplication instance, which manages the application's control flow and main settings
    app = QApplication(sys.argv)
    # Create an instance of MainWindow (our custom main window)
    window = MainWindow()
    # Display the main window
    window.show()
    # Start the application's event loop and exit when the loop ends
    sys.exit(app.exec_())