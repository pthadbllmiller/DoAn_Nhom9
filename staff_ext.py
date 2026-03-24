# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:59:32 2026

@author: ThanhHa
"""

import json
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from PyQt6.QtCore import QDate

class StaffService:
# ======================================== MỞ THÔNG TIN PHÒNG CHI TIẾT ========================================
    def open_staff_detail(self, row):
        from addInfo_ext import addInfo  # import ở đây để tránh circular import

        manv = self.tableWidget_Staff.item(row, 0).text()

        with open("data/staffs.json", "r", encoding="utf-8") as f:
            staffs = json.load(f)

        for s in staffs:
            if s["manv"] == manv:
                self.info_window = addInfo(self)
                self.info_window.stackedWidget.setCurrentIndex(14)

                self.info_window.lne_manv2.setText(s["manv"])
                self.info_window.lne_hoten6.setText(s["hoten"])
                self.info_window.lne_cccd4.setText(s["cccd"])
                self.info_window.lne_sdt6.setText(s["sodienthoai"])
                self.info_window.lne_tendangnhap2.setText(s["tendangnhap"])
                self.info_window.lne_matkhau2.setText(s["matkhau"])
                self.info_window.lne_mucluong2.setText(s["mucluong"])
                self.info_window.lne_trangthai1.setText(s["trangthai"])
                self.info_window.lne_hkthuongtru3.setText(s.get("hkthuongtru", ""))
                self.info_window.txt_ghichu8.setPlainText(s.get("ghichu", ""))
 
                try:
                    self.info_window.date_ngaysinh2.setDate(
                        QDate.fromString(s.get("ngaysinh", ""), "dd/MM/yyyy")
                    )
                    self.info_window.cbo_gioitinh4.setCurrentText(s.get("gioitinh", ""))
                    self.info_window.cbo_phongphutrach2.setCurrentText(s.get("phongphutrach", ""))
                except Exception:
                    pass


                self.info_window.disable_edit_staff()
                self.info_window.btn_chinhsua3.clicked.connect(self.info_window.handle_edit_staff)
                
                self.info_window.show()
                return
            
    def update_staff_stats(self):
        total = self.tableWidget_Staff.rowCount()
        active = 0
        inactive = 0
 
        for row in range(total):
            item = self.tableWidget_Staff.item(row, 3)
            if item:
                status = item.text().strip().lower()
                if status == "đang hoạt động":
                    active += 1
                else:
                    inactive += 1
 
        self.lne_sumStaff.setText(str(total))
        self.lne_aStaff.setText(str(active))
        self.lne_unaStaff.setText(str(inactive))
 