import sqlite3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from log_in import *
from new_test import *
from registration import *
from start import *
from student_menu import *
from tester import *
from res import *
from PyQt5.QtGui import QPixmap


# from bot import send_result
def password_level(password):
    c = "0123456789"
    f1 = f2 = f3 = False
    if len(password) < 6:
        s = "Недопустимый пароль"
        return s
    elif password.isdigit():
        s = "Ненадежный пароль"
        return s
    for i in password:
        if i.isupper():
            f1 = True
        elif i.islower():
            f2 = True
        elif i in c:
            f3 = True
    if f1 * f2 * f3:
        s = "ok"
    elif f1 ^ f2 and not f3:
        s = "ok"
    else:
        s = "Слабый пароль"
    return s


"""
def check(login, password):
    cur = sqlite3.connect('users.db').cursor()
    ans = cur.execute(f'''select * from user where login="{login}" and password="{password}"''').fetchall()
    return ans


def check1(login, password, id):
    con = sqlite3.connect('Tg.db')
    cur = con.cursor()
    cur.execute("INSERT INTO tg(login, password, tg_id) VALUES(?,?,?);", [login, password, id])
    con.commit()
    return
"""


class FirstMenu(QMainWindow, Ui_start):
    def __init__(self):
        super().__init__()
        self.next_form = None
        self.setupUi(self)
        self.log_in.clicked.connect(self.log)
        self.registration.clicked.connect(self.reg)
        self.pixmap = QPixmap('my.png').scaled(300, 300)
        self.label.resize(300, 300)
        self.label.move(100, 300)
        self.label.setPixmap(self.pixmap)


    def log(self):
        self.next_form = LogIn()
        self.next_form.show()
        self.close()

    def reg(self):
        self.next_form = Registration()
        self.next_form.show()
        self.close()


class LogIn(QMainWindow, Ui_log_in):
    def __init__(self):
        super().__init__()
        self.new_form = None
        self.setupUi(self)
        self.log_in_button.clicked.connect(self.click)
        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.new_form = FirstMenu()
        self.new_form.show()
        self.close()

    def click(self):
        login = self.login.text()
        password = self.password.text()
        con = sqlite3.connect('users.db')
        cur = con.cursor()
        logins = cur.execute(f'''select login from user where id > 0''').fetchall()
        logins = list(map(lambda x: x[0], logins))
        passwords = cur.execute(f'''select password from user where login="{login}"''').fetchall()
        passwords = list(map(lambda x: x[0], passwords))
        if login not in logins or password not in passwords:
            self.statusbar.showMessage('Неправильный логин или пароль')
            self.login.setText('')
            self.password.setText('')
            return
        status = cur.execute(f'''select status from user where login="{login}"''').fetchall()[0][0]
        if status == 0:
            self.new_form = StudentMenu(login)
            self.new_form.show()
            self.close()
        if status == 1:
            self.new_form = NewTest(login)
            self.new_form.show()
            self.close()


class Registration(QMainWindow, Ui_Registration):
    def __init__(self):
        super().__init__()
        self.new_form = None
        self.setupUi(self)
        self.registration_button.clicked.connect(self.click)
        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.new_form = FirstMenu()
        self.new_form.show()
        self.close()

    def click(self):
        if self.loginEdit.text() == '' or self.password1Edit.text() == '' \
                or self.password1Edit.text() != self.password2Edit.text():
            self.statusbar.showMessage('Неправильные данные')
            self.loginEdit.setText('')
            self.password1Edit.setText('')
            self.password2Edit.setText('')
            return

        if password_level(self.password1Edit.text()) != 'ok':
            self.statusbar.showMessage(password_level(self.password1Edit.text()))
            return

        con = sqlite3.connect('users.db')
        cur = con.cursor()
        logins = cur.execute('''select login from user where id > 0''').fetchall()
        logins = list(map(lambda x: x[0], logins))
        if self.loginEdit.text() in logins:
            self.statusbar.showMessage('Такой логин уже существует')
            return
        n = 0
        if self.comboBox.currentText() == 'Учитель':
            n = 1
        cur.execute(f'''insert into user(login, password, status)
         values ("{self.loginEdit.text()}", "{self.password1Edit.text()}", {n})''')
        con.commit()
        self.new_form = LogIn()
        self.new_form.show()
        self.close()


class StudentMenu(QMainWindow, Ui_StudentMenu):
    def __init__(self, login):
        super().__init__()
        self.next_form = None
        self.new_form = None
        self.setupUi(self)
        self.login = login
        self.startTestButton.clicked.connect(self.click)
        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.new_form = LogIn()
        self.new_form.show()
        self.close()

    def click(self):
        con = sqlite3.connect('tests.db')
        cur = con.cursor()
        keys = cur.execute('''select key from test where id > 0''').fetchall()
        keys = list(map(lambda x: x[0], keys))
        if self.codeEdit.text() not in keys:
            self.statusbar.showMessage('Ключ не действителен')
            return
        s = cur.execute(f'''select t from test where key="{self.codeEdit.text()}"''').fetchall()[0][0]
        self.next_form = Tester(s, self.login, self.codeEdit.text())
        self.next_form.show()
        self.close()


