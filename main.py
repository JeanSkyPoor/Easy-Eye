import sys
from form import *
from secondary_functions import *
import pytesseract
import threading
from form import *
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


class MyWin(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.test_run)
        self.ui.pushButton_2.clicked.connect(self.record)
        self.ui.pushButton_3.clicked.connect(self.set_event)
        self.exit_event = threading.Event()

    def set_event(self):
        """
        Устанавливает Threading.Event в позицию Set у класса myapp(MyWin)
        """

        self.exit_event.set()

    def test_run(self):
        """
        Запускается при нажатии на кнопку СТАРТ. 
        """
        #Обновление данных с формы 
        coordinate_initialization(myapp)
        cut_initialization(myapp)
        
        # Проверка на возможные ошибки и остановка выполнения, если ошибки были
        error_data_coordinate = check_correct_input_coordinate(myapp)
        if type(error_data_coordinate) != type(None):
            return sent_error(myapp, error_data_coordinate)

        error_data_cut = check_correct_input_cut(myapp)

        if type(error_data_cut) != type(None):
            return sent_error(myapp, error_data_cut)        

        convert_data(myapp, flag = 0)
       
        # Пробный ран
        test(myapp)
    
    def record(self):
        """
        Запускается при нажатии кнопки СТАРТ
        """
        #Обновление данных с формы 
        coordinate_initialization(myapp)
        cut_initialization(myapp)
        name_and_time_initialization(myapp)

        # Проверка на возможные ошибки и остановка выполнения, если ошибки были
        error_data_coordinate = check_correct_input_coordinate(myapp)
        if type(error_data_coordinate) != type(None):
            return sent_error(myapp, error_data_coordinate)

        error_data_cut = check_correct_input_cut(myapp)

        if type(error_data_cut) != type(None):
            return sent_error(myapp, error_data_cut)

        error_data_name_and_time = check_for_correct_name_and_time(myapp)
        if type(error_data_name_and_time) != type(None):
            return sent_error(myapp, error_data_name_and_time)

        # Конвертация аргументов класса
        convert_data(myapp, flag = 1)

        # Считывание и запись
        record(myapp)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())