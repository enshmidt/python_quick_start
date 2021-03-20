from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QLineEdit, QTextEdit


def on_button_clicked():
    alert = QMessageBox()
    alert.setText('You clicked the button!')
    alert.exec_()


app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
line = QLineEdit('...')
button = QPushButton('Click')
edit = QTextEdit('write here')
layout.addWidget(line)
layout.addWidget(button)
layout.addWidget(edit)
button.clicked.connect(on_button_clicked)

window.setLayout(layout)
window.show()
app.exec()
