# -*- coding: utf-8 -*-
import json
import os
from PyQt6.QtWidgets import  QMessageBox
class addInfo_Bill:
# ======================== TẠO HOÁ ĐƠN ==========================================================
    def add_bill(self):
        # lấy thông tin người dùng
        mahoadon = self.lne_mahoadon3.text().strip()
        khachthue = self.lne_khachthue4.text().strip()
        so_phong = self.lne_sophong9.text().strip()
        thangnam = self.lne_thangnam4.text().strip()
        trangthai = self.cbo_trangthai6.currentText()
        tienthuephong = self.lne_tienthuephong3.text().strip()
        tiendien = self.lne_tiendien3.text().strip()
        tiennuoc = self.lne_tiennuoc3.text().strip()
        phivs = self.lne_phivs3.text().strip()
        phigiuxe = self.lne_phigiuxe3.text().strip()
        phiwifi = self.lne_phiwifi3.text().strip()
        ndphikhac = self.lne_phikhac13.text().strip()
        phikhac = self.lne_phikhac23.text().strip()
        ghichu = self.txt_ghichu5.toPlainText().strip()

        # kiểm tra dữ liệu rỗng
        if not mahoadon:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập mã hoá đơn!")
            return
        if not khachthue:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập khách thuê!")
            return
        if not so_phong:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập số phòng!")
            return
        if not thangnam:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập tháng năm!")
            return
        if not tienthuephong:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập tiền thuê phòng!")
            return
        if not tiendien:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập tiền điện!")
            return
        if not tiennuoc:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập tiền nước!")
            return
        if not phivs:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập phí vệ sinh!")
            return
        if not phigiuxe:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập phí giữ xe!")
            return
        if not phiwifi:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập phí wifi!")
            return

        bills = []
        if os.path.exists("data/bills.json"):
            try:
                with open("data/bills.json", "r", encoding="utf-8") as f:
                    bills = json.load(f)
            except Exception:
               bills = []

        # trùng mã hợp đồng
        if any(c.get("mahoandon") == mahoadon for c in bills):
            QMessageBox.warning(self, "Thông báo", "Mã hợp đồng đã tồn tại! Vui lòng nhập mã khác.")
            self.lne_mahoadon_3.setFocus()
            self.lne_mahoadon_3.selectAll()
            return

        bill = {
            "mahoadon": mahoadon,
            "khachthue": khachthue,
            "sophong": so_phong,
            "thangnam": thangnam,
            "trangthai": trangthai,
            "tienthuephong": tienthuephong,
            "tiendien": tiendien,
            "tiennuoc": tiennuoc,
            "phivs": phivs,
            "phigiuxe": phigiuxe,
            "phiwifi": phiwifi,
            "noidungphikhac": ndphikhac,
            "phikhac": phikhac,
            "ghichu": ghichu
        }

        bills.append(bill)
        # ghi dữ liệu xuống file json
        with open("data/bills.json", "w", encoding="utf-8") as f:
            json.dump(bills, f, ensure_ascii=False, indent=4)

        # reload bảng
        self.admin.loadTables()
        # cập nhật lại trên dashboard
        self.admin.update_bill_stats()
        QMessageBox.information(self, "Thông báo", "Thêm hoá đơn thành công!")
        self.close()


    def handle_edit_bill(self):
        if not self.is_editing:
            self.enable_edit_bill()
            self.btn_capnhat2.setText("Cập nhật")
            self.is_editing = True
        else:
            self.update_bill_json()
            self.disable_edit_bill()
            self.btn_capnhat2.setText("Chỉnh sửa")
            self.is_editing = False

    # hàm có thể chỉnh sửa
    def enable_edit_bill(self):
        for lne in [
            self.lne_mahoadon1,
            self.lne_khachthue2,
            self.lne_sophong7,
            self.lne_thangnam2,
            self.lne_tienthuephong4,
            self.lne_tiendien1,
            self.lne_tiennuoc1,
            self.lne_phivs1,
            self.lne_phigiuxe1,
            self.lne_phiwifi1,
            self.lne_phikhac11,
            self.lne_phikhac21,
            self.txt_ghichu3
        ]:
            lne.setReadOnly(False)

        self.cbo_trangthai4.setEnabled(True)

    # hàm không cho chỉnh sửa
    def disable_edit_bill(self):
        # thông tin hoá đơn
        for lne in [
            self.lne_mahoadon1,
            self.lne_khachthue2,
            self.lne_sophong7,
            self.lne_thangnam2,
            self.lne_tienthuephong4,
            self.lne_tiendien1,
            self.lne_tiennuoc1,
            self.lne_phivs1,
            self.lne_phigiuxe1,
            self.lne_phiwifi1,
            self.lne_phikhac11,
            self.lne_phikhac21,
            self.txt_ghichu3
        ]:
            lne.setReadOnly(True)

        self.cbo_trangthai4.setEnabled(False)

    # xoá hợp đồng
    def delete_bill(self):
        mahoadon = self.lne_mahoadon.text().strip()

        reply = QMessageBox.question(
            self,
            "Xác nhận xoá",
            f"Bạn có chắc chắn muốn xoá hoá đơn {mahoadon} không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.No:
            return

        with open("data/bills.json", "r", encoding="utf-8") as f:
            bills = json.load(f)

        new_bills = []
        for c in bills:
            if c.get("mahoadon") != mahoadon:
                new_bills.append(c)

        # lọc bỏ hóa đơn cần xoá
        bills = [b for b in bills if b.get("mahoadon") != mahoadon]

        with open("data/bills.json", "w", encoding="utf-8") as f:
            json.dump(bills, f, ensure_ascii=False, indent=4)

        QMessageBox.information(self, "Thông báo", "Xoá hoá đơn thành công!")
        self.close()
        self.admin.loadTables()
        self.admin.update_bill_stats()


    def update_bill_json(self):
            mahoadon = self.lne_mahoadon1.text()

            with open("data/bills.json", "r", encoding="utf-8") as f:
                bills = json.load(f)

            for i, h in enumerate(bills):
                if h["mahoadon"] == mahoadon:
                    bills[i] = {
                        "mahoadon": mahoadon,
                        "khachthue": self.lne_khachthue2.text(),
                        "sophong": self.lne_sophong7.text(),
                        "thangnam": self.lne_thangnam2.text(),
                        "trangthai": self.cbo_trangthai4.currentText(),

                        "tienthuephong": self.lne_tienthuephong1.text(),
                        "tiendien": self.lne_tiendien1.text(),
                        "tiennuoc": self.lne_tiennuoc1.text(),
                        "phivs": self.lne_phivs1.text(),
                        "phigiuxe": self.lne_phigiuxe1.text(),
                        "phiwifi": self.lne_phiwifi1.text(),

                        "ndphikhac": self.lne_phikhac11.text(),
                        "phikhac": self.lne_phikhac21.text(),

                        "ghichu": self.txt_ghichu3.toPlainText()
                    }
                    break

            with open("data/bills.json", "w", encoding="utf-8") as f:
                json.dump(bills, f, ensure_ascii=False, indent=4)

            QMessageBox.information(self, "Thông báo", "Cập nhật hoá đơn thành công!")
            self.close()
            self.admin.loadTables()
            self.admin.update_bill_stats()
