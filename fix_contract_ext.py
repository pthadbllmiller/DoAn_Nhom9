import json
import os
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import QDate, QEvent
from fix_contract import Ui_MainWindow


from contract_ext import *

from addInfo_Contract import addInfo_Contract


class fix_Contract(QMainWindow, Ui_MainWindow, addInfo_Contract):
    def __init__(self, admin,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.admin = admin
        self.is_editing = False

        self.load_combobox()
        self.binding_events()
        self.load_info_admin()

    # ======================== COMBOBOX ========================
    def load_combobox(self):
        self.cbo_trangthai_2.addItems(["Đang chờ hiệu lực", "Hiệu lực", "Hết hiệu lực", "Đã huỷ", "Sắp hết hạn"])
        self.cbo_trangthai_3.addItems(["Đang chờ hiệu lực", "Hiệu lực", "Hết hiệu lực", "Đã huỷ", "Sắp hết hạn"])
        self.cbo_gioitinh_3.addItems(["Nam", "Nữ"])
        self.cbo_gioitinh_4.addItems(["Nam", "Nữ"])
        self.cbo_gioitinh_5.addItems(["Nam", "Nữ"])
        self.cbo_gioitinh_6.addItems(["Nam", "Nữ"])


    # ======================== BINDING EVENTS ========================
    def binding_events(self):
        self.btn_huy.clicked.connect(self.close)
        self.btn_huyhopdong_2.clicked.connect(self.close)
        self.btn_themmoi_2.clicked.connect(self.add_contract)
        self.btn_capnhat_2.clicked.connect(self.handle_edit_contract)
        self.btn_huyhopdong.clicked.connect(self.delete_contract)

    # Luôn load mặc định thông tin admin xem thông tin chi tiết
    def load_info_admin(self):
        # Load mặc định ở page xem chi tiết hợp đồng
        self.lne_hoten_3.setText("Nguyễn Văn A")
        self.lne_hoten_3.setReadOnly(True)

        self.cbo_gioitinh_3.setCurrentText("Nam")
        self.cbo_gioitinh_3.setEnabled(False)

        self.date_namsinh_2.setDate(QDate(1985, 1, 1))
        self.date_namsinh_2.setEnabled(False)

        self.lne_cccd_4.setText("0983837392")
        self.lne_cccd_4.setReadOnly(True)

        self.lne_dcthuongtru_3.setText("123 Lê Lợi, Huế")
        self.lne_dcthuongtru_3.setReadOnly(True)

        self.lne_stk_2.setText("123456789")
        self.lne_stk_2.setReadOnly(True)

        # Load mặc định ở page thêm hợp đồng
        self.lne_hoten_6.setText("Nguyễn Văn A")
        self.lne_hoten_6.setReadOnly(True)

        self.cbo_gioitinh_5.setCurrentText("Nam")
        self.cbo_gioitinh_5.setEnabled(False)

        self.date_namsinh_6.setDate(QDate(1985, 1, 1))
        self.date_namsinh_6.setEnabled(False)

        self.lne_cccd_5.setText("0983837392")
        self.lne_cccd_5.setReadOnly(True)

        self.lne_dcthuongtru_6.setText("123 Lê Lợi, Huế")
        self.lne_dcthuongtru_6.setReadOnly(True)

        self.lne_stk_3.setText("123456789")
        self.lne_stk_3.setReadOnly(True)