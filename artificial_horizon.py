from PyQt5 import QtWidgets, QtGui, QtCore
import math

class ArtificialHorizon(QtWidgets.QWidget):
    def __init__(self, parent=None, sky_color="#4193F9", ground_color="#975B19"):
        super().__init__(parent)
        self.sky_color = sky_color
        self.ground_color = ground_color
        self.roll_angle = 0
        self.pitch_angle = 0  # Add pitch angle for demo
        self.pitch_direction = 1  # Add pitch direction for reversing
        self.rotation_state = 0  # State of rotation
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_horizon)
        self.timer.start(30)
        self.rotation_timer = QtCore.QTimer(self)
        self.rotation_timer.timeout.connect(self.toggle_rotation)
        self.rotation_timer.start(10000)  # 10 seconds interval
        self.setFixedSize(360, 360)
        self.setContentsMargins(0, 0, 0, 0)  # Set margins to zero

        # Create ALT label
        self.blinking_label = QtWidgets.QLabel("ALT", self)
        self.blinking_label.setStyleSheet("color: #333; background-color: transparent; border: 2px solid #333; border-radius: 5px; font-size: 18px;")
        self.blinking_label.setAlignment(QtCore.Qt.AlignCenter)
        self.blinking_label.setGeometry(20, 20, 50, 30)  # Adjust position and size
        self.blinking_label.setVisible(True)  # Initially visible

        self.blink_timer = QtCore.QTimer(self)
        self.blink_timer.timeout.connect(self.toggle_label_color)

        self.blink_cycle_timer = QtCore.QTimer(self)
        self.blink_cycle_timer.timeout.connect(self.toggle_blinking_cycle)
        self.blink_cycle_timer.start(15000)  # 15 seconds interval

        self.blinking = False  # Initial state of blinking

    def toggle_label_color(self):
        current_color = self.blinking_label.styleSheet()
        if "color: red" in current_color:
            self.blinking_label.setStyleSheet("color: #333; background-color: transparent; border: 2px solid #333; border-radius: 5px; font-size: 18px;")
        else:
            self.blinking_label.setStyleSheet("color: red; background-color: transparent; border: 2px solid red; border-radius: 5px; font-size: 18px;")

    def toggle_blinking_cycle(self):
        self.blinking = not self.blinking
        if self.blinking:
            self.blink_timer.start(500)  # Start blinking
            QtCore.QTimer.singleShot(5000, self.stop_blinking)  # Stop blinking after 5 seconds
        else:
            self.blinking_label.setStyleSheet("color: #333; background-color: transparent; border: 2px solid #333; border-radius: 5px; font-size: 18px;")

    def stop_blinking(self):
        self.blink_timer.stop()
        self.blinking_label.setStyleSheet("color: #333; background-color: transparent; border: 2px solid #333; border-radius: 5px; font-size: 18px;")

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Draw the rounded square background
        rounded_rect_path = QtGui.QPainterPath()
        rounded_rect_path.addRoundedRect(QtCore.QRectF(self.rect()), 30, 30)
        painter.fillPath(rounded_rect_path, QtGui.QColor("#171717"))

        # Draw the outer ellipse
        painter.setPen(QtGui.QPen(QtGui.QColor("#444"), 5))
        painter.drawEllipse(QtCore.QRectF(18, 18, 324, 324))  # Adjust the ellipse size and position

        # Create an elliptical clipping path
        ellipse_path = QtGui.QPainterPath()
        ellipse_path.addEllipse(QtCore.QRectF(20, 20, 320, 320))  # Adjust the ellipse size and position

        # Set the clipping path to the ellipse
        painter.setClipPath(ellipse_path)

        self.draw_horizon(painter)

    def draw_horizon(self, painter):
        width = self.width()
        height = self.height()
        center_x = width // 2
        center_y = height // 2

        # Define rectangles for the sky and ground
        sky_points = [
            QtCore.QPoint(center_x - width, center_y - height),
            QtCore.QPoint(center_x + width, center_y - height),
            QtCore.QPoint(center_x + width, center_y),
            QtCore.QPoint(center_x - width, center_y)
        ]

        ground_points = [
            QtCore.QPoint(center_x - width, center_y),
            QtCore.QPoint(center_x + width, center_y),
            QtCore.QPoint(center_x + width, center_y + height),
            QtCore.QPoint(center_x - width, center_y + height)
        ]

        # Rotate points
        roll_radians = math.radians(self.roll_angle)
        def rotate_point(point, angle, cx, cy):
            s = math.sin(angle)
            c = math.cos(angle)
            x = point.x() - cx
            y = point.y() - cy
            new_x = x * c - y * s
            new_y = x * s + y * c
            return QtCore.QPoint(int(new_x + cx), int(new_y + cy))

        rotated_sky_points = [rotate_point(point, roll_radians, center_x, center_y) for point in sky_points]
        rotated_ground_points = [rotate_point(point, roll_radians, center_x, center_y) for point in ground_points]

        # Draw the sky
        painter.setBrush(QtGui.QColor(self.sky_color))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawPolygon(QtGui.QPolygon(rotated_sky_points))

        # Draw the ground
        painter.setBrush(QtGui.QColor(self.ground_color))
        painter.drawPolygon(QtGui.QPolygon(rotated_ground_points))

        # Draw the separator line between sky and ground
        painter.setPen(QtGui.QPen(QtCore.Qt.gray, 1))
        painter.drawLine(rotated_sky_points[2], rotated_sky_points[3])

        # Draw pitch lines and pitch ladder
        self.draw_pitch_lines_and_ladder(painter, center_x, center_y)

        # Draw roll indicator
        self.draw_roll_indicator(painter, center_x, center_y)

        # Define the L-shaped plane outline points
        left_L = [
            QtCore.QPoint(center_x - 144, center_y - 5), QtCore.QPoint(center_x - 84, center_y - 5),
            QtCore.QPoint(center_x - 84, center_y - 5), QtCore.QPoint(center_x - 74, center_y - 5),
            QtCore.QPoint(center_x - 74, center_y + 22), QtCore.QPoint(center_x - 84, center_y + 22),
            QtCore.QPoint(center_x - 84, center_y + 5), QtCore.QPoint(center_x - 144, center_y + 5)
        ]

        right_L = [
            QtCore.QPoint(center_x + 144, center_y - 5), QtCore.QPoint(center_x + 84, center_y - 5),
            QtCore.QPoint(center_x + 84, center_y - 5), QtCore.QPoint(center_x + 74, center_y - 5),
            QtCore.QPoint(center_x + 74, center_y + 22), QtCore.QPoint(center_x + 84, center_y + 22),
            QtCore.QPoint(center_x + 84, center_y + 5), QtCore.QPoint(center_x + 144, center_y + 5)
        ]

        # Draw plane outline
        painter.setPen(QtGui.QPen(QtGui.QColor("yellow"), 3))
        painter.setBrush(QtGui.QColor("black"))
        painter.drawPolygon(QtGui.QPolygon(left_L))
        painter.drawPolygon(QtGui.QPolygon(right_L))

        # Draw smaller square at the center
        square_size = 10
        painter.drawRect(center_x - square_size // 2, center_y - square_size // 2, square_size, square_size)

        # Update roll angle and pitch angle (for demon)
        if self.rotation_state == 1:  # Rotate to +20 degrees
            self.roll_angle += 0.2
            if self.roll_angle >= 20:
                self.rotation_state = 2
        elif self.rotation_state == 2:  # Rotate to -20 degrees
            self.roll_angle -= 0.2
            if self.roll_angle <= -20:
                self.rotation_state = 3
        elif self.rotation_state == 3:  # Return to initial state
            self.roll_angle += 0.2
            if self.roll_angle >= 0:
                self.roll_angle = 0
                self.rotation_state = 0

        self.pitch_angle += 0.2 * self.pitch_direction
        if self.pitch_angle >= 30 or self.pitch_angle <= -30:
            self.pitch_direction *= -1

    def draw_pitch_lines_and_ladder(self, painter, center_x, center_y):
        pitch_angles = [-30, -27.5, -25, -22.5, -20, -17.5, -15, -12.5, -10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30]
        ellipse_radius = 160  # Half of the ellipse size = (320 / 2)
        fade_start_distance = ellipse_radius * 0.55  # Start fading at 55% of the radius
        for i, pitch in enumerate(pitch_angles):
            y = int(center_y - (pitch + self.pitch_angle) * 6)  # Controls vertical spacing between lines of the ladder
            distance_from_center = abs(y - center_y)
            if distance_from_center < fade_start_distance:
                fade_factor = 1
            else:
                fade_factor = max(0, 1 - (distance_from_center - fade_start_distance) / (ellipse_radius - fade_start_distance))
            line_length = int(34 * fade_factor)  # Pitch line length
            opacity = int(255 * fade_factor)

            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, opacity), 2))
            font = QtGui.QFont()
            font.setPointSize(12)
            painter.setFont(font)
            if pitch % 10 == 0:  # Long lines with degree labels
                painter.drawLine(center_x - line_length, y, center_x + line_length, y)
                painter.drawText(center_x - 64, y + 5, f"{pitch:>3}")
                painter.drawText(center_x + 40, y + 5, f"{pitch:<3}")
            elif pitch % 5 == 0:  # Medium lines
                painter.drawLine(center_x - int(line_length // 1.5), y, center_x + int(line_length // 1.5), y)
            else:  # Short lines
                painter.drawLine(center_x - line_length // 2, y, center_x + line_length // 2, y)

    def draw_roll_indicator(self, painter, center_x, center_y):
        painter.setPen(QtGui.QPen(QtCore.Qt.white, 2))
        painter.drawArc(center_x - 150, center_y - 150, 300, 300, 16 * 45, 16 * 90)  # Draw arc for roll indicator
        painter.drawLine(center_x, center_y - 150, center_x, center_y - 140)  # Draw center tick mark

    def toggle_rotation(self):
        self.rotation_state = 1  # Start the rotation cycle

    def update_horizon(self):
        if self.rotation_state == 1:  # Rotate to +20 degrees
            self.roll_angle += 0.2
            if self.roll_angle >= 20:
                self.rotation_state = 2
        elif self.rotation_state == 2:  # Rotate to -20 degrees
            self.roll_angle -= 0.2
            if self.roll_angle <= -20:
                self.rotation_state = 3
        elif self.rotation_state == 3:  # Return to initial state
            self.roll_angle += 0.2
            if self.roll_angle >= 0:
                self.roll_angle = 0
                self.rotation_state = 0

        self.update()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = ArtificialHorizon()
    window.show()
    sys.exit(app.exec_())
