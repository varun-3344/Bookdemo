from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QScrollArea, QLineEdit,
    QHBoxLayout, QFrame, QPushButton, QLabel, QDateEdit, QDialog
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from db import get_all_books, create_table, insert_book, update_book, delete_book

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📚 My Book Tracker")
        self.setMinimumSize(450, 600)
        self.initUI()
        create_table()
        self.load_collection()

    def initUI(self):
        self.main_frame = QFrame()
        self.main_layout = QVBoxLayout(self.main_frame)

        title = QLabel("📘 Add New Book")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 5px;")
        self.main_layout.addWidget(title)

        self.register_widget = CreateRecord(self)
        self.main_layout.addWidget(self.register_widget)

        books_label = QLabel('📖 Completed Books')
        books_label.setStyleSheet('font-size: 16px; margin-top: 10px;')
        self.main_layout.addWidget(books_label)

        self.book_collection_area()

        self.setCentralWidget(self.main_frame)

    def book_collection_area(self):
        scroll_frame = QFrame()
        self.book_collection_layout = QVBoxLayout(scroll_frame)
        self.book_collection_layout.setSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_frame)
        scroll.setStyleSheet('QScrollArea { border: none; }')
        self.main_layout.addWidget(scroll)

    def load_collection(self):
        for i in reversed(range(self.book_collection_layout.count())):
            widget = self.book_collection_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for collection in get_all_books():
            frame = BookCard(*collection, self)
            self.book_collection_layout.insertWidget(0, frame)

    def update_book(self, book_id, name, date, price):
        dialog = UpdateBookDialog(self, book_id, name, date, str(price))
        dialog.exec_()


class CreateRecord(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.book_name = QLineEdit()
        self.book_name.setPlaceholderText('Book name')

        self.date_entry = QDateEdit()
        self.date_entry.setCalendarPopup(True)
        self.date_entry.setDate(QDate.currentDate())

        self.price = QLineEdit()
        self.price.setPlaceholderText('₹ Price')

        self.add_button = QPushButton("➕ Add Book")
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; color: white;
                border-radius: 5px; padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.add_button.clicked.connect(self.add_book)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Book Name:"))
        layout.addWidget(self.book_name)
        layout.addWidget(QLabel("Completed Date:"))
        layout.addWidget(self.date_entry)
        layout.addWidget(QLabel("Price:"))
        layout.addWidget(self.price)
        layout.addWidget(self.add_button)

    def add_book(self):
        name = self.book_name.text()
        date = self.date_entry.date().toString("yyyy-MM-dd")
        price = self.price.text()

        if name and price:
            insert_book(name, date, price)
            self.main_window.load_collection()
            self.book_name.clear()
            self.price.clear()


class BookCard(QFrame):
    def __init__(self, book_id, name, price, completed_date, main_window):
        super().__init__()
        self.main_window = main_window
        self.book_id = book_id
        self.bookname = name
        self.completed_date = completed_date
        self.price = price

        self.setStyleSheet("""
            QFrame {
                background: #fff;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
            }
            QFrame:hover {
                border: 1px solid #0078D7;
                background: #f0faff;
            }
        """)

        layout = QVBoxLayout(self)

        title = QLabel(f"<b>{self.bookname}</b>")
        price_label = QLabel(f"₹{self.price}")
        date_label = QLabel(f"📅 Completed: {self.completed_date}")

        btn_layout = QHBoxLayout()

        # SVG: Edit Icon
        edit_icon = QSvgWidget("edit.svg")
        edit_icon.setFixedSize(26, 26)
        edit_icon.setToolTip("Edit")
        edit_icon.mousePressEvent = lambda event: self.edit_book_click()

        # SVG: Delete Icon
        delete_icon = QSvgWidget("delete.svg")
        delete_icon.setFixedSize(26, 26)
        delete_icon.setToolTip("Delete")
        delete_icon.mousePressEvent = lambda event: self.delete_book_click()

        btn_layout.addStretch()
        btn_layout.addWidget(edit_icon)
        btn_layout.addWidget(delete_icon)

        layout.addWidget(title)
        layout.addWidget(price_label)
        layout.addWidget(date_label)
        layout.addLayout(btn_layout)

        edit_btn = QPushButton()
        edit_btn.setIcon(QIcon("edit.svg"))
        edit_btn.setFixedSize(30, 30)
        edit_btn.setToolTip("Edit")
        edit_btn.setStyleSheet("QPushButton { background: transparent; border: none; } QPushButton:hover { background-color: #e0f7ff; }")
        edit_btn.clicked.connect(self.edit_book_click)

        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon("delete.svg"))
        delete_btn.setFixedSize(30, 30)
        delete_btn.setToolTip("Delete")
        delete_btn.setStyleSheet("QPushButton { background: transparent; border: none; } QPushButton:hover { background-color: #ffe0e0; }")
        delete_btn.clicked.connect(self.delete_book_click)


    def delete_book_click(self):
        delete_book(self.book_id)
        self.main_window.load_collection()

    def edit_book_click(self):
        self.main_window.update_book(self.book_id, self.bookname, self.completed_date, self.price)


class UpdateBookDialog(QDialog):
    def __init__(self, main_window, book_id, name, completed_date, price):
        super().__init__(main_window)
        self.main_window = main_window
        self.book_id = book_id

        self.setWindowTitle("✏️ Update Book")
        self.setFixedSize(300, 170)

        layout = QVBoxLayout()

        self.book_name_edit = QLineEdit()
        self.book_name_edit.setText(name)

        self.price_edit = QLineEdit()
        self.price_edit.setText(price)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.set_date(completed_date)

        btns = QHBoxLayout()
        save_btn = QPushButton("💾 Save", clicked=self.save_update)
        cancel_btn = QPushButton("Cancel", clicked=self.accept)
        btns.addWidget(save_btn)
        btns.addWidget(cancel_btn)

        layout.addWidget(QLabel("Book Name:"))
        layout.addWidget(self.book_name_edit)
        layout.addWidget(QLabel("Price:"))
        layout.addWidget(self.price_edit)
        layout.addWidget(QLabel("Completed Date:"))
        layout.addWidget(self.date_edit)
        layout.addLayout(btns)

        self.setLayout(layout)

    def set_date(self, date_str):
        date = QDate.fromString(date_str, "yyyy-MM-dd")
        self.date_edit.setDate(date)

    def save_update(self):
        updated_name = self.book_name_edit.text()
        updated_price = self.price_edit.text()
        updated_date = self.date_edit.date().toString("yyyy-MM-dd")
        update_book(self.book_id, updated_name, updated_date, updated_price)
        self.accept()
        self.main_window.load_collection()


def main():
    app = QApplication([])
    app.setStyle('Fusion')
    win = Main()
    win.show()
    app.exec_()

if __name__ == '__main__':
    main()
