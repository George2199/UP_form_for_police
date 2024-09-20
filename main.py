import sys
import pyodbc
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem, QHBoxLayout, QTableWidgetItem, QTableWidget
from PyQt5.QtCore import Qt
from datetime import datetime
from PyQt5.QtGui import QColor, QFont

CONNECTION_STRING = 'DRIVER={SQL Server};SERVER=ADCLG1;DATABASE=Денисов_УП;UID=;PWD='

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

    def try_enter(self, db):
        login = self.login_input.text()
        password = self.password_input.text()

        db_users = self.load_data('users')

        entered = False
        for row in db_users:
            if login == row['login'] and password == row['password']:
                self.enter()
                entered = True
                break
            else:
                continue
        if not entered:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
            
    def load_data(self, table_name):
        # Подключение к базе данных
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Запрос данных из таблицы Cases
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Получение названий столбцов
        column_names = [column[0] for column in cursor.description]

        # Создание списка словарей из данных
        data_dicts = []
        for row in rows:
            data_dict = {column_names[col_idx]: row[col_idx] for col_idx in range(len(column_names))}
            data_dicts.append(data_dict)

        # Закрытие подключения
        cursor.close()
        conn.close()

        # Возврат списка словарей
        return data_dicts


class BarChart(QGraphicsView):
    def __init__(self, data):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.create_bars(data)
        self.setAlignment(Qt.AlignTop)

    def create_bars(self, data):
        max_value = max(data.values())
        bar_height = 30
        spacing = 10

        dct = {
                0: Qt.white,
                1: QColor(99, 81, 211),
                2: Qt.red}
        for i, (label, value) in enumerate(data.items()):
            bar_length = (value / max_value) * 400  # максимальная длина полосы
            rect = QGraphicsRectItem(0, i * (bar_height + spacing), bar_length, bar_height)
            rect.setBrush(dct[i])
            self.scene.addItem(rect)

            text_item = QGraphicsTextItem(label)
            text_item.setPos(bar_length + 5, i * (bar_height + spacing))
            
            # Установка стиля текста
            text_item.setDefaultTextColor(Qt.white)  # Цвет текста
            text_item.setFont(QFont("Comic Sans MS", 16))  # Шрифт и размер текста
            
            self.scene.addItem(text_item)

        self.scene.setSceneRect(0, 0, 500, len(data) * (bar_height + spacing))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Система "ГАИ"')
        top_widget = QWidget()
        self.setCentralWidget(top_widget)

        self.table_widget = QTableWidget()
        db_cases = self.load_data('Cases', True)
        db_viols = self.load_data('Violations', False)

        print(db_viols)
        # Главный горизонтальный макет
        main_layout = QHBoxLayout(top_widget)
    
        summ_date_diff = 0
        values = {}
        for i in db_cases:
            id = db_viols[i['violation_id'] - 1]['violation_type']
            if id in values.keys():
                values[id] += 1
            else:
                values[id] = 1
            diff = datetime.strptime(i['close_date'], '%Y-%m-%d') - datetime.strptime(i['open_date'], '%Y-%m-%d')
            summ_date_diff += diff.days

        # Левый вертикальный макет для статистики
        stats_layout = QVBoxLayout()
        n_closed_keys = len(db_cases)
        mean_time_case_close = summ_date_diff / len(db_cases)

        closed_cases_label = CustomLabel(f'Количество закрытых дел: {n_closed_keys}', self)
        mean_time_case_label = CustomLabel(f'Среднее время закрытия дела: {mean_time_case_close} дней', self)
        case_types = CustomLabel(f'Типы дел: ', self)

        stats_layout.addWidget(closed_cases_label)
        stats_layout.addWidget(mean_time_case_label)
        stats_layout.addWidget(case_types)


        
        nums = values
        data = {}

        for i in range(3):
            if len(nums) <= 0:
                break
            ma = (max(values, key=nums.get))
            data[ma + f', {nums[ma]}'] = nums[ma]
            nums.pop(max(nums, key=nums.get), 3000)

        # Добавляем график
        self.bar_chart = BarChart(data)
        stats_layout.addWidget(self.bar_chart)
        stats_layout.setAlignment(Qt.AlignTop)

        # Добавляем stats_layout в левую часть главного макета
        main_layout.addLayout(stats_layout)

        # Правый вертикальный макет для поиска
        search_layout = QVBoxLayout()

        search = QLineEdit(self)
        search.setPlaceholderText("Поиск")

        search_layout.addWidget(search)
        search_layout.addWidget(self.table_widget)
        search_layout.setAlignment(Qt.AlignTop)

        # Добавляем search_layout в правую часть главного макета
        main_layout.addLayout(search_layout)

        self.table_widget.setStyleSheet("""
            QTableWidget {
                font-family: 'Comic Sans MS';
                font-size: 16px;
            }
            QTableWidget::item {
                padding: 5px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: red;
                color: white;
                font-family: 'Comic Sans MS';
                font-size: 20px;
                padding: 5px;
            }
        """)

        self.setStyleSheet('''
            background-color: #0000FF;
        ''')

        print(db_cases)

    
    def load_data(self, table_name, load_to_form):
        # Подключение к базе данных
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()

        # Запрос данных из таблицы Cases
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Получение названий столбцов
        column_names = [column[0] for column in cursor.description]

        # Создание списка словарей из данных
        data_dicts = []
        for row in rows:
            data_dict = {column_names[col_idx]: row[col_idx] for col_idx in range(len(column_names))}
            data_dicts.append(data_dict)

        if load_to_form:
            # Установка количества строк и столбцов в таблице
            self.table_widget.setRowCount(len(rows))
            self.table_widget.setColumnCount(len(column_names))

            # Установка заголовков столбцов
            self.table_widget.setHorizontalHeaderLabels(column_names)

            # Заполнение таблицы данными
            for row_idx, row in enumerate(rows):
                for col_idx, value in enumerate(row):
                    self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        # Закрытие подключения
        cursor.close()
        conn.close()

        # Возврат списка словарей
        return data_dicts

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyForm()
    window.show()
    app.exec_()
