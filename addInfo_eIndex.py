# -*- coding: utf-8 -*-
import json
from PyQt6.QtWidgets import  QMessageBox

class addInfo_eIndex:
    # ======================== CẬP NHẬT GIÁ ĐIỆN NƯỚC ========================
    def update_price(self):
        giadien = self.lne_giadienmoi.text().strip()
        gianuoc = self.lne_gianuocmoi.text().strip()

        if not giadien or not gianuoc:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập đầy đủ giá điện và giá nước!")
            return

        # Kiểm tra phải là số
        try:
            giadien = float(giadien)
            gianuoc = float(gianuoc)
        except ValueError:
            QMessageBox.warning(self, "Thông báo", "Giá điện và giá nước phải là số!")
            return

        # để không lấy dấu . đăng sau
        giadien = int(giadien) if giadien.is_integer() else giadien
        gianuoc = int(gianuoc) if gianuoc.is_integer() else gianuoc

        data = {"giadien": giadien, "gianuoc": gianuoc}
        with open("data/price.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Reload giá lên dashboard của Admin
        self.admin.update_price_stats()

        QMessageBox.information(self, "Thông báo", "Cập nhật giá thành công!")
        self.close()

    def handle_edit_eIndex(self):
        if not self.is_editing:
            self.enable_edit_eIndex()
            self.btn_capnhat3.setText("Cập nhật")
            self.is_editing = True
        else:
            self.update_eIndex_json()
            self.disable_edit_eIndex()
            self.is_editing = False
    
    def enable_edit_eIndex(self):
        for w in [self.lne_sophong6, self.lne_khachthue1, self.lne_thangnam1,
                  self.lne_csdiencu1, self.lne_csdienmoi1, self.lne_csnuoccu1, self.lne_csnuocmoi1]:
            w.setReadOnly(False)
        self.txt_lydo1.setReadOnly(False)
    
    def disable_edit_eIndex(self):
        for w in [self.lne_sophong6, self.lne_khachthue1, self.lne_thangnam1,
                  self.lne_csdiencu1, self.lne_csdienmoi1, self.lne_csnuoccu1, self.lne_csnuocmoi1]:
            w.setReadOnly(True)
        self.txt_lydo1.setReadOnly(True)

    def update_eIndex_json(self):
        room_id = self.lne_sophong6.text()
        with open("data/eIndex.json", "r", encoding="utf-8") as f:
            eIndex = json.load(f)
        for i, r in enumerate(eIndex):
            if r["phong"] == room_id:
                eIndex[i] = {
                   "phong": room_id,
                   "khachthue": self.lne_khachthue1.text(),
                   "thangnam": self.lne_thangnam1.text(),
                   "dien_cu": self.lne_csdiencu1.text(),
                   "dien_moi": self.lne_csdienmoi1.text(),
                   "nuoc_cu": self.lne_csnuoccu1.text(),
                   "nuoc_moi": self.lne_csnuocmoi1.text(),
                   "lydo": self.txt_lydo1.toPlainText()
                   }
                break
            
        with open("data/eIndex.json", "w", encoding="utf-8") as f:
            json.dump(eIndex, f, ensure_ascii=False, indent=4)
        
        self.admin.load_table_json(self.admin.tableWidget_eIndex,"data/eIndex.json","eindex")
        QMessageBox.information(self, "Thông báo", "Chỉnh sửa thành công!")
        self.close()

    # luôn tự reset giá cũ lên form
    def fix_old_price(self):
        try:
            with open("data/price.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            giadiencu = data.get("giadien", "")
            gianuoccu = data.get("gianuoc", "")

            # Set giá cũ lên UI
            self.lne_giadiencu.setText(str(giadiencu))
            self.lne_gianuoccu.setText(str(gianuoccu))

            # Không cho sửa
            self.lne_giadiencu.setReadOnly(True)
            self.lne_gianuoccu.setReadOnly(True)

            # Focus vào ô nhập giá mới
            self.lne_giadienmoi.setFocus()

        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không đọc được file giá!\n{e}")

        