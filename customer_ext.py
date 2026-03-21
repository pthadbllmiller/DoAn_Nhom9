# -*- coding: utf-8 -*-
"""
customer_ext.py
Chứa Customer— tất cả logic liên quan đến quản lý Khách Thuê.
Được kế thừa bởi class Admin trong QuanLyPhongTro_Ext.py
"""
import json
from PyQt6.QtWidgets import QMessageBox, QMainWindow


class CustomerService:

    # ======================================== MỞ THÔNG TIN KHÁCH THUÊ CHI TIẾT ========================================
    def open_customer_detail(self, row):
        from addInfo_ext import addInfo

        makh = self.tableWidget_Customer.item(row, 0).text()

        with open("data/customers.json", "r", encoding="utf-8") as f:
            customers = json.load(f)

        for c in customers:
            if c["makh"] == makh:
                self.info_window = addInfo(self)
                self.info_window.stackedWidget.setCurrentIndex(3)

                self.info_window.lne_makhachthue1.setText(c["makh"])
                self.info_window.lne_hoten1.setText(c["hoten"])
                self.info_window.cbo_gioitinh1.setCurrentText(c["gioitinh"])
                self.info_window.lne_sdt1.setText(c["sodienthoai"])
                self.info_window.lne_sophong4.setText(c["sophong"])
                self.info_window.lne_cccd1.setText(c["cccd"])
                self.info_window.lne_ngaysinh1.setText(c["ngaysinh"])
                self.info_window.lne_biensoxe1.setText(c["biensoxe"])
                self.info_window.txt_hkthuongtru1.setPlainText(c["hokhau"])
                self.info_window.txt_ghichu1.setPlainText(c["ghichu"])

         # Khóa không cho chỉnh sửa khi xem chi tiết
                self.info_window.disable_edit_customer()
                self.info_window.show()
                return

    def update_customer_stats(self):
        total = self.tableWidget_Customer.rowCount()
        self.lne_sumCustomer.setText(str(total))
