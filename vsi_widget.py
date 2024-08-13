from PyQt5 import QtWidgets, QtGui, QtCore
import math

class VerticalSpeedIndicatorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vertical_speed = 0
        self.direction = 1  # 1 for increasing, -1 for decreasing
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(500)  # Update every 500 milliseconds (0.5 second)
        self.setFixedSize(360, 360)
        self.setContentsMargins(0, 0, 0, 0)  # Set margins to zero

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        self.draw_background(painter)
        self.draw_speed_markings(painter)
        self.draw_digital_display(painter)
        self.draw_speed_triangle(painter)

    def draw_background(self, painter):
        # Fill the entire widget background with rounded corners
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), 30, 30)
        painter.setClipPath(path)
        painter.fillRect(self.rect(), QtGui.QColor("#151515"))

        # Draw the ellipse with the new background color inside
        ellipse_path = QtGui.QPainterPath()
        ellipse_path.addEllipse(26, 26, 308, 308)
        painter.setClipPath(ellipse_path)
        painter.fillRect(26, 26, 308, 308, QtGui.QColor("#2F3035"))
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QPen(QtGui.QColor("#454545"), 5))
        painter.drawEllipse(26, 26, 308, 308)

    def draw_speed_markings(self, painter):
        main_positions = {
            30: "10",   # 1 o'clock
            150: "-10", # 5 o'clock
            210: "-5",  # 7 o'clock
            270: "0",   # 9 o'clock
            330: "5"    # 11 o'clock
        }
        for angle, text in main_positions.items():
            rad_angle = math.radians(angle - 90)
            x1 = int(180 + 144 * math.cos(rad_angle))
            y1 = int(180 + 144 * math.sin(rad_angle))
            x2 = int(180 + 150 * math.cos(rad_angle))
            y2 = int(180 + 150 * math.sin(rad_angle))
            painter.setPen(QtGui.QPen(QtGui.QColor("#FFFFFF"), 5))
            painter.drawLine(x1, y1, x2, y2)

            # Draw numbers
            num_x = int(180 + 120 * math.cos(rad_angle))
            num_y = int(180 + 120 * math.sin(rad_angle))
            font = painter.font()
            font.setFamily("Courier")  # Set font to Courier
            font.setPointSize(22)
            font.setBold(True)  # Make numbers bold
            painter.setFont(font)
            painter.drawText(num_x - 20, num_y - 20, 40, 40, QtCore.Qt.AlignCenter, text)

        # Draw small tick marks
        for i in range(150, 390, 12):  # 150° to 390°
            if i not in main_positions.keys():  # Skip main positions
                angle = math.radians(i - 90)
                x1 = int(180 + 140 * math.cos(angle))
                y1 = int(180 + 140 * math.sin(angle))
                x2 = int(180 + 150 * math.cos(angle))
                y2 = int(180 + 150 * math.sin(angle))
                painter.setPen(QtGui.QPen(QtGui.QColor("#FFFFFF"), 2))
                painter.drawLine(x1, y1, x2, y2)

    def draw_digital_display(self, painter):
        rect = QtCore.QRect(110, 150, 140, 60)
        painter.setPen(QtGui.QPen(QtGui.QColor("#FFFFFF"), 2))
        painter.setBrush(QtGui.QColor("#000000"))
        painter.drawRect(rect)

        font = painter.font()
        font.setFamily("Courier")
        font.setPointSize(24)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(rect, QtCore.Qt.AlignCenter, f"{self.vertical_speed:.1f} m/s")

    def draw_speed_triangle(self, painter):
        # Calculate the angle for the current vertical speed
        angle = 270 + (self.vertical_speed * 12)  # 12 degrees per m/s indicator
        rad_angle = math.radians(angle - 90)
        x = int(180 + 150 * math.cos(rad_angle))
        y = int(180 + 150 * math.sin(rad_angle))

        # Draw the red triangle
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(QtGui.QColor("#FF0000")))

        # Define the triangle points
        triangle = QtGui.QPolygonF()
        triangle.append(QtCore.QPointF(x, y))
        triangle.append(QtCore.QPointF(x - 10, y + 20))
        triangle.append(QtCore.QPointF(x + 10, y + 20))

        # Rotate the triangle to match the angle
        transform = QtGui.QTransform()
        transform.translate(x, y)
        transform.rotate(angle)
        transform.translate(-x, -y)
        triangle = transform.map(triangle)

        painter.drawPolygon(triangle)

    def update_speed(self):
        # Logic to update vertical speed (For demo)
        if self.vertical_speed > 5:
            self.direction = -1
        elif self.vertical_speed < -5:
            self.direction = 1
        self.vertical_speed += self.direction * 0.1
        self.update()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = VerticalSpeedIndicatorWidget()
    widget.show()
    sys.exit(app.exec_())
