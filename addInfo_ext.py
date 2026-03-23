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
from addInfo_eIndex import addInfo_eIndex
from addInfo_Request import addInfo_Request
from addInfo_Staff import addInfo_Staff
from addInfo_Revenue import addInfo_Revenue
from addInfo_Contract import addInfo_Contract

class addInfo(QMainWindow, Ui_AddInfo,addInfo_Room,
              addInfo_Bill,addInfo_Customer,addInfo_eIndex,addInfo_Contract,
              addInfo_Request,addInfo_Staff,addInfo_Revenue):
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
        self.cbo_trangthai10.addItems(["Ngừng hoạt động", "Đang hoạt động"])
        self.cbo_trangthai8.addItems(["Chưa xử lý", "Đã xử lý"])
        self.cbo_gioitinh1.addItems(["Nam", "Nữ"])
        self.cbo_gioitinh3.addItems(["Nam", "Nữ"])
        self.cbo_gioitinh4.addItems(["Nam", "Nữ"])
        self.cbo_phongphutrach2.addItems(["A", "B"])
        self.cbo_phongphutrach3.addItems(["A", "B"])
        self.cbo_nguoidaidien1.addItems(["Có", "Không"])
        self.cbo_trangthai4.addItems([ "Chưa thanh toán","Đã thanh toán"])
        self.cbo_trangthai6.addItems([ "Chưa thanh toán","Đã thanh toán"])
        
        self.lne_sophong9.textChanged.connect(self.auto_fill_bill_info)
   # ======================== BINDING EVENTS ========================
    def binding_events(self):
        self.btn_huy1.clicked.connect(self.close)
        self.btn_huy2.clicked.connect(self.close)
        self.btn_dong1.clicked.connect(self.close)
        self.btn_huy5.clicked.connect(self.close)
        self.btn_huy4.clicked.connect(self.close)
        self.btn_huy6.clicked.connect(self.close)
        self.btn_themmoi1.clicked.connect(self.add_room)
        self.btn_capnhat2.clicked.connect(self.update_price)
        self.btn_tao1.clicked.connect(self.create_bill)
        self.btn_them1.clicked.connect(self.add_staff)
        self.btn_huy10.clicked.connect(self.close)
        self.btn_dong2.clicked.connect(self.close)
        self.btn_huy8.clicked.connect(self.close)
        self.btn_thoat1.clicked.connect(self.close)
        self.btn_xuatfile1.clicked.connect(self.report)
        self.btn_gui1.clicked.connect(self.close)
        self.btn_phanhoi1.clicked.connect(lambda:self.stackedWidget.setCurrentIndex(12))
       

