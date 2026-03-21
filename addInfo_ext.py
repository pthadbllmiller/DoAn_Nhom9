# -*- coding: utf-8 -*-
"""
addInfo_ext.py
Chứa class addInfo (form thêm/xem chi tiết) và RoomDetail.
Tách ra khỏi QuanLyPhongTro_Ext.py để gọn hơn.
"""
import json
import os
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import QDate, QEvent
from addInfo import Ui_AddInfo

from room_ext import *
from customer_ext import *
from contract_ext import *
from bill_ext import *
from eIndex_ext import *

from addInfo_Room import addInfo_Room
from addInfo_Bill import addInfo_Bill
from addInfo_Customer import addInfo_Customer
from addInfo_Staff import addInfo_Staff

class addInfo(QMainWindow, Ui_AddInfo,addInfo_Room,addInfo_Bill,addInfo_Customer, addInfo_Staff):
    def __init__(self, admin, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.admin = admin
        self.is_editing = False

        self.btn_chinhsua2.clicked.connect(self.handle_edit_bill)
        self.btn_huyhoadon1.clicked.connect(self.delete_bill)

        self.load_combobox()
        self.binding_events()

    # ======================== COMBOBOX ========================
    def load_combobox(self):
        self.cbo_loaiphong1.addItems(["Nhỏ", "Lớn"])
        self.cbo_trangthai1.addItems(["Ngừng hoạt động", "Đã cho thuê","Chuẩn bị cho thuê"])
        self.cbo_trangthai2.addItems(["Ngừng hoạt động", "Đã cho thuê", "Chuẩn bị cho thuê"])
        self.cbo_gioitinh1.addItems(["Nam", "Nữ"])
        self.cbo_gioitinh3.addItems(["Nam", "Nữ"])
        self.cbo_gioitinh4.addItems(["Nam", "Nữ"])
        self.cbo_nguoidaidien1.addItems(["Có", "Không"])
        self.cbo_trangthai4.addItems(["Đã thanh toán", "Chưa thanh toán"])
        self.cbo_trangthai6.addItems(["Đã thanh toán", "Chưa thanh toán"])
        self.cbo_trangthai7.addItems(["Đang hoạt động", "Ngừng hoạt động"])
        self.cbo_trangthai_n.addItems(["Đang hoạt động", "Ngừng hoạt động"])
        self.cbo_trangthai10.addItems(["Đang hoạt động", "Ngừng hoạt động"])
        room_codes = []
        for hundred in range(1, 6):  # 1 to 5
            for num in range(1, 11):  # 1 to 10
                code = f"A{hundred}{num:02d}"
                room_codes.append(code)
        self.cbo_phongphutrach1.addItems(room_codes)



        

   # ======================== BINDING EVENTS ========================
    def binding_events(self):
        self.btn_huy1.clicked.connect(self.close)
        self.btn_huy2.clicked.connect(self.close)
        self.btn_dong1.clicked.connect(self.close)
        self.btn_dong2.clicked.connect(self.close)
        self.btn_huy5.clicked.connect(self.close)
        self.btn_huy4.clicked.connect(self.close)
        self.btn_huy6.clicked.connect(self.close)
        self.btn_tao1.clicked.connect(self.add_bill)
        self.btn_themmoi1.clicked.connect(self.add_room)
        self.btn_capnhat2.clicked.connect(self.handle_edit_bill)
        self.btn_huyhoadon1.clicked.connect(self.delete_bill)
        self.btn_them1.clicked.connect(self.add_staff)



        #self.btn_capnhat2.clicked.connect(self.update_price)
        #self.btn_tao1.clicked.connect(self.create_bill)
       

