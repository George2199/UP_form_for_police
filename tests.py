import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
import sys

from main import MyForm

class TestMyForm(unittest.TestCase):

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.form = MyForm()

    @patch('main.pyodbc.connect')
    def test_load_data(self, mock_connect):

        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.return_value = [(1, 'test_user', 'password'), (2, 'user2', 'pass2')]
        mock_cursor.description = [('id',), ('login',), ('password',)]
        
        data = self.form.load_data('users')
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['login'], 'test_user')
        self.assertEqual(data[1]['password'], 'pass2')
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users")

    def test_try_enter_valid_credentials(self):
        self.form.login_input.setText('test_user')
        self.form.password_input.setText('password')

        with patch.object(self.form, 'load_data', return_value=[{'login': 'test_user', 'password': 'password'}]):
            with patch.object(self.form, 'enter') as mock_enter:
                self.form.try_enter()
                mock_enter.assert_called_once()

    def test_enter_method_exists(self):
        self.assertTrue(hasattr(self.form, 'enter'), "Метод 'enter' отсутствует в MyForm.")

    def test_try_enter_invalid_credentials(self):
        self.form.login_input.setText('wrong_user')
        self.form.password_input.setText('wrong_pass')

        with patch.object(self.form, 'load_data', return_value=[{'login': 'test_user', 'password': 'password'}]):
            with patch('main.QMessageBox.warning') as mock_warning:
                self.form.try_enter()
                mock_warning.assert_called_once_with(self.form, "Ошибка", "Неверный логин или пароль")

    def test_try_enter_blank_space(self):
        self.form.login_input.setText('')
        self.form.password_input.setText('')

        with patch.object(self.form, 'load_data', return_value=[{'login': 'test_user', 'password': 'password'}]):
            with patch('main.QMessageBox.warning') as mock_warning:
                self.form.try_enter()
                mock_warning.assert_called_once_with(self.form, "Ошибка", "Неверный логин или пароль")

    @patch('main.pyodbc.connect')
    def test_load_data_empty_table(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []
        mock_cursor.description = [('id',), ('login',), ('password',)]
        
        data = self.form.load_data('users')
        
        # Проверяем, что возвращается пустой список
        self.assertEqual(data, [])
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users")

    @patch('main.pyodbc.connect')
    def test_load_data_with_error(self, mock_connect):
        # Настроим моки для генерации исключения
        mock_connect.side_effect = Exception("Connection Error")
        
        with self.assertRaises(Exception) as context:
            self.form.load_data('users')
        
        self.assertEqual(str(context.exception), "Connection Error")

    def test_login_input_placeholder(self):
        # Проверяем, что текст-заполнитель установлен правильно
        self.assertEqual(self.form.login_input.placeholderText(), 'Логин')

    def test_password_input_placeholder(self):
        # Проверяем, что текст-заполнитель установлен правильно
        self.assertEqual(self.form.password_input.placeholderText(), 'Пароль')

    @patch('main.pyodbc.connect')
    def test_try_enter_multiple_users(self, mock_connect):
        # Настраиваем мок для возврата нескольких пользователей
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            (1, 'user1', 'pass1'),
            (2, 'user2', 'pass2'),
            (3, 'test_user', 'password')
        ]
        mock_cursor.description = [('id',), ('login',), ('password',)]
        
        self.form.login_input.setText('test_user')
        self.form.password_input.setText('password')

        with patch.object(self.form, 'load_data', return_value=[
            {'login': 'user1', 'password': 'pass1'},
            {'login': 'user2', 'password': 'pass2'},
            {'login': 'test_user', 'password': 'password'}
        ]):
            with patch.object(self.form, 'enter') as mock_enter:
                self.form.try_enter()
                mock_enter.assert_called_once()


if __name__ == '__main__':
    unittest.main()
