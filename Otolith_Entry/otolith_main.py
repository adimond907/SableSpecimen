import os
import pyodbc
import subprocess
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtCore import Qt
from ui.otolith_menu import Ui_Otolith_Entry
from db_utils import db_connection
from Otolith_Entry.sample_collection import SampleCollectionsDialog

class OtolithEntryApp(QtWidgets.QMainWindow, Ui_Otolith_Entry):
    def __init__(self, station, haul, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Store the event data
        self.selected_station = station
        self.selected_haul = haul
        
        # Display the event data
        self.station_number.setText(station)
        self.haul_number.setText(haul)
        self.oto_number.setText(self.get_oto_num())
        self.get_depths()
        self.get_sex()
        self.get_maturity()
        self.get_oto_cond()

        #track sample collections
        self.current_sample_selections = []
        
        # Create a validator that only allows integers
        # Optional: Set a range, e.g., 0 to 9999
        int_validator = QIntValidator(0, 9999, self)

        # Apply it to your boxes
        self.length_box.setValidator(int_validator)
        self.weight_box.setValidator(int_validator)
        # Connect buttons
        self.menu_button.clicked.connect(self.close)
        self.sample_col_button.clicked.connect(self.open_sample_collection)
        self.next_button.clicked.connect(self.go_next)

        #set up plot
        self.plot_label.setScaledContents(True)
        self.plot_label.setAlignment(Qt.AlignCenter)

        self.update_plot()

    def update_plot(self):
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(script_dir, "SableSpecimen_DB.accdb")
        r_script_path = os.path.join(script_dir, "Otolith_Entry", "lw_plot.R")
        rscript_exe = os.path.join(script_dir, "R-portable", "bin", "Rscript.exe")
        plot_path = os.path.join(script_dir, "Otolith_Entry", "lw_plot.png")  # Define it here!
        
        # Check if bundled R exists
        if not os.path.exists(rscript_exe):
            QtWidgets.QMessageBox.warning(
                self, 
                "R Not Found", 
                f"R installation not found at:\n{rscript_exe}"
            )
            return
        
        try:
            subprocess.run(
                [rscript_exe, r_script_path, db_path],
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.warning(
                self, 
                "R Script Error", 
                f"Failed to run R script:\n{e.stderr}"
            )
            return
        
        # Load and display the plot
        pixmap = QPixmap(plot_path)
        
        if pixmap.isNull():
            QtWidgets.QMessageBox.warning(
                self, 
                "Image Error", 
                f"Failed to load plot image from: {plot_path}"
            )
        else:
            self.plot_label.setPixmap(pixmap)


    def get_oto_num(self):
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(Otolith_number) FROM otolith;")
            result = cursor.fetchone()

            if result[0] is None:
                oto_num = 1  # Start at 1 if table is empty
            else:
                oto_num = result[0] + 1

        return str(oto_num)
    
    def get_depths(self):
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Stratum_name FROM Depths")
            rows = cursor.fetchall()

            current_selection = self.depth_box.currentText()

            self.depth_box.clear()
            for row in rows:
                self.depth_box.addItem(str(row[0]))

            if current_selection:
                index = self.depth_box.findText(current_selection)
                if index >= 0:
                    self.depth_box.setCurrentIndex(index)

    
    def get_sex(self):
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Sex_Code, Sex FROM Sex")
            rows = cursor.fetchall()

            self.sex_box.clear()
            self.sex_box.addItem("", None)
            for row in rows:
                combined_text = str(row[0]) + " - " + str(row[1])
                self.sex_box.addItem(combined_text)
    
    def get_maturity(self):
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Maturity_Code FROM Maturity")
            rows = cursor.fetchall()

            self.maturity_box.clear()

            self.maturity_box.addItem("", None)
            for row in rows:
                self.maturity_box.addItem(str(row[0]))

    def get_oto_cond(self):
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Description FROM Otolith_Condition ORDER BY Condition_ID")
            rows = cursor.fetchall()

            self.cond_box.clear()
            for row in rows:
                self.cond_box.addItem(str(row[0]))
        
    def open_sample_collection(self):
        """Open the sample collections dialog"""
        dialog = SampleCollectionsDialog(self, preselected=[s[0] for s in self.current_sample_selections])
        #save the values
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.current_sample_selections = dialog.get_selections()


    def go_next(self):
        with db_connection() as conn:
            cursor = conn.cursor()
            if self.current_sample_selections:
                selected_samples_str = ','.join([code for code, name in self.current_sample_selections])
            else:
                selected_samples_str = '' 


            cursor.execute("""
            INSERT INTO Otolith (
                [Otolith_Number], [Haul_Number], [Depth_Strata], [Sex], [Maturity], 
                [Length], [Weight], [Sample_Collections], [Otolith_Condition], [Comments]
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            int(self.oto_number.text()),
            int(self.haul_number.text()),
            int(self.depth_box.currentText()),
            int(self.sex_box.currentText().split('-')[0].strip()),
            int(self.maturity_box.currentText()),
            int(self.length_box.Text()),
            int(self.weight_box.Text()),
            selected_samples_str,
            self.cond_box.currentText(),
            self.comments_box.toPlainText(),
            ))

            conn.commit()
        self.current_sample_selections = []
        self.update_plot()
        self.oto_number.setText(self.get_oto_num())
        self.clear_form()

    def clear_form(self):
        self.length_box.clear()
        self.weight_box.clear()
        self.comments_box.clear()
        self.sex_box.setCurrentIndex(0)
        self.maturity_box.setCurrentIndex(0)
        self.cond_box.setCurrentIndex(0)

            

        



