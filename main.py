from PyQt5 import QtWidgets, QtCore, QtGui
import sys
from artificial_horizon import ArtificialHorizon
from compass_widget import CompassWidget
from altimeter_widget import AltimeterWidget
from vsi_widget import VerticalSpeedIndicatorWidget  # Import your new widget

def create_labeled_widget(widget, label_text):
    container = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(5)

    label = QtWidgets.QLabel(label_text)
    label.setStyleSheet("color: #888; font-size: 16px; padding-left: 10px;")  # Add left padding
    label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
    layout.addWidget(label)
    layout.addWidget(widget)

    return container

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    main_window.setWindowTitle("Aero Display")
    main_window.setGeometry(100, 100, 1000, 800)
    main_window.setStyleSheet("background-color: black;")

    # Create instance of each widget
    horizon_widget = ArtificialHorizon()
    horizon_widget.setStyleSheet("border-radius: 40px; background-color: black;")
    
    compass_widget = CompassWidget()
    compass_widget.setStyleSheet("border-radius: 40px; background-color: black;")
    
    altimeter_widget = AltimeterWidget()
    altimeter_widget.setStyleSheet("border-radius: 40px; background-color: black;")
    
    vsi_widget = VerticalSpeedIndicatorWidget()
    vsi_widget.setStyleSheet("border-radius: 40px; background-color: black;")
    
    container = QtWidgets.QWidget()
    main_layout = QtWidgets.QGridLayout(container)
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(10)

    # Add widgets to the grid layout with fixed positions
    main_layout.addWidget(create_labeled_widget(horizon_widget, "Artificial Horizon"), 0, 0)
    main_layout.addWidget(create_labeled_widget(compass_widget, "Compass"), 0, 1)
    main_layout.addWidget(create_labeled_widget(altimeter_widget, "Altimeter"), 0, 2)
    main_layout.addWidget(create_labeled_widget(vsi_widget, "Vertical Speed Indicator"), 1, 0, 1, 3, alignment=QtCore.Qt.AlignLeft)

    # Add spacers to maintain constant margins
    main_layout.setRowStretch(0, 1)
    main_layout.setRowStretch(1, 1)
    main_layout.setColumnStretch(0, 1)
    main_layout.setColumnStretch(1, 1)
    main_layout.setColumnStretch(2, 1)

    main_window.setCentralWidget(container)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
