# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import json
import os
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate


class addInfo_Staff:

    # ======================== THÊM NHÂN VIÊN  ========================
    def add_staff(self):
        manv   = self.lne_manv1.text().strip()
        hoten  = self.lne_hoten5.text().strip()
        cccd   = self.lne_cccd3.text().strip()
        sdt    = self.lne_sdt5.text().strip()
        tendangnhap = self.lne_tendangnhap1.text().strip()
        matkhau = self.lne_matkhau1.text().strip()
        mucluong = self.lne_mucluong1.text().strip()
        
        if not manv:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập mã nhân viên!")
            return
        if not hoten:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập họ tên!")
            return
        if not cccd:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập CCCD!")
            return
        if not sdt:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập số điện thoại!")
            return
        if not tendangnhap:
           QMessageBox.warning(self, "Thông báo", "Vui lòng nhập tên đăng nhập!")
           return
        if not matkhau:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập mật khẩu!")
            return
        if not mucluong:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập mức lương!")
            return

        # Kiểm tra trùng mã nhân viên
        if os.path.exists("data/staffs.json"):
            with open("data/staffs.json", "r", encoding="utf-8") as f:
                staffs = json.load(f)
            if any(s["manv"] == manv for s in staffs):
                QMessageBox.warning(self, "Trùng mã nhân viên!", "Vui lòng nhập mã khác")
                self.lne_manv1.setFocus()
                self.lne_manv1.selectAll()
                return
            
            if any(s.get("tendangnhap", "").strip().lower() == tendangnhap.lower() for s in staffs):
               QMessageBox.warning(self, "Thông báo", "Tên đăng nhập đã tồn tại!")
               self.lne_tendangnhap1.setFocus()
               self.lne_tendangnhap_1.selectAll()
               return

        new_staff = {
            "manv":          manv,
            "hoten":         hoten,
            "ngaysinh":      self.date_ngaysinh1.date().toString("dd/MM/yyyy"),
            "gioitinh":      self.cbo_gioitinh3.currentText(),
            "cccd":          cccd,
            "sodienthoai":   sdt,
            "tendangnhap":   self.lne_tendangnhap1.text().strip(),
            "matkhau":       self.lne_matkhau1.text().strip(),
            "mucluong":      self.lne_mucluong1.text().strip(),
            "hkthuongtru":   self.lne_hkthuongtru2.text().strip(),
            "phongphutrach": self.cbo_phongphutrach1.currentText(),
            "trangthai":     self.cbo_trangthai10.currentText(),
            "ghichu":        self.txt_ghichu7.toPlainText()
        }

        file_path = "data/staffs.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        data.append(new_staff)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.admin.load_table_json(self.admin.tableWidget_Staff, "data/staffs.json", "staff")
        self.admin.update_staff_stats()
        QMessageBox.information(self, "Thông báo", "Thêm nhân viên thành công!")
        self.close()

    # ======================== CHỈ ĐỌC / CHỈNH SỬA  ========================
    def set_readonly_staff(self):
        for w in [self.lne_manv2, self.lne_hoten6, self.lne_cccd4,
                  self.lne_sdt6, self.lne_tendangnhap2, self.lne_matkhau2,
                  self.lne_mucluong2, self.lne_trangthai1, self.lne_hkthuongtru3]:
            w.setReadOnly(True)
        self.txt_ghichu8.setReadOnly(True)
        self.date_ngaysinh2.setEnabled(False)
        self.cbo_gioitinh4.setEnabled(False)
        self.cbo_phongphutrach2.setEnabled(False)

    def enable_edit_staff(self):
        for w in [self.lne_manv2, self.lne_hoten6, self.lne_cccd4,
                  self.lne_sdt6, self.lne_mucluong2, self.lne_trangthai1, self.lne_hkthuongtru3]:
            w.setReadOnly(False)
        self.txt_ghichu8.setReadOnly(False)
        self.date_ngaysinh2.setEnabled(True)
        self.cbo_gioitinh4.setEnabled(True)
        self.cbo_phongphutrach2.setEnabled(True)

    def disable_edit_staff(self):
        self.set_readonly_staff()

    def handle_edit_staff(self):
        if not self.is_editing:
            self.enable_edit_staff()
            self.is_editing = True
            self.btn_chinhsua3.setText("Cập nhật")
        else:
            self.update_staff_json()
            self.disable_edit_staff()
            self.is_editing = False
            self.btn_chinhsua3.setText("Chỉnh sửa")

    # ======================== CẬP NHẬT JSON =============================================================================================
    def update_staff_json(self):
        manv = self.lne_manv2.text().strip()
        if not manv:
            QMessageBox.warning(self, "Thông báo", "Mã nhân viên không được để trống!")
            return

        updated = {
            "manv":          manv,
            "hoten":         self.lne_hoten6.text().strip(),
            "ngaysinh":      self.date_ngaysinh2.date().toString("dd/MM/yyyy"),
            "gioitinh":      self.cbo_gioitinh4.currentText(),
            "cccd":          self.lne_cccd4.text().strip(),
            "sodienthoai":   self.lne_sdt6.text().strip(),
            "tendangnhap":   self.lne_tendangnhap2.text().strip(),
            "matkhau":       self.lne_matkhau2.text().strip(),
            "mucluong":      self.lne_mucluong2.text().strip(),
            "trangthai":     self.lne_trangthai1.text().strip(),
            "hkthuongtru":   self.lne_hkthuongtru3.text().strip(),
            "phongphutrach": self.cbo_phongphutrach2.currentText(),
            "ghichu":        self.txt_ghichu8.toPlainText()
        }

        with open("data/staffs.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for i, s in enumerate(data):
            if s["manv"] == manv:
                data[i] = updated
                break
        with open("data/staffs.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.admin.load_table_json(self.admin.tableWidget_Staff, "data/staffs.json", "staff")
        self.admin.update_staff_stats()
        QMessageBox.information(self, "Thông báo", "Chỉnh sửa nhân viên thành công!")
        self.close()

