from PyQt5 import QtWidgets, QtGui, QtCore
import math

class CompassWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, compass_color="#FFFFFF"):
        super().__init__(parent)
        self.heading_angle = 0
        self.rotation_direction = 1  # 1 for clockwise, -1 for counterclockwise
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_compass)
        self.timer.start(30)  # Update interval at 30 milliseconds
        self.setFixedSize(360, 360)
        self.setContentsMargins(0, 0, 0, 0)

        # Add QLabel to display the angle and direction
        self.angle_label = QtWidgets.QLabel(self)
        self.angle_label.setStyleSheet("color: white; font-size: 24px;")
        self.angle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.update_angle_label()

        # Pre-render direction labels as images
        self.direction_images = self.create_direction_images()
        # Pre-render degree labels as images
        self.degree_images = self.create_degree_images()

    def create_direction_images(self):
        directions = ["N", "E", "S", "W"]
        images = {}
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        for direction in directions:
            image = QtGui.QImage(40, 40, QtGui.QImage.Format_ARGB32)
            image.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(image)
            painter.setFont(font)
            painter.setPen(QtGui.QPen(QtGui.QColor("#FDF34D"), 5))
            painter.drawText(image.rect(), QtCore.Qt.AlignCenter, direction)
            painter.end()
            images[direction] = image
        return images

    def create_degree_images(self):
        degrees = [30, 60, 120, 150, 210, 240, 300, 330]
        images = {}
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        for degree in degrees:
            image = QtGui.QImage(40, 40, QtGui.QImage.Format_ARGB32)
            image.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(image)
            painter.setFont(font)
            painter.setPen(QtGui.QPen(QtGui.QColor("white"), 4))
            painter.drawText(image.rect(), QtCore.Qt.AlignCenter, str(degree))
            painter.end()
            images[degree] = image
        return images

    def update_angle_label(self):
        direction = self.get_direction(self.heading_angle)
        self.angle_label.setText(f"{self.heading_angle:.1f}° {direction}")
        self.angle_label.adjustSize()
        self.angle_label.move(self.width() // 2 - self.angle_label.width() // 2, self.height() // 2 - self.angle_label.height() // 2)

    def get_direction(self, angle):
        if 337.5 <= angle < 360 or 0 <= angle < 22.5:
            return "N"
        elif 22.5 <= angle < 67.5:
            return "NE"
        elif 67.5 <= angle < 112.5:
            return "E"
        elif 112.5 <= angle < 157.5:
            return "SE"
        elif 157.5 <= angle < 202.5:
            return "S"
        elif 202.5 <= angle < 247.5:
            return "SW"
        elif 247.5 <= angle < 292.5:
            return "W"
        elif 292.5 <= angle < 337.5:
            return "NW"

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Create a clipping path with rounded corners
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), 30, 30)
        painter.setClipPath(path)

        # Fill the background with dark gray color
        painter.fillRect(self.rect(), QtGui.QColor("#151515"))

        self.draw_compass(painter)

    def draw_compass(self, painter):
        width = self.width()
        height = self.height()
        center_x = width // 2
        center_y = height // 2

        # Draw the outer ellipse
        painter.setPen(QtGui.QPen(QtGui.QColor("#555"), 5))
        painter.drawEllipse(center_x - 156, center_y - 156, 312, 312)

        # Draw the compass ellipse
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QPen(QtGui.QColor("#555"), 5))
        painter.drawEllipse(center_x - 140, center_y - 140, 280, 280)  

        # Draw tick marks (increments)
        tick_count = 36
        for i in range(tick_count):  # 36 tick marks
            angle = math.radians(i * (360 / tick_count))
            x1 = int(center_x + 115 * math.sin(angle))  
            y1 = int(center_y - 115 * math.cos(angle))  
            x2 = int(center_x + 135 * math.sin(angle)) 
            y2 = int(center_y - 135 * math.cos(angle))  
            painter.setPen(QtGui.QPen(QtGui.QColor("#D9F054"), 4))  # Bolder tick marks
            painter.drawLine(x1, y1, x2, y2)

            # Draw dots between tick marks
            next_angle = math.radians((i + 1) * (360 / tick_count))
            dot_angle = (angle + next_angle) / 2  # Position dot between tick marks
            dot_x = int(center_x + 115 * math.sin(dot_angle))  # Adjusts margin to the center
            dot_y = int(center_y - 115 * math.cos(dot_angle))  # Adjusts margin to the center
            painter.setPen(QtGui.QPen(QtGui.QColor("#D9F054"), 3))  # Dot color
            painter.setBrush(QtGui.QBrush(QtGui.QColor("#D9F054")))  # Fill color for the dots
            painter.drawEllipse(dot_x - 2, dot_y - 2, 4, 4)  # Draw small circles

        # Draw compass needle as a triangle
        painter.setBrush(QtGui.QColor("white"))
        painter.setPen(QtGui.QPen(QtGui.QColor("white"), 1))
        needle_points = [
            QtCore.QPoint(center_x, center_y - 75),
            QtCore.QPoint(center_x - 10, center_y - 55),
            QtCore.QPoint(center_x + 10, center_y - 55)
        ]
        painter.drawPolygon(QtGui.QPolygon(needle_points))

        # Draw compass directions closer to the center
        directions = ["N", "E", "S", "W"]
        for i, direction in enumerate(directions):
            angle = math.radians(i * 90 - self.heading_angle)  # Adjust angle based on heading
            x = int(center_x + 95 * math.sin(angle))  # Position relative to the center
            y = int(center_y - 95 * math.cos(angle))  # Position relative to the center
            painter.save()
            painter.translate(x, y)
            painter.rotate(i * 90 - self.heading_angle)  # Rotate to point towards the center
            painter.drawImage(-20, -20, self.direction_images[direction])  # Draw pre-rendered image
            painter.restore()

        # Draw additional degree labels
        additional_degrees = [30, 60, 120, 150, 210, 240, 300, 330]
        for degree in additional_degrees:
            angle = math.radians(degree - self.heading_angle)  # Adjust angle based on heading
            x = int(center_x + 100 * math.sin(angle))  # Position inside the compass
            y = int(center_y - 100 * math.cos(angle))  # Position inside the compass
            painter.save()
            painter.translate(x, y)
            painter.rotate(degree - self.heading_angle)  # Rotate to point towards the center
            painter.drawImage(-14, -14, self.degree_images[degree])  # Draw pre-rendered image
            painter.restore()

        # Update heading angle for demonstration
        self.heading_angle += 0.08 * self.rotation_direction  # Adjust the increment based on rotation direction
        if self.heading_angle >= 360 or self.heading_angle <= 0:
            self.rotation_direction *= -1  # Reverse the direction

        self.update_angle_label()

    def update_compass(self):
        self.update()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = CompassWidget()
    window.show()
    sys.exit(app.exec_())
