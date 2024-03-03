from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance
import os

app = QApplication([])

window = QWidget() #Створення вікна програми
window.setWindowTitle("Easy Editors")
window.resize(900, 650)

WORK_DIR = None
def shooseWorkdir(): #Функція вибору нової папки
    global WORK_DIR
    WORK_DIR = QFileDialog.getExistingDirectory()
    filesnames = os.listdir(WORK_DIR)
    filesnames = filter(filesnames, [".png", ".jpg", ".svg", ".bmp", ".jpeg"])
    showFilenamesList(filesnames)

def filter(filenames, extensions): #Функція фільтру файлів
    result = []
    for file in filenames:
        for extension in extensions:
            if file.lower().endswith(extension):
                result.append(file)
                break
    return result

def showFilenamesList(filesnames): #Функція показу списку картинок
    images_list.clear()
    images_list.addItems(filesnames)

def update_list_image(): #Функція оновлення списку картинок
    filenames = os.listdir(WORK_DIR)
    filenames = filter(filenames, [".png", ".jpg", ".svg", ".bmp", ".jpeg"])
    showFilenamesList(filenames)

def showShosenImage(): #Функція показу картинки
    image_label.hide()
    image_name = images_list.selectedItems()[0].text()
    pixmap = QPixmap(WORK_DIR + "/" + image_name)
    w, h = image_label.width(), image_label.height()
    pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
    image_label.setPixmap(pixmap)
    image_label.show()

def do_bw():
    if images_list.selectedItems():
        image_name = WORK_DIR + "/" + images_list.selectedItems()[0].text() #Отримуемо путь к картинке
        image = Image.open(image_name) #Отримуємо картинку
        new_image = image.convert("L") #Робимо картинку Ч/Б
        new_image_name = image_name.split(".")[0] + "_bw." + image.format.lower() #Отримуемо назву нової картинки
        new_image.save(new_image_name) #Зберігаємо картнику
        update_list_image() #Оновлюемо список картинок

def do_left():
    if images_list.selectedItems():
        image_name = WORK_DIR + "/" + images_list.selectedItems()[0].text()
        image = Image.open(image_name)
        new_image = image.transpose(Image.ROTATE_90)
        new_image_name = image_name.split(".")[0] + "_left." + image.format.lower()
        new_image.save(new_image_name)
        update_list_image()

def do_right():
    if images_list.selectedItems():
        image_name = WORK_DIR + "/" + images_list.selectedItems()[0].text()
        image = Image.open(image_name)
        new_image = image.transpose(Image.ROTATE_270)
        new_image_name = image_name.split(".")[0] + "_right." + image.format.lower()
        new_image.save(new_image_name)
        update_list_image()

def do_flip():
    if images_list.selectedItems():
        image_name = WORK_DIR + "/" + images_list.selectedItems()[0].text()
        image = Image.open(image_name)
        new_image = image.transpose(Image.FLIP_LEFT_RIGHT)
        new_image_name = image_name.split(".")[0] + "_flip." + image.format.lower()
        new_image.save(new_image_name)
        update_list_image()

def do_contrast():
    if images_list.selectedItems():
        image_name = WORK_DIR + "/" + images_list.selectedItems()[0].text()
        image = Image.open(image_name)
        new_image = ImageEnhance.Contrast(image)
        new_image = new_image.enhance(1.5)
        new_image_name = image_name.split(".")[0] + "_contrast." + image.format.lower()
        new_image.save(new_image_name)
        update_list_image()

#-------------------------------------Створення всіх віджетів
dir_button = QPushButton("Папка")
dir_button.clicked.connect(shooseWorkdir)

images_list = QListWidget()
images_list.itemClicked.connect(showShosenImage)
image_label = QLabel("Image")
image_hlayout = QHBoxLayout() #Прикріпляємо віджети для вибору фото на image_hlayout
image_hlayout.addWidget(images_list, alignment = Qt.AlignLeft)
image_hlayout.addWidget(image_label)

left_rbutton = QPushButton("Повернути вліво")
left_rbutton.clicked.connect(do_left)
right_rbutton = QPushButton("Повернути вправо")
right_rbutton.clicked.connect(do_right)
mirror_rbutton = QPushButton("Відобразити дзеркально")
mirror_rbutton.clicked.connect(do_flip)
contrast_rbutton = QPushButton("Збільшити різкість")
contrast_rbutton.clicked.connect(do_contrast)
blwh_rbutton = QPushButton("Зробити Ч/Б")
blwh_rbutton.clicked.connect(do_bw)
redact_hlayout = QHBoxLayout() #Прикріпляємо кнопки для редагування на redact_hlayout
redact_hlayout.addWidget(left_rbutton)
redact_hlayout.addWidget(right_rbutton)
redact_hlayout.addWidget(mirror_rbutton)
redact_hlayout.addWidget(contrast_rbutton)
redact_hlayout.addWidget(blwh_rbutton)

main_layout = QVBoxLayout() #Прикріпляємо всі віджети на main_layout
main_layout.addWidget(dir_button, alignment = Qt.AlignLeft)
main_layout.addLayout(image_hlayout)
main_layout.addLayout(redact_hlayout)


window.setLayout(main_layout) #Показуємо наше вікно
window.show()
app.exec_()
