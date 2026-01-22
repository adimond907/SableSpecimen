# Import the EventSelectApp class from the Event_Select module, which handles event data querying and display
from Event_Select.event_data_query import EventSelectApp

# Import the Ui_MainWindow class from the ui module, which contains the UI setup for the main menu
from ui.main_menu import Ui_MainWindow

# Import necessary PyQt5 widgets: QApplication for the application instance and QMainWindow for the main window
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap

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
        #self.oto_button.clicked.connect(self.open_otolith_select)
        self.addimage()

    def open_event_select(self):
        # Create an instance of EventSelectApp, which loads and displays event data in a table
        self.event_select = EventSelectApp()
        # Show the EventSelectApp window
        self.event_select.show()

    def addimage(self):
        qpixmap = QPixmap("Sablefish.jpg")
        self.label.setPixmap(qpixmap)

# This block runs only if the script is executed directly (not imported as a module)
if __name__ == "__main__":
    # Create the QApplication insta~nce, which manages the application's control flow and main settings
    app = QApplication(sys.argv)
    # Create an instance of MainWindow (our custom main window)
    window = MainWindow()
    # Display the main window
    window.show()
    # Start the application's event loop and exit when the loop ends
    sys.exit(app.exec_())


