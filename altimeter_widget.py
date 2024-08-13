from PyQt5 import QtWidgets, QtGui, QtCore
import math

class AltimeterWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.altitude = 0
        self.target_altitude = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_altitude)
        self.timer.start(30)  # Update every 30 milliseconds
        self.setFixedSize(360, 360)
        self.setContentsMargins(0, 0, 0, 0)  # Set margins to zero

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Create a clipping path with rounded corners
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), 30, 30)
        painter.setClipPath(path)

        # Fill the background
        painter.fillRect(self.rect(), QtGui.QColor("#171717"))

        # Draw the altimeter circle
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QPen(QtGui.QColor("#454545"), 5))
        painter.drawEllipse(26, 26, 308, 308)  # Adjusted to 308x308

        # Draw altitude markings and numbers
        for i in range(0, 360, 36):  # 10 major tick marks
            angle = math.radians(i - 90)  # Adjust angle to start from 12 o'clock
            x1 = int(180 + 135 * math.cos(angle))
            y1 = int(180 + 135 * math.sin(angle))
            x2 = int(180 + 150 * math.cos(angle))
            y2 = int(180 + 150 * math.sin(angle))
            painter.setPen(QtGui.QPen(QtGui.QColor("#FFFFFF"), 5))
            painter.drawLine(x1, y1, x2, y2)

            # Draw the numbers
            number = (i // 36) % 10
            num_x = int(180 + 120 * math.cos(angle))
            num_y = int(180 + 120 * math.sin(angle))
            font = painter.font()
            font.setFamily("Courier")  # Set font to Courier
            font.setPointSize(22)
            font.setBold(True)  # Make numbers bold
            painter.setFont(font)
            painter.drawText(num_x - 20, num_y - 20, 40, 40, QtCore.Qt.AlignCenter, str(number))  # Adjusted position and size

            # Draw the smaller tick marks
            for j in range(1, 5):  # 4 tick marks
                small_angle = angle + math.radians(j * 7.2)
                x1 = int(180 + 140 * math.cos(small_angle))
                y1 = int(180 + 140 * math.sin(small_angle))
                x2 = int(180 + 150 * math.cos(small_angle))
                y2 = int(180 + 150 * math.sin(small_angle))
                painter.setPen(QtGui.QPen(QtGui.QColor("#FFFFFF"), 2))
                painter.drawLine(x1, y1, x2, y2)

        # Draw the "ALT" label
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 1))
        painter.setBrush(QtGui.QColor("#444"))
        painter.drawRect(120, 120, 60, 30)  # Move ALT label slightly lower and closer to center
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 2))
        painter.drawText(120, 120, 60, 30, QtCore.Qt.AlignCenter, "ALT")

        # Draw the labels "100" and "Feet" following the circular arc
        font.setPointSize(8)  # Set smaller font size
        painter.setFont(font)
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 2))

        # Draw "100" label on the left half between 9 and 0
        angle = math.radians(-110)  # Adjust angle to position the text
        painter.save()
        painter.translate(180 + 140 * math.cos(angle), 180 + 140 * math.sin(angle))
        painter.rotate(math.degrees(angle) + 90)
        painter.drawText(-10, 16, "100")  # Adjust text position
        painter.restore()

        # Draw "FEET" label on the right half between 0 and 1
        angle = math.radians(-76)  # Adjust angle to position the text
        painter.save()
        painter.translate(180 + 140 * math.cos(angle), 180 + 140 * math.sin(angle))
        painter.rotate(math.degrees(angle) + 90)
        painter.drawText(-11, 16, "F")  # Adjust text position for each letter
        painter.drawText(0, 16, "E")
        painter.drawText(10, 17, "E")
        painter.drawText(20, 18, "T")
        painter.restore()

        # Draw the second hand (hundreds of feet)
        angle = math.radians((self.altitude % 1000) * 360 / 1000 - 90)
        x = int(180 + 114 * math.cos(angle))
        y = int(180 + 114 * math.sin(angle))

        # Draw the thicker line for the second hand
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 9))  # Increase thickness
        painter.drawLine(180, 180, x, y)

        # Draw the pointy triangle at the end of the line
        mid_x = int(180 + 118 * math.cos(angle))
        mid_y = int(180 + 118 * math.sin(angle))
        triangle_path = QtGui.QPainterPath()
        triangle_path.moveTo(mid_x + 10 * math.cos(angle), mid_y + 10 * math.sin(angle))  # Adjust triangle position
        triangle_path.lineTo(mid_x + 4 * math.cos(angle - math.radians(90)), mid_y + 4 * math.sin(angle - math.radians(90)))
        triangle_path.lineTo(mid_x + 4 * math.cos(angle + math.radians(90)), mid_y + 4 * math.sin(angle + math.radians(90)))
        triangle_path.closeSubpath()
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 1))
        painter.setBrush(QtGui.QColor("white"))
        painter.drawPath(triangle_path)

        # Draw the hour hand (thousands of feet) with varying thickness
        angle = math.radians((self.altitude // 1000) * 360 / 10 - 90)

        # Define the lengths for each segment
        length1 = 20  # First 1/3 (thin)
        length2 = 60  # Remaining 2/3 (thick)

        # Calculate the points for each segment
        x1 = int(180 + length1 * math.cos(angle))
        y1 = int(180 + length1 * math.sin(angle))
        x2 = int(x1 + length2 * math.cos(angle))
        y2 = int(y1 + length2 * math.sin(angle))

        # Draw the first thin segment
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 3))
        painter.drawLine(180, 180, x1, y1)

        # Draw the remaining thick segment
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 9))
        painter.drawLine(x1, y1, x2, y2)

        # Draw the shortest needle (tens of thousands of feet) with an upside-down triangle
        angle = math.radians((self.altitude // 10000) * 360 / 10 - 90)
        x = int(180 + 150 * math.cos(angle))  # Extends the line length to reach the ellipse
        y = int(180 + 150 * math.sin(angle))

        # Draw the thicker bottom half of the hand with a border
        painter.setPen(QtGui.QPen(QtGui.QColor("black"), 15))  # Border
        painter.drawLine(180, 180, int(180 + 75 * math.cos(angle)), int(180 + 75 * math.sin(angle)))
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 6))  # Fill
        painter.drawLine(180, 180, int(180 + 75 * math.cos(angle)), int(180 + 75 * math.sin(angle)))

        # Draw the thinner top half of the hand with a border
        painter.setPen(QtGui.QPen(QtGui.QColor("black"), 5))  # Border
        painter.drawLine(int(180 + 75 * math.cos(angle)), int(180 + 75 * math.sin(angle)), x, y)
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 3))  # Fill
        painter.drawLine(int(180 + 75 * math.cos(angle)), int(180 + 75 * math.sin(angle)), x, y)

        # Draw the smaller white triangle higher on the line with a black border
        triangle_x = int(180 + 146 * math.cos(angle))  # Move the triangle higher by increasing the distance from the center
        triangle_y = int(180 + 146 * math.sin(angle))
        triangle_path = QtGui.QPainterPath()
        triangle_path.moveTo(triangle_x - 30 * math.cos(angle), triangle_y - 30 * math.sin(angle))  # Adjust triangle position
        triangle_path.lineTo(triangle_x + 15 * math.cos(angle - math.radians(90)), triangle_y + 15 * math.sin(angle - math.radians(90)))  # Adjust triangle size
        triangle_path.lineTo(triangle_x + 15 * math.cos(angle + math.radians(90)), triangle_y + 15 * math.sin(angle + math.radians(90)))  # Adjust triangle size
        triangle_path.closeSubpath()
        painter.setPen(QtGui.QPen(QtGui.QColor("black"), 1))  # Border
        painter.setBrush(QtGui.QColor("white"))  # Fill
        painter.drawPath(triangle_path)
        
    def update_altitude(self):
        self.altitude += 2  # Simulate slower altitude change (For demo)
        if self.altitude > 100000:
            self.altitude = 0
        self.update()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = AltimeterWidget()
    window.show()
    sys.exit(app.exec_())
