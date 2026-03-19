# -*- coding: utf-8 -*-
import json
import os
from PyQt6.QtWidgets import  QMessageBox
class addInfo_Bill:
# ======================== TẠO HOÁ ĐƠN ==========================================================
    def create_bill(self):
        new_bill = {
            "mahoadon":  self.lne_mahoadon3.text(),
            "sophong":   self.lne_sophong9.text(),
            "khachthue": self.lne_khachthue4.text(),
            "thangnam":  self.lne_thangnam4.text(),
            "trangthai": self.cbo_trangthai6.currentText(),
            "tienphong": self.lne_tienthuephong3.text(),
            "tiendien":  self.lne_tiendien3.text(),
            "tiennuoc":  self.lne_tiennuoc3.text(),
            "phivesinh": self.lne_phivs3.text(),
            "phiguixe":  self.lne_phigiuxe3.text(),
            "phiwifi":   self.lne_phiwifi3.text(),
            "phikhac":   self.lne_phikhac23.text(),
            "ghichu":    self.txt_ghichu5.toPlainText()
        }
        file_path = "data/bills.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
        data.append(new_bill)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
        QMessageBox.information(self, "Thông báo", "Tạo hóa đơn thành công")
        self.admin.load_table_json(self.admin.tableWidget_Bill, "data/bills.json", "bill")
        self.admin.update_bill_stats()
        self.close()

    def delete_bill(self):
        ma = self.lne_mahoadon1.text()
        with open("data/bills.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        data = [bill for bill in data if bill["mahoadon"] != ma]
        with open("data/bills.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.admin.load_table_json(self.admin.tableWidget_Bill, "data/bills.json", "bill")
        self.admin.update_bill_stats()
        QMessageBox.information(self, "Thông báo", "Đã xóa hóa đơn")
        self.close()

    def load_current_bill(self):
        ma = self.lne_mahoadon1.text()
        with open("data/bills.json", "r", encoding="utf-8") as f:
            bills = json.load(f)
        for b in bills:
            if b["mahoadon"] == ma:
                self.lne_sophong7.setText(b["sophong"])
                self.lne_khachthue2.setText(b["khachthue"])
                self.lne_thangnam2.setText(b["thangnam"])
                self.cbo_trangthai4.setCurrentText(b["trangthai"])
                self.lne_tienthuephong1.setText(str(b["tienphong"]))
                self.lne_tiendien1.setText(str(b["tiendien"]))
                self.lne_tiennuoc1.setText(str(b["tiennuoc"]))
                self.lne_phivs1.setText(str(b["phivesinh"]))
                self.lne_phigiuxe1.setText(str(b["phiguixe"]))
                self.lne_phiwifi1.setText(str(b["phiwifi"]))
                self.lne_phikhac11.setText(str(b.get("ndphikhac", "")))
                self.lne_phikhac21.setText(str(b["phikhac"]))
                self.txt_ghichu3.setPlainText(b["ghichu"])
                return
            
    # ======================== CHỈNH SỬA / CHỈ ĐỌC HOÁ ĐƠN ========================
    def set_read_only(self):
        for w in [self.lne_mahoadon1, self.lne_sophong7, self.lne_khachthue2,
                  self.lne_thangnam2, self.lne_tienthuephong1, self.lne_tiendien1,
                  self.lne_tiennuoc1, self.lne_phivs1, self.lne_phigiuxe1,
                  self.lne_phiwifi1, self.lne_phikhac11, self.lne_phikhac21]:
            w.setReadOnly(True)
        self.txt_ghichu3.setReadOnly(True)
        self.cbo_trangthai4.setEnabled(False)

    def enable_edit(self):
        for w in [self.lne_mahoadon1, self.lne_sophong7, self.lne_khachthue2,
                  self.lne_thangnam2, self.lne_tienthuephong1, self.lne_tiendien1,
                  self.lne_tiennuoc1, self.lne_phivs1, self.lne_phigiuxe1,
                  self.lne_phiwifi1, self.lne_phikhac11, self.lne_phikhac21]:
            w.setReadOnly(False)
        self.txt_ghichu3.setReadOnly(False)
        self.cbo_trangthai4.setEnabled(True)

    def disable_edit(self):
        self.set_read_only()

    def handle_edit(self):
        if not self.is_editing:
            self.enable_edit()
            self.is_editing = True
            self.btn_chinhsua2.setText("Cập nhật")
            self.btn_huyhoadon1.setText("Hủy")
        else:
            self.update_bill()
            self.disable_edit()
            self.is_editing = False
            self.btn_chinhsua2.setText("Chỉnh sửa")
            self.btn_huyhoadon1.setText("Hủy hóa đơn")

    def handle_cancel(self):
        if self.is_editing:
            self.disable_edit()
            self.load_current_bill()
            self.is_editing = False
            self.btn_chinhsua2.setText("Chỉnh sửa")
            self.btn_huy1.setText("Hủy hóa đơn")
        else:
            self.delete_bill()

    def get_form_data(self):
        return {
            "mahoadon":  self.lne_mahoadon1.text(),
            "sophong":   self.lne_sophong7.text(),
            "khachthue": self.lne_khachthue2.text(),
            "thangnam":  self.lne_thangnam2.text(),
            "trangthai": self.cbo_trangthai4.currentText(),
            "tienphong": int(self.lne_tienthuephong1.text() or 0),
            "tiendien":  int(self.lne_tiendien1.text() or 0),
            "tiennuoc":  int(self.lne_tiennuoc1.text() or 0),
            "phivesinh": int(self.lne_phivs1.text() or 0),
            "phiguixe":  int(self.lne_phigiuxe1.text() or 0),
            "phiwifi":   int(self.lne_phiwifi1.text() or 0),
            "ndphikhac": self.lne_phikhac11.text(),
            "phikhac":   int(self.lne_phikhac21.text() or 0),
            "ghichu":    self.txt_ghichu3.toPlainText()
        }

    def update_bill(self):
        data_new = self.get_form_data()
        ma = data_new["mahoadon"]
        with open("data/bills.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for i, bill in enumerate(data):
            if bill["mahoadon"] == ma:
                data[i] = data_new
                break
        with open("data/bills.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        QMessageBox.information(self, "Thông báo", "Chỉnh sửa hóa đơn thành công!")
        self.close()
        self.admin.load_table_json(self.admin.tableWidget_Bill, "data/bills.json", "bill")
        self.admin.update_bill_stats()