# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:33:55 2026

@author: ThanhHa
"""
import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox, QFileDialog, QTableWidgetItem, QGraphicsDropShadowEffect, QHeaderView
from PyQt6.QtGui import QIcon,QPixmap,QColor,QFont
from PyQt6.QtCore import Qt
from login import Ui_Login
from admin import Ui_Main_Admin
from fix_contract import Ui_MainWindow
from addInfo import Ui_AddInfo

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
        self.stackedWidget.setCurrentIndex(0) #Dashboard làm trang chủ
        self.role = role

        self.format_main()
        self.format_shadowItem()
        self.format_table_all()

        
        self.load_table_json(self.tableWidget_Room,"data/rooms.json")
        self.load_table_json(self.tableWidget_Customer,"data/customers.json")
        self.load_table_json(self.tableWidget_Contract,"data/contracts.json")
        self.load_table_json(self.tableWidget_eIndex,"data/eIndex.json")
        
        self.phanQuyen()
        self.binding_events_main()
        
#==================FORMAT FOR ALL=================================================================================
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
        
    def format_shadowItem(self):
        #Đổ bóng
        lne=[
        self.lne_db_room_dangthue,self.lne_sumCustomer,self.lne_requestCustomer,
        self.lne_db_doanhthu,self.lne_sumContract,self.lne_validContract,self.lne_waitingContract,
        self.lne_db_room_trong,self.lne_abtoEContract,self.lne_eCost,self.lne_wCost,
        self.lne_db_request,self.lne_sumBill, self.lne_paidBill, self.lne_unpaidBill,
        self.lne_db_bill,
        self.tableWidget, self.tableWidget_Room,self.tableWidget_Bill,self.tableWidget_Contract,self.tableWidget_Customer,
        self.lne_phongTrong, self.tableWidget_Request,self.tableWidget_Revenue,self.tableWidget_Staff,self.tableWidget_eIndex,
        self.lne_sumRoom, self.lne_doanhthu_month,self.lne_doanhthu_year,self.lne_sumBillRoom,self.lne_sumBillE,
        self.lne_room_dangthue,self.lne_otherCost]
        
        for le in lne:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setOffset(0,4)
            shadow.setColor(QColor(0,0,0,80))
            le.setGraphicsEffect(shadow)
            
#================================================================================================================

#======================FORMAT QTABLEWIDGET=======================================================================
    def format_table(self, table):
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        
        # tạo cột dấu ba chấm
        col = table.columnCount()
        table.setColumnCount(col + 1)
        table.setHorizontalHeaderItem(col, QTableWidgetItem(""))
        
    def format_table_all(self):
        tables = [
        self.tableWidget_Room,
        self.tableWidget_Customer,
        self.tableWidget_Contract,
        self.tableWidget_eIndex,
        self.tableWidget_Bill,
        self.tableWidget_Request,
        self.tableWidget_Staff,
        self.tableWidget_Revenue
        ]
        
        for table in tables:
            self.format_table(table)
            
    def create_item(self, value): #Khi add item, tự động căn giữa, font, size
        item = QTableWidgetItem(str(value))

        # căn giữa
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    
        # font Arial size 12
        font = QFont("Arial", 12)
        item.setFont(font)
    
        return item
         
    def three_dots(self,row):
            #Thêm QPushButton ba chấm vào mỗi dòng để hiển thị thông tin chi tiết
            btn = QPushButton("⋯")
            btn.setFixedWidth(30)
            btn.setStyleSheet("""
            QPushButton{
                border:none;
                font-size:26px;
            }
            QPushButton:hover{
                background:#f0f0f0;
                border-radius:6px;
            }
        """)
            return btn
#================================================================================================================
#==============DATA==============================================================================================
            
    def load_table_json(self, table, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            return
    
        table.setRowCount(0)
    
        for row_data in data:
    
            row = table.rowCount()
            table.insertRow(row)
    
            for col, value in enumerate(row_data.values()):
                table.setItem(row, col, self.create_item(value))
    
            btn = self.three_dots(row)
            table.setCellWidget(row, table.columnCount()-1, btn)
            
            
#=======================================================================================================================

#++++++++++++TABLE+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def addInfo(self,index):
        self.info_window = addInfo(self)
        self.info_window.stackedWidget.setCurrentIndex(index)
        self.info_window.show()
        
    def fix_Contract(self):
        self.fc = fix_Contract()
        self.fc.show()
        
    #ADD DATA FOR ALL TABLES
    def insert_row_table(self, table, data_dict, json_file):
        row = table.rowCount()
        table.insertRow(row)
    
        for col, value in enumerate(data_dict.values()):
            table.setItem(row, col, self.create_item(value))
    
        btn = self.three_dots(row)
        table.setCellWidget(row, table.columnCount()-1, btn)
    
        self.save_table_json(table, json_file)
    
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#===============ADD INFO+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def save_table_json(self, table, json_file):
        data=[]
        for row in range(table.rowCount()):
            row_data={}
            for col in range(table.columnCount()-1):
                header = table.horizontalHeaderItem(col).text()
            
                item = table.item(row,col)
                value = item.text() if item else ""
            
                row_data[header] = value
            data.append(row_data)
    
        with open(json_file,"w",encoding="utf-8") as f:
            json.dump(data,f,ensure_ascii=False,indent=4)



#+++++++++++++++++++++++++++++++++++++++++++++++==================================================================================
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

        
        self.btn_home.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btn_room.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btn_customer.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.btn_contract.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.btn_eIndex.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.btn_bill.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.btn_request.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(6))
        self.btn_staff.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(7))
        self.btn_report.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(8))
        self.btn_history.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(9))
        self.btn_profile.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(10))

        self.pb_addRoom.clicked.connect(lambda: self.addInfo(0))
        self.pb_addContract.clicked.connect(self.fix_Contract)
        self.pb_eIndex_alter.clicked.connect(lambda: self.addInfo(5))
        self.pb_addBill.clicked.connect(lambda: self.addInfo(9))
        self.pb_addStaff.clicked.connect(lambda: self.addInfo(13))
        self.pb_pf_alter.clicked.connect(lambda: self.addInfo(18))
        
class addInfo(QMainWindow,Ui_AddInfo):
    def __init__(self,admin,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.admin=admin
        self.load_combobox()
        self.binding_events()
        
    def add_room(self):
        room = {
            "phong": self.lne_sophong1.text(),
            "loai": self.cbo_loaiphong1.currentText(),
            "dientich": self.lne_dientich1.text(),
            "gia": self.lne_giathue1.text(),
            "trangthai": self.cbo_trangthai1.currentText(),
            "mota": self.txt_mota1.toPlainText(),
            "tienich": self.txt_tienich1.toPlainText()
        }
        
        self.admin.insert_row_table(
            self.admin.tableWidget_Room,
            room,
            "data/rooms.json"
        )
        QMessageBox.information(self,"Thông báo","Thêm phòng thành công")
        self.close()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
    def load_combobox(self):
        # Loại phòng
        self.cbo_loaiphong1.addItems(["Nhỏ", "Lớn"])
    
        # Trạng thái
        self.cbo_trangthai1.addItems(["Chưa cho thuê", "Đã cho thuê"])
        
    def binding_events(self):
        self.btn_themmoi1.clicked.connect(self.add_room)
        self.btn_huy1.clicked.connect(self.close)
        
        

class fix_Contract(QMainWindow,Ui_MainWindow):
    def __init__(self,admin,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.admin=admin
        
    