from PyQt5 import QtWidgets, QtGui, QtCore
import math

class VerticalSpeedIndicatorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vertical_speed = 0
        self.direction = 1  # 1 for increasing, -1 for decreasing
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_speed)
        self.timer.start(500)  # Update every 500 milliseconds
        self.setFixedSize(360, 360)
        self.setContentsMargins(0, 0, 0, 0)

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

        # Draw the outer ellipse with gradient background
        gradient = QtGui.QRadialGradient(180, 180, 180)
        gradient.setColorAt(0, QtGui.QColor("#555"))
        gradient.setColorAt(1, QtGui.QColor("#222"))
        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(14, 14, 332, 332)

        # Draw the main ellipse with the gradient
        ellipse_path = QtGui.QPainterPath()
        ellipse_path.addEllipse(26, 26, 308, 308)
        painter.setClipPath(ellipse_path)

        gradient = QtGui.QRadialGradient(180, 180, 154)
        gradient.setColorAt(1, QtGui.QColor("#1D1E21"))
        gradient.setColorAt(0.9, QtGui.QColor("#2F3035"))
        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawEllipse(26, 26, 308, 308)

        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QPen(QtGui.QColor("#222"), 5))
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
            x1 = int(180 + 136 * math.cos(rad_angle))
            y1 = int(180 + 136 * math.sin(rad_angle))
            x2 = int(180 + 150 * math.cos(rad_angle))
            y2 = int(180 + 150 * math.sin(rad_angle))
            painter.setPen(QtGui.QPen(QtGui.QColor("#B3C1C9"), 5))
            painter.drawLine(x1, y1, x2, y2)

            # Draw numbers
            num_x = int(180 + 112 * math.cos(rad_angle))
            num_y = int(180 + 112 * math.sin(rad_angle))
            font = painter.font()
            font.setFamily("Arial")
            font.setPointSize(18) 
            font.setBold(True) 
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
                painter.setPen(QtGui.QPen(QtGui.QColor("#B3C1C9"), 2))
                painter.drawLine(x1, y1, x2, y2)

    def draw_digital_display(self, painter):
        # Define the rectangle and the half-circle path
        rect = QtCore.QRect(152, 126, 208, 100)
        path = QtGui.QPainterPath()
        path.moveTo(152, 126)  # Start at the top-left corner of the rectangle
        path.arcTo(102, 126, 100, 100, 90, 180)  # Draw the half-circle
        path.lineTo(152, 226)  # Draw the left side of the rectangle
        path.lineTo(360, 226)  # Draw the bottom line of the rectangle
        path.lineTo(360, 126)  # Draw the right side of the rectangle
        path.closeSubpath() 

        # Draw the path
        painter.setPen(QtGui.QPen(QtGui.QColor("#aaa"), 2))
        painter.setBrush(QtGui.QColor("#15161C"))
        painter.drawPath(path)

        # Draw the text inside the path
        font = QtGui.QFont("Arial", 22, QtGui.QFont.Bold)
        painter.setFont(font)
        painter.setPen(QtGui.QPen(QtGui.QColor("#CBEAFB")))

        # Adjust the text position by moving it to the left
        text_rect = rect.adjusted(-30, 0, -30, 0)  # Move 30 pixels to the left
        painter.drawText(text_rect, QtCore.Qt.AlignCenter, f"{self.vertical_speed:.1f} m/s")

        # Add the "VARIO" label
        vario_font = QtGui.QFont("Arial", 8, QtGui.QFont.Bold) 
        painter.setFont(vario_font)
        painter.setPen(QtGui.QPen(QtGui.QColor("#CBEAFB")))
        painter.drawText(rect.adjusted(10, 10, 0, 0), QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop, "VARIO")

    def draw_speed_triangle(self, painter):
        # Calculate the angle for the current vertical speed
        angle = 270 + (self.vertical_speed * 12)  # 12 degrees per m/s
        rad_angle = math.radians(angle - 90)
        x = int(180 + 150 * math.cos(rad_angle))
        y = int(180 + 150 * math.sin(rad_angle))

        # Define the trapezoid points
        trapezoid = QtGui.QPolygonF()
        trapezoid.append(QtCore.QPointF(x - 4, y))
        trapezoid.append(QtCore.QPointF(x + 4, y))
        trapezoid.append(QtCore.QPointF(x + 8, y + 30))
        trapezoid.append(QtCore.QPointF(x - 8, y + 30))

        # Rotate the trapezoid to match the angle
        transform = QtGui.QTransform()
        transform.translate(x, y)
        transform.rotate(angle)
        transform.translate(-x, -y)
        trapezoid = transform.map(trapezoid)

        # Draw the trapezoid with transparent fill and red outline
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QPen(QtGui.QColor("#EA5132"), 4))
        painter.drawPolygon(trapezoid)

    def update_speed(self):
        # Logic to update vertical speed
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
