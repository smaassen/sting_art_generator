from PySide2.QtCore import QSize, Qt, QRect, QPoint, QLine
from PySide2.QtWidgets import QApplication, QMainWindow, QFormLayout, QLabel, QLineEdit, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PySide2.QtGui import QPalette, QColor, QIntValidator, QDoubleValidator, QPixmap, QPainter, QPen, QVector2D

# Only needed for access to command line arguments
import sys

MW_WIDTH = 2000
MW_HEIGHT = 1200

SCALE = 400.0  # pixels / meter


def metersToPixels(v: float) -> int:
    return int(v * SCALE)


def pixelsToMeters(v: int):
    return v / SCALE


class ParameterInput(QWidget):

    def __init__(self, name):
        super(ParameterInput, self).__init__()

        self.layout = QHBoxLayout()
        self.label = QLabel(name)

        self.input = QLineEdit()
        self.input.setMaxLength(10)
        self.input.setPlaceholderText("Height of the Canvas")

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)

        self.setLayout(self.layout)

    def return_pressed(self):
        print("Return pressed!")
        self.centralWidget().setText("BOOM!")

    def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())

    def text_changed(self, s):
        print("Text changed...")
        print(s)

    def text_edited(self, s):
        print("Text edited...")
        print(s)


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):

    def __init__(self):
        # super(MainWindow, self).__init__()

        # self.setWindowTitle("My App")

        # layout = QVBoxLayout()

        # layout.addWidget(Color('red'))
        # layout.addWidget(Color('green'))
        # layout.addWidget(Color('blue'))

        # widget = QWidget()
        # widget.setLayout(layout)
        # self.setCentralWidget(widget)
        super(MainWindow, self).__init__()

        self.setWindowTitle("Amazing String Creator")

        self.setFixedSize(QSize(MW_WIDTH, MW_HEIGHT))

        # Inputs
        self.layoutInput = QFormLayout()

        self.labelHeightCanvas = QLabel("Height Canvas [m]")
        self.inputHeightCanvas = QLineEdit("1.0")
        self.inputHeightCanvas.setValidator(QDoubleValidator(0.0, 10.0, 2))
        self.labelWidthCanvas = QLabel("Width Canvas [m]")
        self.inputWidthCanvas = QLineEdit("2.0")
        self.inputWidthCanvas.setValidator(QDoubleValidator(0.0, 10.0, 2))
        self.labelNumberNailsHeight = QLabel("Number of Nails in Height")
        self.inputNumberNailsHeight = QLineEdit("50")
        self.inputNumberNailsHeight.setValidator(QIntValidator(0, 10000))
        self.labelNumberNailsWidth = QLabel("Number of Nails in Width")
        self.inputNumberNailsWidth = QLineEdit("50")
        self.inputNumberNailsWidth.setValidator(QIntValidator(0, 10000))

        self.layoutInput.addRow(self.labelHeightCanvas, self.inputHeightCanvas)
        self.layoutInput.addRow(self.labelWidthCanvas, self.inputWidthCanvas)
        self.layoutInput.addRow(self.labelNumberNailsHeight,
                                self.inputNumberNailsHeight)
        self.layoutInput.addRow(self.labelNumberNailsWidth,
                                self.inputNumberNailsWidth)

        # Actions
        self.layoutGenerate = QHBoxLayout()
        self.buttonGenerateNails = QPushButton("Generate Nails")
        self.buttonGenerateNails.clicked.connect(self.generate_nails)
        self.buttonGenerateStrings = QPushButton("Generate Strings")
        self.buttonGenerateStrings.clicked.connect(self.generate_strings)
        self.layoutGenerate.addWidget(self.buttonGenerateNails)
        self.layoutGenerate.addWidget(self.buttonGenerateStrings)

        # Output
        self.layoutOutput = QVBoxLayout()
        self.layoutOutput.addWidget(Color("blue"))

        # Canvas
        self.layoutVisualizer = QVBoxLayout()
        self.canvas = QPixmap(round(MW_WIDTH * 2 / 3), round(MW_HEIGHT))
        self.canvas.fill(Qt.white)
        self.labelCanvas = QLabel()
        self.labelCanvas.setPixmap(self.canvas)
        self.layoutVisualizer.addWidget(self.labelCanvas)

        self.canvasCenter = [
            int(self.canvas.height() / 2),
            int(self.canvas.width() / 2)
        ]

        # main layout
        self.layoutMain = QHBoxLayout()

        self.layoutInterface = QVBoxLayout()

        self.layoutInterface.addLayout(self.layoutInput)
        self.layoutInterface.addLayout(self.layoutGenerate)
        self.layoutInterface.addLayout(self.layoutOutput)

        self.layoutMain.addLayout(self.layoutInterface, 1)
        self.layoutMain.addLayout(self.layoutVisualizer, 2)

        widget = QWidget()
        widget.setLayout(self.layoutMain)

        # Set the central widget of the Window.
        self.setCentralWidget(widget)

    def generate_nails(self):
        print("Generating Canvas")
        painter = QPainter(self.labelCanvas.pixmap())
        painter.eraseRect(0, 0, self.canvas.width(), self.canvas.height())

        pen = QPen()
        pen.setWidth(1)
        pen.setColor(Qt.black)
        painter.setPen(pen)

        self.frame_width = float(self.inputWidthCanvas.text())
        self.frame_height = float(self.inputHeightCanvas.text())

        self.frame_width_px = metersToPixels(self.frame_width)
        self.frame_height_px = metersToPixels(self.frame_height)

        rect = QRect(int((self.canvasCenter[0] - self.frame_width_px / 2)),
                     int((self.canvasCenter[1] - self.frame_height_px / 2)),
                     int(self.frame_width_px), int(self.frame_height_px))
        painter.drawRect(rect)

        self.nails_px = []
        nail_border = 0.05  # TODO Make parameter
        nail_border_px = metersToPixels(nail_border)
        nail_top_left_px = QVector2D(rect.topLeft().x() + nail_border_px,
                                     rect.topLeft().y() + nail_border_px)
        nail_top_right_px = QVector2D(rect.topRight().x() - nail_border_px,
                                      rect.topRight().y() + nail_border_px)
        nail_bottom_left_px = QVector2D(rect.bottomLeft().x() + nail_border_px,
                                        rect.bottomLeft().y() - nail_border_px)
        nail_bottom_right_px = QVector2D(
            rect.bottomRight().x() - nail_border_px,
            rect.bottomRight().y() - nail_border_px)

        self.n_nails_x = int(self.inputNumberNailsWidth.text())
        self.n_nails_y = int(self.inputNumberNailsHeight.text())

        pitch_x_px = (nail_bottom_right_px -
                      nail_bottom_left_px).length() / (self.n_nails_x - 1)
        pitch_y_px = (nail_top_right_px -
                      nail_bottom_right_px).length() / (self.n_nails_y - 1)
        for i in range(0, self.n_nails_x):
            self.nails_px.append(nail_top_left_px +
                                 i * QVector2D(pitch_x_px, 0))
        for i in range(0, self.n_nails_y):
            self.nails_px.append(nail_top_right_px +
                                 i * QVector2D(0, pitch_y_px))
        for i in range(0, self.n_nails_x):
            self.nails_px.append(nail_bottom_right_px +
                                 i * QVector2D(-pitch_x_px, 0))
        for i in range(0, self.n_nails_y):
            self.nails_px.append(nail_bottom_left_px +
                                 i * QVector2D(0, -pitch_y_px))
        self.n_nails = len(self.nails_px)

        # print("Generating nails")
        # self.nail_coordinates=[]
        # for i in range(0,self.inp)
        pen.setColor(Qt.red)
        painter.drawPoints([QPoint(p.x(), p.y()) for p in self.nails_px])
        painter.end()
        self.update()

    def generate_strings(self):
        print("Generating Stings")
        painter = QPainter(self.labelCanvas.pixmap())

        pen = QPen()
        pen.setWidth(1)
        pen.setColor(Qt.red)
        painter.setPen(pen)

        # TODO Think about how this can be changed by the user
        for i in range(0, self.n_nails_x):
            p1 = QPoint(self.nails_px[i].x(), self.nails_px[i].y())
            p2 = QPoint(self.nails_px[i + self.n_nails_x].x(),
                        self.nails_px[i + self.n_nails_x].y())
            line = QLine(p1, p2)
            painter.drawLine(line)

        pen = QPen()
        pen.setWidth(1)
        pen.setColor(Qt.blue)
        painter.setPen(pen)

        # TODO Think about how this can be changed by the user
        for i in range(self.n_nails_x, self.n_nails_x + self.n_nails_y):
            p1 = QPoint(self.nails_px[i].x(), self.nails_px[i].y())
            p2 = QPoint(self.nails_px[i + self.n_nails_y].x(),
                        self.nails_px[i + self.n_nails_y].y())
            line = QLine(p1, p2)
            painter.drawLine(line)

        painter.end()
        self.update()


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec_()

# Your application won't reach here until you exit and the event
# loop has stopped.