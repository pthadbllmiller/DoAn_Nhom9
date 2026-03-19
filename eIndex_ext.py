# -*- coding: utf-8 -*-
"""
eindex_ext.py
Chứa EIndex — tất cả logic liên quan đến quản lý Chỉ Số Điện Nước.
Được kế thừa bởi class Admin trong QuanLyPhongTro_Ext.py
"""
import json
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from addInfo import Ui_AddInfo


class EIndexService:

    # ======================================== MỞ THÔNG TIN CHỈ SỐ ĐIỆN NƯỚC CHI TIẾT ========================================
    def open_eindex_detail(self, row):
        from addInfo_ext import addInfo

        phong = self.tableWidget_eIndex.item(row, 0).text()

        with open("data/eIndex.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for e in data:
            if e["phong"] == phong:
                self.info_window = addInfo(self)
                self.info_window.stackedWidget.setCurrentIndex(6)

                self.info_window.lne_sophong6.setText(e["phong"])
                self.info_window.lne_khachthue1.setText(e["khachthue"])
                self.info_window.lne_thangnam1.setText(e["thangnam"])
                self.info_window.lne_csdiencu1.setText(e["dien_cu"])
                self.info_window.lne_csdienmoi1.setText(e["dien_moi"])
                self.info_window.lne_csnuoccu1.setText(e["nuoc_cu"])
                self.info_window.lne_csnuocmoi1.setText(e["nuoc_moi"])
                self.info_window.txt_lydo1.setPlainText(e["lydo"])

                self.info_window.show()
                return
            
# ======================== CẬP NHẬT GIÁ ĐIỆN NƯỚC ========================
    def update_price(self):
        giadien = self.lne_giadienmoi.text().strip()
        gianuoc = self.lne_gianuocmoi.text().strip()
 
        if not giadien or not gianuoc:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ giá điện và giá nước!")
            return
 
        data = {"giadien": giadien, "gianuoc": gianuoc}
        with open("data/price.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
 
        # Reload giá lên dashboard của Admin
        self.admin.load_price_dashboard()
        self.info_window.lne_giadiencu.setText(self.lne_eCost.text())
        self.info_window.lne_gianuoccu.setText(self.lne_wCost.text())
        
        QMessageBox.information(self, "Thông báo", "Cập nhật giá thành công!")
        self.close()
        

