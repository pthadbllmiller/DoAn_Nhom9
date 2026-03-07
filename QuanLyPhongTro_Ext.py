# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:33:55 2026

@author: ThanhHa
"""
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidgetItem
from PyQt6.QtGui import QIcon,QPixmap
from login import Ui_Login
from admin import Ui_Main_Admin

class Login(QMainWindow,Ui_Login):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.format_login()
        self.binding_events()
        
        
    def format_login(self):
        self.setFixedSize(1440,1024)
        self.setStyleSheet("""QMainWindow {border-image: url(src/login.png)}""")
        
    def handle_login(self):
        username=self.lne_sign.text()
        password=self.lne_pw.text()
        
        # Kiểm tra nhập rỗng
        if username == "" or password == "":
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return
        
        # Kiểm tra có chọn radioButton chưa
        if not self.rd_admin.isChecked() and not self.rd_nv.isChecked():
            QMessageBox.warning(self, "Thông báo", "Vui lòng chọn quyền đăng nhập!")
            return
        
        #========ADMIN=========
        if self.rd_admin.isChecked():
            if username=='admin' and password=='123': #Admin: Username: admin, Password: 123
                self.open_admin('admin')
            else:
                QMessageBox.warning(self, "Thông báo", "Sai tên đăng nhập hoặc tài khoản!")
        
        #========STAFF=========
        elif self.rd_nv.isChecked():
            if username=='nhanvien' and password=='123': #Staff: Username: nhanvien, Password: 123
                self.open_admin('staff')
            else:
                QMessageBox.warning(self, "Thông báo", "Sai tên đăng nhập hoặc tài khoản!")
                
    #Mở Window dựa trên Role
    def open_admin(self,role):
        self.admin = Admin(role)
        self.admin.show()
        self.close()

        
    def binding_events(self):
        self.btn_sign.clicked.connect(self.handle_login)
    
class Admin(QMainWindow,Ui_Main_Admin):
    def __init__(self,role,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.role = role

        self.format_main()
        self.phanQuyen()
        self.binding_events_main()

    def format_main(self):
        self.setFixedSize(1440,1024)
        self.setStyleSheet("""QMainWindow {border-image: url(src/layout.png)}""")
        
        self.btn_home.setIcon(QIcon("icons/home.png"))
        self.btn_room.setIcon(QIcon("icons/door.png"))
        self.btn_customer.setIcon(QIcon("icons/people.png"))
        self.btn_contract.setIcon(QIcon("icons/agreement.png"))
        self.btn_eIndex.setIcon(QIcon("icons/electric.png"))
        self.btn_bill.setIcon(QIcon("icons/bill.png"))
        self.btn_request.setIcon(QIcon("icons/tools.png"))
        self.btn_staff.setIcon(QIcon("icons/group.png"))
        self.btn_report.setIcon(QIcon("icons/report.png"))
        self.btn_history.setIcon(QIcon("icons/history.png"))
        self.btn_profile.setIcon(QIcon("icons/user.png"))
        self.btn_logOut.setIcon(QIcon("icons/log-out.png"))

        
        
    #Staff sẽ không hiển thị các btn hợp đồng, qly nhân viên và báo cáo thống kê
    def phanQuyen(self):
        if self.role=='staff':
            self.btn_contract.setDisabled(True)
            self.btn_staff.setDisabled(True)
            self.btn_report.setDisabled(True)
            
    def logOut(self):
        from __main__ import Login # import lại Login
        self.login = Login()
        self.login.show()
        self.close()
        
    #Nút đăng xuất
    def binding_events_main(self):
        self.btn_logOut.clicked.connect(self.logOut)