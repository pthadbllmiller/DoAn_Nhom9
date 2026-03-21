import json
import os
from PyQt6.QtWidgets import  QMessageBox

class addInfo_Staff:
    # ======================== THÊM NHÂN VIÊN ========================
    def add_staff(self):
        manv = self.lne_manv1.text().strip()
        hoten = self.lne_hoten5.text().strip()
        ngaysinh = self.date_ngaysinh1.date().toString("dd/MM/yyyy")
        gioitinh = self.cbo_gioitinh3.currentText().strip()
        cccd = self.lne_cccd3.text().strip()
        sodienthoai = self.lne_sdt5.text().strip()
        tendangnhap = self.lne_tendangnhap1.text().strip()
        matkhau = self.lne_matkhau1.text().strip()
        mucluong = self.lne_mucluong1.text().strip()
        trangthai = self.cbo_trangthai10.currentText().strip()
        hkthuongtru = self.lne_hkthuongtru2.text().strip()
        phongphutrach = self.cbo_phongphutrach1.currentText().strip()
        ghichu = self.txt_ghichu7.toPlainText().strip()

        if not manv:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập mã nhân viên!")
            return
        if not hoten:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập họ tên nhân viên!")
            return
        if not sodienthoai:
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

        staffs = []
        if os.path.exists("data/staffs.json"):
            try:
                with open("data/staffs.json", "r", encoding="utf-8") as f:
                    staffs = json.load(f)
            except Exception:
                staffs = []

        if any(s.get("manv") == manv for s in staffs):
            QMessageBox.warning(self, "Thông báo", "Mã nhân viên đã tồn tại!")
            self.lne_manv1.setFocus()
            self.lne_manv1.selectAll()
            return

        if any(s.get("tendangnhap", "").strip().lower() == tendangnhap.lower() for s in staffs):
            QMessageBox.warning(self, "Thông báo", "Tên đăng nhập đã tồn tại!")
            self.lne_tendangnhap1.setFocus()
            self.lne_tendangnhap_1.selectAll()
            return

        staff = {
            "manv": manv,
            "hoten": hoten,
            "ngaysinh": ngaysinh,
            "gioitinh": gioitinh,
            "cccd": cccd,
            "sodienthoai": sodienthoai,
            "tendangnhap": tendangnhap,
            "matkhau": matkhau,
            "mucluong": mucluong,
            "trangthai": trangthai,
            "hkthuongtru": hkthuongtru,
            "phongphutrach": phongphutrach,
            "ghichu": ghichu
        }

        self.admin.insert_row_table(
            self.admin.tableWidget_Staff,
            staff,
            "data/staffs.json",
            "staff"
        )

        self.admin.update_staff_states()
        QMessageBox.information(self, "Thông báo", "Thêm nhân viên thành công!")
        self.close()

    # ======================== KHÓA / MỞ SỬA ========================
    def enable_edit_staff(self):
        for w in [
            self.lne_manv2,
            self.lne_hoten6,
            self.lne_cccd4,
            self.lne_sdt6,
            self.lne_tendangnhap2,
            self.lne_matkhau2,
            self.lne_mucluong2,
            self.lne_hkthuongtru3,
            self.txt_ghichu8
        ]:
            w.setReadOnly(False)
        self.date_ngaysinh2.setEnabled(True)
        self.cbo_gioitinh4.setEnabled(True)
        self.cbo_trangthai_n.setEnabled(True)
        self.cbo_phongphutrach3.setEnabled(True)

    def disable_edit_staff(self):
        for w in [
            self.lne_manv2,
            self.lne_hoten6,
            self.lne_cccd4,
            self.lne_sdt6,
            self.lne_tendangnhap2,
            self.lne_matkhau2,
            self.lne_mucluong2,
            self.lne_hkthuongtru2,
            self.txt_ghichu8
        ]:
            w.setReadOnly(True)

        self.date_ngaysinh2.setEnabled(False)
        self.cbo_gioitinh4.setEnabled(False)
        self.cbo_trangthai_n.setEnabled(False)
        self.cbo_phongphutrach2.setEnabled(False)

    def handle_edit_staff(self):
        if not self.is_editing:
            self.enable_edit_staff()
            self.btn_chinhsua3.setText("Cập nhật")
            self.is_editing = True
        else:
            self.update_staff_json()
            self.disable_edit_staff()
            self.btn_chinhsua3.setText("Chỉnh sửa")
            self.is_editing = False

    # ======================== CẬP NHẬT JSON ========================
    def update_staff_json(self):
        manv = self.lne_manv2.text().strip()

        try:
            with open("data/staffs.json", "r", encoding="utf-8") as f:
                staffs = json.load(f)
        except Exception:
            staffs = []

        for s in staffs:
            if s.get("manv") == manv:
                s["hoten"] = self.lne_hoten6.text().strip()
                s["ngaysinh"] = self.date_ngaysinh2.date().toString("dd/MM/yyyy")
                s["gioitinh"] = self.cbo_gioitinh4.currentText().strip()
                s["cccd"] = self.lne_cccd4.text().strip()


                s["sodienthoai"] = self.lne_sdt6.text().strip()
                s["tendangnhap"] = self.lne_tendangnhap2.text().strip()
                s["matkhau"] = self.lne_matkhau2.text().strip()
                s["mucluong"] = self.lne_mucluong2.text().strip()
                s["trangthai"] = self.cbo_trangthai_n.currentText().strip()
                s["hkthuongtru"] = self.lne_hkthuongtru3.text().strip()
                s["phongphutrach"] = self.cbo_phongphutrach2.currentText().strip()
                s["ghichu"] = self.txt_ghichu8.toPlainText().strip()



        with open("data/staffs.json", "w", encoding="utf-8") as f:
            json.dump(staffs, f, ensure_ascii=False, indent=4)

        self.admin.load_table_json(self.admin.tableWidget_Staff, "data/staffs.json", "staff")
        self.admin.update_staff_states()
        QMessageBox.information(self, "Thông báo", "Cập nhật nhân viên thành công!")
        self.close()
