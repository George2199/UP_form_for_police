import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt


class CustomLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            font-size: 36px;
            color: white;
            padding: 10px;
            font-family: "Comic Sans MS", "Comic Sans";
        """)


class MyForm(QWidget):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle('Система "ГАИ"')

        # Создаем поля для ввода и кнопку
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText('Логин')
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Пароль')
        
        button = QPushButton('Войти', self)
        button.setCheckable(True)
        button.clicked.connect(self.try_enter)

        self.button_reg = QPushButton('Зарегистрироваться')

        # Создаем макет и добавляем в него элементы
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.login_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(button)
        self.layout.addWidget(self.button_reg)

        # Создаем контейнер для фона
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.container.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 10px;
            font-family: "Comic Sans MS", "Comic Sans"
        """)
        self.container.setFixedSize(400, 300)

        self.title = QLabel()
        self.title.setText('Система "ГАИ"')

        self.copyright = QLabel()
        self.copyright.setText('C ИЦ "Пино4ет"')

        # Основной макет
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.container)
        self.main_layout.setAlignment(Qt.AlignCenter)

        # Устанавливаем основной макет для окна
        self.setLayout(self.main_layout)
        
        # Устанавливаем стили для основного окна и полей ввода
        self.setStyleSheet("""
            background-color: #0000FF;
        """)
        self.login_input.setStyleSheet("""
            background-color: rgba(255, 0, 0, 0.1);
            padding: 10px;
            font-size: 16px;
        """)
        self.password_input.setStyleSheet("""
            background-color: rgba(255, 0, 0, 0.1);
            padding: 10px;
            font-size: 16px;                   
        """)
        self.title.setStyleSheet("""
            font-size: 42px;
            color: rgba(122, 163, 200);
            text-align: center;
        """)
        button.setStyleSheet("""
            background-color: #6351D3;
            color: #FFFFFF;
            padding: 10px;
            font-family: "Comic Sans MS", "Comic Sans";
            font-size: 24px;
        """)

        self.button_reg.setStyleSheet("""
            padding: 10px;
            font-family: "Comic Sans MS", "Comic Sans";
            font-size: 16px;
        """)

    def enter(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

    def try_enter(self):
        login = self.login_input.text()
        password = self.password_input.text()

        correct_login = "2"
        correct_password = "2"

        if login == correct_login and password == correct_password:
            self.enter()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")


class BarChart(QGraphicsView):
    def __init__(self, data):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.create_bars(data)

    def create_bars(self, data):
        max_value = max(data.values())
        bar_height = 30
        spacing = 10

        dct = {
                0: Qt.white,
                1: Qt.blue,
                2: Qt.red}
        for i, (label, value) in enumerate(data.items()):
            bar_length = (value / max_value) * 100  # 400 - максимальная длина полосы
            rect = QGraphicsRectItem(0, i * (bar_height + spacing), bar_length, bar_height)
            rect.setBrush(dct[i])
            self.scene.addItem(rect)

            text_item = QGraphicsTextItem(label)
            text_item.setPos(bar_length + 5, i * (bar_height + spacing))
            self.scene.addItem(text_item)

        self.scene.setSceneRect(0, 0, 500, len(data) * (bar_height + spacing))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Система "ГАИ"')
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Создаем вертикальный layout для меток
        stats_layout = QVBoxLayout()
        n_closed_keys = 40
        mean_time_case_close = 3

        closed_cases_label = CustomLabel(f'Количество закрытых дел: {n_closed_keys}', self)
        mean_time_case_label = CustomLabel(f'Среднее время закрытия дела: {mean_time_case_close}', self)
        case_types = CustomLabel(f'Типы дел: ', self)

        stats_layout.addWidget(closed_cases_label)
        stats_layout.addWidget(mean_time_case_label)
        stats_layout.addWidget(case_types)
        layout.addLayout(stats_layout)
        layout.setAlignment(Qt.AlignTop)

        # Данные для графика
        data = {
            'Аварии': 10,
            'Превышения скорости': 18,
            'Нарушения разметки': 20,
        }

        # Добавляем график
        self.bar_chart = BarChart(data)
        self.bar_chart.setAlignment(Qt.AlignTop)
        layout.addWidget(self.bar_chart)
        self.setStyleSheet('''
            background-color: #0000FF;
        ''')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyForm()
    window.show()
    app.exec_()
