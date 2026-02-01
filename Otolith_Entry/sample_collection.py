import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from ui.sample_menu import Ui_sample_collections
from db_utils import db_connection

class SampleCollectionsDialog(QtWidgets.QDialog, Ui_sample_collections):
    def __init__(self, parent=None, preselected=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.selected_samples = []
        self.preselected = preselected or []
        
        self.sample_buttons = [
            self.pushButton,
            self.pushButton_2,
            self.pushButton_3,
            self.pushButton_4,
            self.pushButton_5,
            self.pushButton_6,
            self.pushButton_7,
            self.pushButton_8,
            self.pushButton_9
        ]
        
        self.populate_buttons()
        
        self.pushButton_11.clicked.connect(self.clear_selections)
        self.pushButton_12.clicked.connect(self.reject)
        self.pushButton_10.clicked.connect(self.confirm_selections)
    
    def populate_buttons(self):
        """Load sample types from database and assign to buttons"""
        with db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT Study_Code, Study_Name FROM Sample_Collections WHERE Active = 1 ORDER BY Study_Name")
            rows = cursor.fetchall()
        
        for i, (Study_Code, Study_Name) in enumerate(rows):
            if i < len(self.sample_buttons):
                button = self.sample_buttons[i]
                button.setText(Study_Code)
                button.setProperty('sample_name', Study_Name)  # Store name in property
                button.setCheckable(True)
                button.clicked.connect(self.toggle_button)
                
                # Pre-select if in preselected list
                if Study_Code in self.preselected:  # Fixed: use Study_Code
                    button.setProperty('selected', True)
                    button.setStyleSheet("background-color: lightblue;")
                    button.setChecked(True)
                else:
                    button.setProperty('selected', False)
            else:
                break
        
        # Hide unused buttons
        for i in range(len(rows), len(self.sample_buttons)):
            self.sample_buttons[i].hide()
    
    def toggle_button(self):
        """Handle button clicks"""
        button = self.sender()
        is_selected = button.property('selected')
        
        if is_selected:
            button.setProperty('selected', False)
            button.setStyleSheet("")
        else:
            button.setProperty('selected', True)
            button.setStyleSheet("background-color: lightblue;")
    
    def clear_selections(self):
        """Clear all selections"""
        for button in self.sample_buttons:
            if button.isVisible():
                button.setProperty('selected', False)
                button.setStyleSheet("")
                button.setChecked(False)
    
    def confirm_selections(self):
        """Collect selections and close dialog"""
        self.selected_samples = []
        for button in self.sample_buttons:
            if button.isVisible() and button.property('selected'):
                study_code = button.text()  # Code is on button
                study_name = button.property('sample_name')  # Name is in property
                self.selected_samples.append((study_code, study_name))
        
        self.accept()
    
    def get_selections(self):
        """Return the selected samples"""
        return self.selected_samples