class NewTest(QMainWindow, Ui_NewTest):
    def __init__(self, login):
        super().__init__()
        self.answers = []
        self.login = login
        self.setupUi(self)
        self.addAnsButton.clicked.connect(self.add)
        self.cleaButton.clicked.connect(self.clear)
        self.loadButton.clicked.connect(self.load)
        self.pushButton.clicked.connect(self.back)
        self.pushButton_2.clicked.connect(self.result)

    def result(self):

        self.next_form = Results(self.login, self.codeEdit.text())
        self.next_form.show()
        self.close()

    def back(self):
        self.next_form = LogIn()
        self.next_form.show()
        self.close()

    def add(self):
        if self.answerEdit.text() == '' or self.qwestionEdit.text() == '':
            self.statusbar.showMessage('Некорректные данные')
            self.qwestionEdit.setText('')
            self.answerEdit.setText('')
            return
        s = self.qwestionEdit.text() + ',,,,' + self.answerEdit.text()
        self.answers.append(s)
        self.qwestionEdit.setText('')
        self.answerEdit.setText('')

    def clear(self):
        self.answerEdit.setText('')
        self.qwestionEdit.setText('')

    def load(self):
        if len(self.answers) == 0:
            self.statusbar.showMessage('Нет вопросов')
            return
        if self.codeEdit.text() == '':
            self.statusbar.showMessage('Пустое поле кода теста')
            return

        con = sqlite3.connect('tests.db')
        cur = con.cursor()
        keys = cur.execute('''select key from test where id > 0''').fetchall()
        keys = list(map(lambda x: x[0], keys))
        if self.codeEdit.text() in keys:
            self.statusbar.showMessage('Ваш ключ не уникален')
            return
        self.answers = '\n'.join(self.answers)
        cur.execute(f'''insert into test(key, t, author) 
        values ("{self.codeEdit.text()}", "{self.answers}", "{self.login}")''')
        con.commit()
        self.statusbar.showMessage('Проверочная создана успешно')


class Results(QMainWindow, Ui_Res):
    def __init__(self, login, code):
        super().__init__()
        self.code = code
        self.new_form = None
        self.answers = []
        self.login = login
        self.setupUi(self)
        self.pushButton.clicked.connect(self.back)
        con = sqlite3.connect('tests.db')
        cur = con.cursor()
        res = cur.execute(f'''select results from test where author="{self.login}" and key="{self.code}"''').fetchall()
        if not res:
            self.statusbar.showMessage('результатов по такому коду не найдено')
            return
        else:
            res = res[0][0]
        f = open(f't{self.code}.txt', mode='w')
        f1 = open(f't{self.code}.txt', mode='r')
        f.write(res)
        f.close()
        res = f1.read()
        self.textBrowser.setText(res)

    def back(self):
        self.new_form = NewTest(self.login)
        self.new_form.show()
        self.close()


class Tester(QMainWindow, Ui_Tester):
    def __init__(self, test, login, key):
        super().__init__()
        self.setupUi(self)
        self.login = login
        self.key = key
        self.results = []
        # Внутри test пары вопрос ответ через \n а внутри через ,,,,
        self.test = test.split('\n')
        self.test = list(map(lambda x: x.split(',,,,'), self.test))
        self.user_answers = ['' for _ in range(len(self.test))]
        self.saveButton.clicked.connect(self.save)
        self.previewButton.clicked.connect(self.preview)
        self.nextButton.clicked.connect(self.next)
        self.endButton.clicked.connect(self.end)
        self.current_qwe = 0
        self.qwestionText.setText(self.test[self.current_qwe][0])
        self.max_qwe = len(self.test) - 1
        self.pushButton.clicked.connect(self.back)

    def back(self):
        self.next_form = StudentMenu(self.login)
        self.next_form.show()
        self.close()

    def save(self):
        self.user_answers[self.current_qwe] = self.answerEdit.text()

    def preview(self):
        if self.current_qwe == 0:
            self.statusbar.showMessage('Некорректный запрос')
            return
        self.current_qwe = self.current_qwe - 1
        self.qwestionText.setText(self.test[self.current_qwe][0])

    def next(self):
        if self.current_qwe + 1 > self.max_qwe:
            self.statusbar.showMessage('Некорректный запрос')
            return
        self.current_qwe = self.current_qwe + 1
        self.qwestionText.setText(self.test[self.current_qwe][0])
        self.answerEdit.setText('')

    def end(self):
        con = sqlite3.connect('tests.db')
        cur = con.cursor()
        logins = cur.execute(f'''select logins from test where key="{self.key}"''').fetchall()[0][0]
        if logins is not None:
            if self.login in logins.split('\n'):
                self.statusbar.showMessage('Вы уже выполнили тестирование')
                return
        for i in range(self.max_qwe + 1):
            if self.user_answers[i] == self.test[i][1]:
                self.results.append(True)
            else:
                self.results.append(False)
        res = self.login + '; ' + str(self.results.count(True)) + ' из ' + str(len(self.results))
        con = sqlite3.connect('tests.db')
        cur = con.cursor()
        pre = cur.execute(f'''select results from test where key="{self.key}"''').fetchall()[0][0]
        if pre is None:
            pre = res + '\n'
        else:
            pre += res + '\n'
        cur.execute(f'''update test
        set results="{pre}"
        where key="{self.key}"''')
        con.commit()
        pre = cur.execute(f'''select logins from test where key="{self.key}"''').fetchall()[0][0]
        if pre is None:
            pre = self.login + '\n'
        else:
            pre += self.login + '\n'
        cur.execute(f'''update test
        set logins="{pre}"
        where key="{self.key}"''')
        con.commit()
        self.statusbar.showMessage('Ваш ответ записан')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstMenu()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
