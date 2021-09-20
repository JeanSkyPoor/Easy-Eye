import sys
import os.path
from form import *
from time import sleep
import pytesseract
from PIL import ImageGrab
from numpy import savetxt, array
from datetime import datetime, time
import threading
from re import sub
from cv2 import imshow, waitKey, cvtColor, COLOR_BGR2RGB
from PyQt5.QtWidgets import QMessageBox
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


def thread(my_func):
    """
    Запускает функцию в отдельном потоке
    """
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper

@thread
def show_img(new_img):
    imshow('fragment', new_img)
    waitKey(0)

class MyWin(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self, parent=None)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.check_for_test)
        self.ui.pushButton_2.clicked.connect(self.check_for_record)
        self.ui.pushButton_3.clicked.connect(self.stopClicked)
        self.stop = False

    
        
    def stopClicked(self):
        """
        Функция для смены флага на True при нажатии на кнопку СТОП
        """
        self.stop = True
    


    def check_for_test(self):
        """
        Проверяет правильность введенных данных и запускает функцию self.test
        """
        left = self.ui.lineEdit_2.text().strip()
        if len(left)==0:
            return QMessageBox.about(self, "Ошибка", "Заполните поля координат")
        if left.isdigit() == True:
            left = int(left)
        else:
            return QMessageBox.about(self, "Ошибка", "Введите координаты в числовом формате")

        top = self.ui.lineEdit_3.text().strip()
        if len(top)==0:
            return QMessageBox.about(self, "Ошибка", "Заполните поля координат")
        if top.isdigit() == True:
            top = int(top)
        else:
            return QMessageBox.about(self, "Ошибка", "Введите координаты в числовом формате")

        right = self.ui.lineEdit_4.text().strip()
        if len(right)==0:
            return QMessageBox.about(self, "Ошибка", "Заполните поля координат")
        if right.isdigit() == True:
            right = int(right)
        else:
            return QMessageBox.about(self, "Ошибка", "Введите координаты в числовом формате")

        down = self.ui.lineEdit_5.text().strip()
        if len(down)==0:
            return QMessageBox.about(self, "Ошибка", "Заполните поля координат")
        if down.isdigit() == True:
            down = int(down)
        else:
            return QMessageBox.about(self, "Ошибка", "Введите координаты в числовом формате")

        if right <= left:
            return QMessageBox.about(self, "Ошибка", "Значения координат правого угла (первое поле) должны быть больше, чем у левого угла (первое поле)")
        if down <= top:
            return QMessageBox.about(self, "Ошибка", "Значения координат правого угла (второе поле) должны быть больше, чем у левого угла (второе поле)")

        first_to_drop = self.ui.lineEdit_7.text().strip() or str(0)
        if first_to_drop.isdigit() == True:
            first_to_drop = int(first_to_drop)
        else:
            return QMessageBox.about(self, "Ошибка", " Вводимые в поле 'В начале' данные не числового формата") 

        second_to_drop = self.ui.lineEdit_8.text().strip() or str(0)
        if second_to_drop.isdigit() == True:
            second_to_drop = int(second_to_drop)
        else:
            return QMessageBox.about(self, "Ошибка", " Вводимые в поле 'В конце' данные не числового формата") 

        self.test(left, top, right, down, first_to_drop, second_to_drop)

    

    @thread
    def test(self, left, top, right, down, first_to_drop, second_to_drop):
        """
        Проводит тестирование заданных координат, открывает вырезанный кусок изображения и выводит информацию о полученных
        данных на главный интерфейс в поле "Результаты теста"
        """
        self.ui.label_13.setText("В процессе")
        sleep(5)

        # Вырезка изображения, его открытие в отдельном окне и вывод на форму результата работы pytesseract

        img = ImageGrab.grab(
            bbox=(left, top, right, down), all_screens=True)
        new_img = array(img)
        new_img = cvtColor(new_img, COLOR_BGR2RGB)
        show_img(new_img)

        data = pytesseract.image_to_string(img)
        data = sub(r'[\x00-\x1f]+', '', data)
        result = data[first_to_drop:len(data)-second_to_drop:]
        self.ui.label_11.setText(result)
        self.ui.label_13.setText("")
        
    def check_for_record(self):
        left = self.ui.lineEdit_2.text().strip()
        if len(left)==0:
            return QMessageBox.about(self, "Ошибка", "Заполните поля координат")
        if left.isdigit() == True:
            left = int(left)
        else:
            return QMessageBox.about(self, "Ошибка", "Введите координаты в числовом формате")

        top = self.ui.lineEdit_3.text().strip()
        if len(top)==0:
            return QMessageBox.about(self, "Ошибка", "Заполните поля координат")
        if top.isdigit() == True:
            top = int(top)
        else:
            return QMessageBox.about(self, "Ошибка", "Введите координаты в числовом формате")

        right = self.ui.lineEdit_4.text().strip()
        if len(right)==0:
            return QMessageBox.about(self, "Ошибка", "Заполните поля координат")
        if right.isdigit() == True:
            right = int(right)
        else:
            return QMessageBox.about(self, "Ошибка", "Введите координаты в числовом формате")

        down = self.ui.lineEdit_5.text().strip()
        if len(down)==0:
            return QMessageBox.about(self, "Ошибка", "Заполните поля координат")
        if down.isdigit() == True:
            down = int(down)
        else:
            return QMessageBox.about(self, "Ошибка", "Введите координаты в числовом формате")

        if right <= left:
            return QMessageBox.about(self, "Ошибка", "Значения координат правого угла (первое поле) должны быть больше, чем у левого угла (первое поле)")
        if down <= top:
            return QMessageBox.about(self, "Ошибка", "Значения координат правого угла (второе поле) должны быть больше, чем у левого угла (второе поле)")

        first_to_drop = self.ui.lineEdit_7.text().strip() or str(0)
        if first_to_drop.isdigit() == True:
            first_to_drop = int(first_to_drop)
        else:
            return QMessageBox.about(self, "Ошибка", " Вводимые в поле 'В начале' данные не числового формата") 

        second_to_drop = self.ui.lineEdit_8.text().strip() or str(0)
        if second_to_drop.isdigit() == True:
            second_to_drop = int(second_to_drop)
        else:
            return QMessageBox.about(self, "Ошибка", "Вводимые в поле 'В конце' данные не числового формата") 

        time_to_sleep = self.ui.lineEdit_6.text().strip()
        if time_to_sleep.isdigit()==True:
            time_to_sleep = int(time_to_sleep)
        else:
            return QMessageBox.about(self, "Ошибка", "Частота записей должна быть целым числом больше 0")            

        name = self.ui.lineEdit.text() or None
        if name == None:
            return QMessageBox.about(self, "Ошибка", "Введите имя будущего файла")
        if os.path.isdir('Records') is False:
            os.mkdir('Records')
        if os.path.exists('.\Records\{}.csv'.format(name)):
            return QMessageBox.about(self, "Ошибка", "Файл с именем '{}' уже существует, введите другое.".format(name))

        self.record(left, top, right, down, first_to_drop,second_to_drop, time_to_sleep, name)  

    @thread
    def record(self, left, top, right, down, first_to_drop, second_to_drop, time_to_sleep, name):
        """
        Инициализация параметров, вырезка изображения,
        его обработка и запись в CSV файл в случае нажатия клавиши СТОП
        """
        self.stop = False
        times = 1
        list_data = [['Время записи', 'Значения']]
        self.ui.label_13.setText('В процессе')
        # Пока не будет нажата кнопка СТОП, цикл будет записывать данные

        while True:
            times += 1
            img = ImageGrab.grab(
                bbox=(int(left), int(top), int(right), int(down)), all_screens=True)
            data = pytesseract.image_to_string(img)
            data = sub(r'[\x00-\x1f]+', '', data)
            result = data[int(first_to_drop):len(
                data)-int(second_to_drop):]
            list_data.append([datetime.now().strftime("%H:%M:%S"), result])
            sleep(int(time_to_sleep))
            self.ui.label_13.setText('Запишется {} записей'.format(times))
            # При нажатии кнопки СТОП флаг меняется, записываются данные и цикл останавливается
            if self.stop:
                self.stop = False
                savetxt(".\Records\{}.csv".format(name), list_data,
                        delimiter=";",  fmt='% s')
                self.ui.label_13.setText('Файл сохранен')
                break

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())