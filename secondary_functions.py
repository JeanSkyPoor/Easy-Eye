import os
from time import sleep
import pytesseract
from PIL import ImageGrab
from numpy import savetxt, array
from datetime import datetime
import threading
from re import sub
from cv2 import imshow, waitKey, cvtColor, COLOR_BGR2RGB
from PyQt5.QtWidgets import QMessageBox

def thread(my_func):
    """
    Запускает функцию в отдельном потоке
    """
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()
    return wrapper

def image_grab(myapp):
    """
    Делает скриншот по указанным координатам, переводит цветовые каналы к RGB и возвращает изображение
    """
    img = ImageGrab.grab(bbox = (myapp.left, myapp.top, myapp.right, myapp.down), all_screens = True)
    img = array(img)
    img  = cvtColor(img, COLOR_BGR2RGB)
    return img

def show_img(new_img):
    """
    Открывает вырезанный фрагмент изображения в новом окне и ждет, пока его закроют
    """
    imshow('fragment', new_img)
    waitKey(0)

def sent_error(myapp, error_data):
    """
    Отправляет ошибку, где первый аргумент - тайтл, а второй - описание ошибки. Если возвращается None, ошибку не отправляет
    """
    QMessageBox.about(myapp, error_data[0], error_data[1])

def convert_data(myapp, flag):
    """
    Переводит данные к типу int, если флаг равен 1, можно применить к Record
    """
    myapp.left = int(myapp.left)
    myapp.top = int(myapp.top)
    myapp.right = int(myapp.right)
    myapp.down = int(myapp.down)
    myapp.first_to_drop = int(myapp.first_to_drop)
    myapp.second_to_drop = int(myapp.second_to_drop)
    if flag == 1:
        myapp.time_to_sleep = int(myapp.time_to_sleep)

def check_correct_input_coordinate(myapp):
    """
    Проверяет корректность введеных данных координат от пользователя. В случае ошибки возвращает тег "Ошибка" и описание ошибки
    """
    if len(myapp.left) == 0:
        return 'Ошибка', 'Заполните поля координат'
    if myapp.left.isdigit() == False:
        return 'Ошибка', 'Введите координаты в числовом формате'

    if len(myapp.top) == 0:
        return 'Ошибка', 'Заполните поля координат'
    if myapp.top.isdigit() == False:
        return 'Ошибка', 'Введите координаты в числовом формате'

    if len(myapp.right) == 0:
        return 'Ошибка', 'Заполните поля координат'
    if myapp.right.isdigit() == False:
        return 'Ошибка', 'Введите координаты в числовом формате'

    if len(myapp.down) == 0:
        return 'Ошибка', 'Заполните поля координат'
    if myapp.down.isdigit() == False:
        return  'Ошибка', 'Введите координаты в числовом формате'

    if myapp.right <= myapp.left:
        return "Ошибка", "Значения координат правого угла (первое поле) должны быть больше, чем у левого угла (первое поле)"
    if myapp.down <= myapp.top:
        return "Ошибка", "Значения координат правого угла (второе поле) должны быть больше, чем у левого угла (второе поле)"

def coordinate_initialization(myapp):
    """
    Обновляет координаты у класса myapp(MyWin)
    """
    myapp.left = myapp.ui.lineEdit_2.text().strip()
    myapp.top = myapp.ui.lineEdit_3.text().strip()
    myapp.right = myapp.ui.lineEdit_4.text().strip()
    myapp.down = myapp.ui.lineEdit_5.text().strip()

def cut_initialization(myapp):
    """
    Обновляет first_to_drop и second_to_drop у класса myapp(MyWin)
    """
    myapp.first_to_drop = myapp.ui.lineEdit_7.text().strip() or str(0)
    myapp.second_to_drop = myapp.ui.lineEdit_8.text().strip() or str(0)

def name_and_time_initialization(myapp):
    """
    Обновляет file_name и time_to_sleep у класса myapp(MyWin)
    """
    myapp.file_name = myapp.ui.lineEdit.text() or None
    myapp.time_to_sleep = myapp.ui.lineEdit_6.text().strip()

def check_correct_input_cut(myapp):
    """
    Проверяет корректность введеных данных в поле "Удаление лишних символов". В случае ошибки возвращает тег "Ошибка" и описание ошибки
    """
    if myapp.first_to_drop.isdigit() != True:
        return  "Ошибка", "Вводимые в поле 'В начале' данные не числового формата"

    if myapp.second_to_drop.isdigit() != True:
        return  "Ошибка", "Вводимые в поле 'В конце' данные не числового формата"

def reading_data(img, myapp):
    """
    Считывает данные с вырезанного изображения и возвращает результат работы pytesseract'a
    """
    data = pytesseract.image_to_string(img)
    data = sub(r'[\x00-\x1f]+', '', data)
    result = data[myapp.first_to_drop : len(data) - myapp.second_to_drop :]
    return result
    
@thread   
def test(myapp):
    """
    Проводит тестовый ран. Вырезает из скриншота по координатам изображение, считывает его, выводит сам фрагмент и 
    выводит в поле результата результат
    """
    myapp.ui.label_13.setText('В процессе')
    sleep(5)
    img = image_grab(myapp)
    data = reading_data(img, myapp)
    myapp.ui.label_11.setText(data)
    myapp.ui.label_13.setText('')
    show_img(img)

def check_for_correct_name_and_time(myapp):
    """
    Проверяет имя файла и заданное время сна у класса myapp(MyWin)
    """
    if myapp.file_name == None:
        return "Ошибка", "Введите имя будущего файла"

    if os.path.isdir('Records') is False:
        os.mkdir('Records')

    if os.path.exists('.\Records\{}.csv'.format(myapp.file_name)):
        return "Ошибка", "Файл с именем '{}' уже существует, введите другое.".format(myapp.file_name)

    if myapp.time_to_sleep.isdigit() != True:
        return "Ошибка", "Частота записей должна быть целым числом больше 0"

def create_file(myapp, list_data):
    """
    Сохраняет вложенный список в виде CSV файла с определенным названием
    """
    savetxt(".\Records\{}.csv".format(myapp.file_name), list_data,
                    delimiter=";",  fmt='% s')

@thread
def record(myapp):
    """
    Проводит считывание и запись данных в лист с фрагмента изображения
    """
    myapp.ui.label_13.setText('В процессе')
    sleep(5)
    myapp.exit_event = threading.Event()
    times = 0
    list_data = [['Время записи', 'Значения']]
    # Пока не будет нажата кнопка СТОП, цикл будет записывать данные
    while myapp.exit_event.is_set() is False:
        times += 1
        img = image_grab(myapp)
        data = reading_data(img, myapp)
        list_data.append([datetime.now().strftime("%H:%M:%S"), data])
        myapp.ui.label_13.setText('Запишется {} записей'.format(times))
        if myapp.exit_event.is_set():
            break
        else:
            for i in range(myapp.time_to_sleep):
                sleep(1)
                if myapp.exit_event.is_set():
                    break
    create_file(myapp, list_data)
    myapp.ui.label_13.setText('Файл сохранен')
        
    
        
              
        
