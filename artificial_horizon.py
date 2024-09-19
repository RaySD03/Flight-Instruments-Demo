from PyQt5 import QtWidgets, QtGui, QtCore
import math

class ArtificialHorizon(QtWidgets.QWidget):
    def __init__(self, parent=None, sky_color="#4193F9", ground_color="#975B19"):
        super().__init__(parent)
        self.sky_color = sky_color
        self.ground_color = ground_color
        self.roll_angle = 0
        self.pitch_angle = 0  # Add pitch angle for demonstration
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

        # Calculate vertical offset based on pitch angle and invert it
        pitch_offset = int(-self.pitch_angle * height / 90)  # Adjust the divisor for sensitivity

        # Define rectangles for the sky and ground with pitch offset
        sky_points = [
            QtCore.QPoint(center_x - width, center_y - height + pitch_offset),
            QtCore.QPoint(center_x + width, center_y - height + pitch_offset),
            QtCore.QPoint(center_x + width, center_y + pitch_offset),
            QtCore.QPoint(center_x - width, center_y + pitch_offset)
        ]

        ground_points = [
            QtCore.QPoint(center_x - width, center_y + pitch_offset),
            QtCore.QPoint(center_x + width, center_y + pitch_offset),
            QtCore.QPoint(center_x + width, center_y + height + pitch_offset),
            QtCore.QPoint(center_x - width, center_y + height + pitch_offset)
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

        # Create gradient for the sky
        sky_gradient = QtGui.QLinearGradient(0, center_y - height + pitch_offset, 0, center_y + pitch_offset)
        sky_gradient.setColorAt(0, QtGui.QColor("#2A6EC9"))  # Top color
        sky_gradient.setColorAt(1, QtGui.QColor("#7CB5EB"))  # Bottom color

        # Create gradient for the ground
        ground_gradient = QtGui.QLinearGradient(0, center_y + pitch_offset, 0, center_y + height + pitch_offset)
        ground_gradient.setColorAt(0, QtGui.QColor("#975B19"))  # Top color
        ground_gradient.setColorAt(1, QtGui.QColor("#654321"))  # Bottom color

        # Draw the sky with gradient
        painter.setBrush(sky_gradient)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawPolygon(QtGui.QPolygon(rotated_sky_points))

        # Draw the ground with gradient
        painter.setBrush(ground_gradient)
        painter.drawPolygon(QtGui.QPolygon(rotated_ground_points))

        # Draw the separator line between sky and ground
        painter.setPen(QtGui.QPen(QtCore.Qt.gray, 1))
        painter.drawLine(rotated_sky_points[2], rotated_sky_points[3])

        # Draw pitch lines and pitch ladder
        self.draw_pitch_lines_and_ladder(painter, center_x, center_y)

        # Draw bank angle arc with tick marks
        self.draw_bank_angle_arc(painter, center_x, center_y)

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

        # Update roll angle and pitch angle for demonstration
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

    def draw_bank_angle_arc(self, painter, center_x, center_y):
        # Draw the arc at the top of the container circle
        arc_rect = QtCore.QRect(center_x - 145, center_y - 145, 290, 290)
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 2))
        painter.drawArc(arc_rect, 60 * 16, 60 * 16)  # Draw arc from -30 to +30 degrees

        # Draw tick marks for bank angles (rotated rectangles)
        for angle in range(-30, 31, 10):
            tick_length = 14 if angle % 30 == 0 else 10  # Adjust rectangles' size
            tick_angle = math.radians(angle - 90)  # Adjust angle to align with the top arc
            x1 = center_x + 158 * math.cos(tick_angle)
            y1 = center_y + 158 * math.sin(tick_angle)
            x2 = center_x + (158 - tick_length) * math.cos(tick_angle)
            y2 = center_y + (158 - tick_length) * math.sin(tick_angle)
            
            if angle == 0:
                # Define points for the inverted yellow triangle
                triangle_points = [
                    QtCore.QPoint(int((x1 + x2) / 2), int(y2)),
                    QtCore.QPoint(int((x1 + x2) / 2 - 8), int(y1)),
                    QtCore.QPoint(int((x1 + x2) / 2 + 8), int(y1))
                ]
                painter.setPen(QtGui.QPen(QtGui.QColor("yellow"), 2))
                painter.setBrush(QtCore.Qt.NoBrush)
                painter.drawPolygon(QtGui.QPolygon(triangle_points))
            else:
                # Define the rectangle for the tick mark
                rect_width = 6  # Width of the rectangle
                painter.setPen(QtGui.QPen(QtGui.QColor("white"), 2))
                rect_height = abs(y1 - y2)  # Height of the rectangle
                rect_center_x = (x1 + x2) / 2
                rect_center_y = (y1 + y2) / 2
                
                # Create the rectangle centered on the arc
                rect = QtCore.QRectF(rect_center_x - rect_width / 2, rect_center_y - rect_height / 2, rect_width, rect_height)
                
                # Create a QTransform object to apply rotation
                transform = QtGui.QTransform()
                transform.translate(rect_center_x, rect_center_y)
                transform.rotate(angle)
                transform.translate(-rect_center_x, -rect_center_y)
                
                # Apply the transformation and draw the rectangle with no fill
                painter.setTransform(transform)
                painter.setBrush(QtCore.Qt.NoBrush)
                painter.drawRect(rect)
                painter.resetTransform()  # Reset transformation for the next tick mark

        # Draw the moving trapezoid and triangle
        triangle_angle = math.radians(-self.roll_angle - 90)  # Adjust angle to align with the top arc
        triangle_x = int(center_x + 140 * math.cos(triangle_angle))
        triangle_y = int(center_y + 140 * math.sin(triangle_angle))

        # Define points for the inverted trapezoid
        trapezoid_points = [
            QtCore.QPoint(triangle_x - 12, triangle_y + 18),
            QtCore.QPoint(triangle_x + 12, triangle_y + 18),
            QtCore.QPoint(triangle_x + 16, triangle_y + 25),
            QtCore.QPoint(triangle_x - 16, triangle_y + 25)
        ]

        # Define points for the triangle
        triangle_points = [
            QtCore.QPoint(triangle_x, triangle_y),
            QtCore.QPoint(triangle_x - 10, triangle_y + 14),
            QtCore.QPoint(triangle_x + 10, triangle_y + 14)
        ]

        # Draw the trapezoid and triangle with yellow outline and no fill
        painter.setPen(QtGui.QPen(QtGui.QColor("yellow"), 2))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawPolygon(QtGui.QPolygon(trapezoid_points))
        painter.drawPolygon(QtGui.QPolygon(triangle_points))

        # Draw the horizontal yellow line
        line_y = triangle_y + 34  # Adjust the position as needed
        painter.setPen(QtGui.QPen(QtGui.QColor("yellow"), 2))
        painter.drawLine(center_x - 150, line_y, center_x + 150, line_y)

        # Draw the horizontal white line
        white_line_y = center_y + 106  # Adjust the position as needed
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 2))
        painter.drawLine(center_x - 150, white_line_y, center_x + 150, white_line_y)

    def draw_pitch_lines_and_ladder(self, painter, center_x, center_y):
        pitch_angles = [-30, -27.5, -25, -22.5, -20, -17.5, -15, -12.5, -10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30]
        ellipse_radius = 160  # Half of the ellipse size = (320 / 2)
        fade_start_distance = ellipse_radius * 0.55  # Start fading at 55% of the radius

        # Define the top and bottom limits for the pitch ladder
        top_limit = center_y - 100  # Adjust this value as needed
        bottom_limit = center_y + 100  # Adjust this value as needed

        for i, pitch in enumerate(pitch_angles):
            y = int(center_y - (pitch + self.pitch_angle) * 8)  # Controls vertical spacing between lines

            # Skip drawing lines outside the top and bottom limits
            if y < top_limit or y > bottom_limit:
                continue

            distance_from_center = abs(y - center_y)
            if distance_from_center < fade_start_distance:
                fade_factor = 1
            else:
                fade_factor = max(0, 1 - (distance_from_center - fade_start_distance) / (ellipse_radius - fade_start_distance))

            # Adjust fade factor based on proximity to the top and bottom limits
            if y < top_limit + 20:
                fade_factor *= (y - top_limit) / 20
            elif y > bottom_limit - 20:
                fade_factor *= (bottom_limit - y) / 20

            line_length = int(34 * fade_factor)  # Pitch line length
            opacity = int(255 * fade_factor)

            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, opacity), 2))
            font = QtGui.QFont()
            font.setPointSize(12)  # Increase font size
            painter.setFont(font)
            if pitch % 10 == 0:  # Long lines with labels
                painter.drawLine(center_x - line_length, y, center_x + line_length, y)
                painter.drawText(center_x - 64, y + 5, f"{pitch:>3}")  # Move numbers closer
                painter.drawText(center_x + 40, y + 5, f"{pitch:<3}")  # Move numbers closer
            elif pitch % 5 == 0:  # Medium lines
                painter.drawLine(center_x - int(line_length // 1.5), y, center_x + int(line_length // 1.5), y)
            else:  # Short lines
                painter.drawLine(center_x - line_length // 2, y, center_x + line_length // 2, y)

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
