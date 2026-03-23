# -*- coding: utf-8 -*-
import json
from PyQt6.QtWidgets import  QMessageBox

class addInfo_eIndex:
    
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

    # ======================== CẬP NHẬT GIÁ ĐIỆN NƯỚC ========================
    def update_price(self):
        giadien = self.lne_giadienmoi.text().strip()
        gianuoc = self.lne_gianuocmoi.text().strip()
        
        
        data = {"giadien": giadien, "gianuoc": gianuoc}
        with open("data/price.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
 
        # Reload giá lên dashboard của Admin
        self.load_price_dashboard()
        self.info_window.lne_giadiencu.setText(self.lne_eCost.text())
        self.info_window.lne_gianuoccu.setText(self.lne_wCost.text())
        
        QMessageBox.information(self, "Thông báo", "Cập nhật giá thành công!")
        self.close()
        