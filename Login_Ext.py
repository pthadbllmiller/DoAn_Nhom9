# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from dangnhap import Ui_DangNhap

class Login(QMainWindow, Ui_DangNhap):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.format_login()
        self.binding_events()
 
    def format_login(self):
        screen = self.screen().availableGeometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)
 
    def handle_login(self):
        username = self.lne_user.text()
        password = self.lne_password.text()
 
        if username == "" or password == "":
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        if not self.rad_admin.isChecked() and not self.rad_staff.isChecked():
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn quyền đăng nhập!")
            return
 
        if self.rad_admin.isChecked():
            if username == "admin" and password == "123":
                self.open_admin("admin")
            else:
                QMessageBox.warning(self, "Thông báo", "Sai tên đăng nhập hoặc mật khẩu!")
        elif self.rad_staff.isChecked():
            if username == "nhanvien" and password == "123":
                self.open_admin("staff")
            else:
                QMessageBox.warning(self, "Thông báo", "Sai tên đăng nhập hoặc mật khẩu!")
 
    def open_admin(self, role):
        from QuanLyPhongTro_Ext import Admin  # import cục bộ tránh circular
        self.admin = Admin(role)
        self.admin.show()
        self.close()
 
    def binding_events(self):
        self.btn_login.clicked.connect(self.handle_login)


