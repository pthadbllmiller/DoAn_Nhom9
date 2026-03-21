# -*- coding: utf-8 -*-
"""
staff_ext.py
Chứa Staff — tất cả logic liên quan đến quản lý Nhân viên.
Được kế thừa bởi class Admin trong QuanLyPhongTro_Ext.py
"""
import json
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from PyQt6.QtCore import QDate


class StaffService:
    # ======================================== MỞ THÔNG TIN NHÂN VIÊN CHI TIẾT ========================================
    def open_staff_detail(self, row):
        from addInfo_ext import addInfo

        manv = self.tableWidget_Staff.item(row, 0).text()

        with open("data/staffs.json", "r", encoding="utf-8") as f:
            staffs = json.load(f)

        for s in staffs:
            if s["manv"] == manv:
                self.info_window = addInfo(self)
                self.info_window.stackedWidget.setCurrentIndex(14)
                self.info_window.lne_manv2.setText(s["manv"])
                self.info_window.lne_hoten6.setText(s["hoten"])

                ngaysinh_str = s.get("ngaysinh", "")
                if ngaysinh_str:
                    qdate_ngaysinh = QDate.fromString(ngaysinh_str, "dd/MM/yyyy")
                    if qdate_ngaysinh.isValid():
                        self.info_window.date_ngaysinh1.setDate(qdate_ngaysinh)

                self.info_window.cbo_gioitinh4.setCurrentText(s["gioitinh"])
                self.info_window.lne_cccd4.setText(s["cccd"])
                self.info_window.lne_sdt6.setText(s["sodienthoai"])
                self.info_window.lne_tendangnhap2.setText(s["tendangnhap"])
                self.info_window.lne_matkhau2.setText(s["matkhau"])
                self.info_window.lne_mucluong2.setText(str(s["mucluong"]))
                self.info_window.cbo_trangthai_n.setCurrentText(s["trangthai"])
                self.info_window.lne_hkthuongtru3.setText(s["hkthuongtru"])
                self.info_window.cbo_phongphutrach2.setCurrentText(s["phongphutrach"])
                self.info_window.txt_ghichu8.setPlainText(s["ghichu"])

                self.info_window.disable_edit_staff()
                self.info_window.btn_chinhsua3.clicked.connect(self.info_window.handle_edit_staff)
                self.info_window.show()
                return

    # ======================================== CẬP NHẬT THỐNG KÊ NHÂN VIÊN ========================================
    def update_staff_states(self):
        total = self.tableWidget_Staff.rowCount()
        active = 0
        inactive = 0

        for row in range(total):
            item = self.tableWidget_Staff.item(row, 3)
            if item:
                status = item.text().strip().lower()
                if status == "đang hoạt động":
                    active += 1
                elif status == "ngừng hoạt động":
                    inactive += 1

        self.lne_sumStaff.setText(str(total))
        self.lne_aStaff.setText(str(active))
        self.lne_unaStaff.setText(str(inactive))
