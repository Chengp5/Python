######################################################
#TODO main file, start point of this application
#################################################




import os
import sys
sys.path.append(r'.\venv\Lib\site-packages')

from PyQt5.QtWidgets import *
import Main_window
import sentiment_classifier

class MainCode(QMainWindow, Main_window.Ui_Form):
    def __init__(self):
        QMainWindow.__init__(self)
        Main_window.Ui_Form.__init__(self)
        self.setupUi(self)
        # connect pushButton's clicked signal to function get_result
        self.pushButton.clicked.connect(self.get_result)
        # connect textEdit's clicked signal to function clear_ui
        self.textEdit.clicked.connect(self.clear_ui)

#use sentence input by user to predict and get the result
    def get_result(self):
        # text for prediction
        text=self.textEdit.toPlainText()
        # get result containing emoji and emotion
        result=sentiment_classifier.predict_text([text])
        # show emoji and emotion on ui
        self.label.setText(result['emoji'])
        self.label_2.setText(result['emotion'])
# clear text in textEdit
    def clear_ui(self):
        self.textEdit.clear()
# initialize label to think emoji
        self.label.setText('🤔')
# initialize label_2's message as emotion
        self.label_2.setText('emotion')


if __name__ == '__main__':
# initialize QTApplication
    app = QApplication(sys.argv)
# create an UI
    md = MainCode()
# show this ui
    md.show()
    sys.exit(app.exec_())
