# -*- coding: utf-8 -*-
"""
bill_ext.py
Chứa Bill — tất cả logic liên quan đến quản lý Hoá Đơn.
Được kế thừa bởi class Admin trong QuanLyPhongTro_Ext.py
"""
import json
import os
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from addInfo import Ui_AddInfo

class BillService:

    # ======================================== MỞ THÔNG TIN HOÁ ĐƠN CHI TIẾT ========================================
    def open_bill_detail(self, row):
        from addInfo_ext import addInfo

        mahoadon = self.tableWidget_Bill.item(row, 0).text()

        with open("data/bills.json", "r", encoding="utf-8") as f:
            bills = json.load(f)

        for b in bills:
            if b["mahoadon"] == mahoadon:
                self.info_window = addInfo(self)
                self.info_window.stackedWidget.setCurrentIndex(7)

                self.info_window.lne_mahoadon1.setText(b["mahoadon"])
                self.info_window.lne_sophong7.setText(b["sophong"])
                self.info_window.lne_khachthue2.setText(b["khachthue"])
                self.info_window.lne_thangnam2.setText(b["thangnam"])
                self.info_window.cbo_trangthai4.setCurrentText(b["trangthai"])

                self.info_window.lne_tienthuephong1.setText(str(b["tienphong"]))
                self.info_window.lne_tiendien1.setText(str(b["tiendien"]))
                self.info_window.lne_tiennuoc1.setText(str(b["tiennuoc"]))

                self.info_window.lne_phivs1.setText(str(b["phivesinh"]))
                self.info_window.lne_phigiuxe1.setText(str(b["phiguixe"]))
                self.info_window.lne_phiwifi1.setText(str(b["phiwifi"]))
                self.info_window.lne_phikhac11.setText(str(b.get("ndphikhac", "")))
                self.info_window.lne_phikhac21.setText(str(b["phikhac"]))

                self.info_window.txt_ghichu3.setPlainText(b["ghichu"])

                self.info_window.set_read_only()
                self.info_window.show()
                return
    # ======================================== CẬP NHẬT THỐNG KÊ HOÁ ĐƠN ========================================
    def update_bill_stats(self):
        total = self.tableWidget_Bill.rowCount()
        paid = 0
        unpaid = 0

        for row in range(total):
            item = self.tableWidget_Bill.item(row, 4)
            if item:
                status = item.text().strip().lower()
                if status == "đã thanh toán":
                    paid += 1
                else:
                    unpaid += 1

        self.lne_sumBill.setText(str(total))
        self.lne_paidBill.setText(str(paid))
        self.lne_unpaidBill.setText(str(unpaid))
        self.lne_db_bill.setText(str(unpaid))