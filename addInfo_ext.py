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

class addInfo(QMainWindow, Ui_AddInfo,addInfo_Room,addInfo_Bill,addInfo_Customer):
    def __init__(self, admin, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.admin = admin
        self.is_editing = False

        self.btn_chinhsua2.clicked.connect(self.handle_edit)
        self.btn_huyhoadon1.clicked.connect(self.handle_cancel)

        self.load_combobox()
        self.binding_events()

    # ======================== COMBOBOX ========================
    def load_combobox(self):
        self.cbo_loaiphong1.addItems(["Nhỏ", "Lớn"])
        self.cbo_trangthai1.addItems(["Ngừng hoạt động", "Đã cho thuê","Chuẩn bị cho thuê"])
        self.cbo_trangthai2.addItems(["Ngừng hoạt động", "Đã cho thuê", "Chuẩn bị cho thuê"])
        self.cbo_gioitinh1.addItems(["Nam", "Nữ"])
        self.cbo_nguoidaidien1.addItems(["Có", "Không"])
        self.cbo_trangthai4.addItems(["Đã thanh toán", "Chưa thanh toán"])
        

   # ======================== BINDING EVENTS ========================
    def binding_events(self):
        self.btn_huy1.clicked.connect(self.close)
        self.btn_huy2.clicked.connect(self.close)
        self.btn_dong1.clicked.connect(self.close)
        self.btn_huy5.clicked.connect(self.close)
        self.btn_huy4.clicked.connect(self.close)
        self.btn_huy6.clicked.connect(self.close)
        self.btn_themmoi1.clicked.connect(self.add_room)
        #self.btn_capnhat2.clicked.connect(self.update_price)
        #self.btn_tao1.clicked.connect(self.create_bill)
       

