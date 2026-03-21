# -*- coding: utf-8 -*-
"""
"""
import json
from PyQt6.QtWidgets import (QMainWindow, QPushButton,
                             QMessageBox, QTableWidgetItem,
                             QGraphicsDropShadowEffect, QHeaderView)
from PyQt6.QtGui import QIcon, QColor, QFont
from PyQt6.QtCore import Qt, QDate

from dangnhap import Ui_DangNhap
from admin import Ui_Main_Admin
from fix_contract import Ui_MainWindow

from room_ext     import RoomService
from customer_ext import CustomerService
from contract_ext import ContractService
from bill_ext     import BillService
from eIndex_ext   import EIndexService
from revenue_ext import RevenueService
from staff_ext import StaffService

# =============================================================================
#  LOGIN
# =============================================================================
class Login(QMainWindow, Ui_DangNhap):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.format_login()
        self.binding_events()
        
    def format_login(self):
        #Căn giữa
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
                QMessageBox.warning(self, "Thông báo", "Sai tên đăng nhập hoặc tài khoản!")
        elif self.rad_staff.isChecked():
            if username == "nhanvien" and password == "123":
                self.open_admin("staff")
            else:
                QMessageBox.warning(self, "Thông báo", "Sai tên đăng nhập hoặc tài khoản!")

    def open_admin(self, role):
        self.admin = Admin(role)
        self.admin.show()
        self.close()

    def binding_events(self):
        self.btn_login.clicked.connect(self.handle_login)


# =============================================================================
#  ADMIN  — kế thừa tất cả
# =============================================================================
class Admin(RoomService, CustomerService, ContractService, BillService, EIndexService,RevenueService, StaffService ,QMainWindow, Ui_Main_Admin):

    def __init__(self, role, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.role = role
        self.stackedWidget.setCurrentIndex(0)
        

        self.format_main()
        self.format_shadowItem()
        self.format_table_all()

       
        self.loadTables()
        self.update_stats()
        self.load_price_dashboard()

        self.phanQuyen()
        self.binding_events_main()

# ======== FORMAT TABLE ALL=======================================================================================
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def format_main(self):
        self.setFixedSize(1440,960)
        self.setStyleSheet("""QMainWindow {border-image: url(src/layout.png)}""")
        
        #Căn giữa
        screen = self.screen().availableGeometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)
        
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
        widgets = [
            self.lne_db_room_dangthue, self.lne_sumCustomer, self.lne_requestCustomer,
            self.lne_db_doanhthu, self.lne_sumContract, self.lne_validContract,
            self.lne_waitingContract, self.lne_db_room_trong, self.lne_abtoEContract,
            self.lne_eCost, self.lne_wCost, self.lne_db_request,
            self.lne_sumBill, self.lne_paidBill, self.lne_unpaidBill, self.lne_db_bill,
            self.tableWidget, self.tableWidget_Room, self.tableWidget_Bill,
            self.tableWidget_Contract, self.tableWidget_Customer,
            self.lne_phongTrong, self.tableWidget_Request, self.tableWidget_Revenue,
            self.tableWidget_Staff, self.tableWidget_eIndex,
            self.lne_sumRoom, self.lne_doanhthu_month, self.lne_doanhthu_year,
            self.lne_sumBillRoom, self.lne_sumBillE,
            self.lne_room_dangthue, self.lne_otherCost,
        ]
        for w in widgets:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setOffset(0, 4)
            shadow.setColor(QColor(0, 0, 0, 80))
            w.setGraphicsEffect(shadow)

    def format_table(self, table):
        table.insertColumn(table.columnCount())
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setHorizontalHeaderItem(table.columnCount() - 1, QTableWidgetItem(""))

    def format_table_all(self):
        for table in [self.tableWidget_Room, self.tableWidget_Customer,
                      self.tableWidget_Contract, self.tableWidget_eIndex,
                      self.tableWidget_Bill, self.tableWidget_Request,
                      self.tableWidget_Staff, self.tableWidget_Revenue]:
            self.format_table(table)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#================TIỆN ÍCH DÙNG CHUNG ===========================================================================================
    
    def create_item(self, value):
        item = QTableWidgetItem(str(value))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setFont(QFont("Arial", 12))
        return item

    def three_dots(self, row, table_type):
        btn = QPushButton("⋯")
        btn.setFixedWidth(30)
        btn.setStyleSheet("""
            QPushButton { border:none; font-size:26px; }
            QPushButton:hover { background:#f0f0f0; border-radius:6px; }
        """)
 
        # Lấy table tương ứng với table_type để tìm row động khi bấm
        table_map = {
            "room":     self.tableWidget_Room,
            "customer": self.tableWidget_Customer,
            "contract": self.tableWidget_Contract,
            "eindex":   self.tableWidget_eIndex,
            "bill":     self.tableWidget_Bill,
            "staff": self.tableWidget_Staff,
        }
        handler_map = {
            "room":     self.open_room_detail,
            "customer": self.open_customer_detail,
            "contract": self.open_contract_detail,
            "eindex":   self.open_eindex_detail,
            "bill":     self.open_bill_detail,
            "staff": self.open_staff_detail,
        }
 
        if table_type in handler_map:
            table_ref = table_map[table_type]
            handler   = handler_map[table_type]
 
            def on_click(_, t=table_ref, b=btn, h=handler):
                # Tìm đúng row của button này tại thời điểm bấm — không bị lệch sau reload
                for r in range(t.rowCount()):
                    if t.cellWidget(r, t.columnCount() - 1) is b:
                        h(r)
                        return
 
            btn.clicked.connect(on_click)
 
        return btn

    def load_table_json(self, table, filename, table_type):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            return

        table.setRowCount(0)

        field_map = {
            "room": ["phong", "loai", "dientich", "gia", "trangthai"],
            "customer": ["makh", "hoten", "sodienthoai", "gioitinh", "sophong"],
            "contract": ["maHD", "sophong", "hoten", "trangthai"],
            "eindex": ["phong", "khachthue", "dien_moi", "nuoc_moi", "thangnam"],
            "bill": ["mahoadon", "sophong", "khachthue", "thangnam", "trangthai"],
            "staff": ["manv", "hoten", "sodienthoai", "trangthai"],
        }

        fields = field_map.get(table_type, [])

        for row_data in data:
            row = table.rowCount()
            table.insertRow(row)

            for col, key in enumerate(fields):
                value = row_data.get(key, "")
                table.setItem(row, col, self.create_item(value))

            btn = self.three_dots(row, table_type)
            table.setCellWidget(row, table.columnCount() - 1, btn)

    def insert_row_table(self, table, data_dict, json_file, table_type):
        row = table.rowCount()
        table.insertRow(row)

        field_map = {
            "room":     ["phong", "loai", "dientich", "gia", "trangthai"],
            "customer": ["makh", "hoten", "sodienthoai", "gioitinh", "sophong"],
            "contract": ["maHD", "sophong", "hoten", "trangthai"],
            "eindex":   ["phong", "khachthue", "dien_moi", "nuoc_moi", "thangnam"],
            "bill":     ["mahoadon", "sophong", "khachthue", "thangnam", "trangthai"],
            "staff": ["manv", "hoten", "sodienthoai", "trangthai"],
        }
        fields = field_map.get(table_type, list(data_dict.keys()))
 
        for col, key in enumerate(fields):
            table.setItem(row, col, self.create_item(data_dict.get(key, "")))
 
        btn = self.three_dots(row, table_type)
        table.setCellWidget(row, table.columnCount() - 1, btn)
 
        # Ghi thẳng data_dict vào JSON — giữ nguyên key tiếng Anh, không dùng header bảng
        import os
        if os.path.exists(json_file):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không đọc được {json_file}:\n{e}")
                return
        else:
            existing = []

        existing.append(data_dict)

        try:
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(existing, f, ensure_ascii=False, indent=4)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không ghi được {json_file}:\n{e}")

    def load_price_dashboard(self):
        try:
            with open("data/price.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            self.lne_eCost.setText(str(data["giadien"]))
            self.lne_wCost.setText(str(data["gianuoc"]))
        except:
            pass

    # ─── PHÂN QUYỀN & ĐIỀU HƯỚNG ─────────────────────────────────────────────
    def phanQuyen(self):
        if self.role == "staff":
            self.btn_contract.setDisabled(True)
            self.btn_staff.setDisabled(True)
            self.btn_report.setDisabled(True)
        if self.role=="admin":
            self.btn_history.setDisabled(True)
    
    def logOut(self):
        self.login = Login()
        self.login.show()
        self.close()

    def addInfo(self, index):
        from addInfo_ext import addInfo as AddInfoWindow
        self.info_window = AddInfoWindow(self)
        self.info_window.stackedWidget.setCurrentIndex(index)
        self.info_window.show()

    def fix_Contract(self, index):
        from fix_contract_ext import fix_Contract
        self.info_window = fix_Contract(self)
        self.info_window.stackedWidget.setCurrentIndex(index)
        self.info_window.show()


    def update_stats(self):
            self.update_room_stats()   # từ Room
            self.update_bill_stats()   # từ Bill
            self.update_customer_stats()
            self.update_contract_stats() # từ Contract
        
    def loadTables(self):
        self.load_table_json(self.tableWidget_Room,     "data/rooms.json",     "room")
        self.load_table_json(self.tableWidget_Customer, "data/customers.json", "customer")
        self.load_table_json(self.tableWidget_Contract, "data/contracts.json", "contract")
        self.load_table_json(self.tableWidget_eIndex,   "data/eIndex.json",    "eindex")
        self.load_table_json(self.tableWidget_Bill,     "data/bills.json",     "bill")
        self.load_table_json(self.tableWidget_Staff, "data/staffs.json", "staff")

        #self.load_revenue()
        
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
        self.pb_addContract.clicked.connect(lambda: self.fix_Contract(1))
        self.pb_eIndex_alter.clicked.connect(lambda: self.addInfo(5))
        self.pb_addBill.clicked.connect(lambda: self.addInfo(9))
        self.pb_addStaff.clicked.connect(lambda: self.addInfo(13))
        self.pb_pf_alter.clicked.connect(lambda: self.addInfo(18))

