# -*- coding: utf-8 -*-

import json
import os
from PyQt6.QtWidgets import  QMessageBox

class addInfo_Room:
    def add_room(self):
        so_phong = self.lne_sophong1.text().strip()
        gia=self.lne_giathue1.text()
        dientich=self.lne_dientich1.text()
        
        if not so_phong:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập số phòng!")
            return
        if not gia:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập giá phòng!")
            return
        if not dientich:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập diện tích phòng!")
            return
        
        # Kiểm tra trùng mã phòng
        if os.path.exists("data/rooms.json"):
            with open("data/rooms.json", "r", encoding="utf-8") as f:
                rooms = json.load(f)
            if any(r["phong"] == so_phong for r in rooms):
                QMessageBox.warning(self, "Trùng mã phòng! Vui lòng nhập mã khác")
                self.lne_sophong1.setFocus()
                self.lne_sophong1.selectAll()
                return

        room = {
            "phong":             so_phong,
            "loai":              self.cbo_loaiphong1.currentText(),
            "dientich":          dientich,
            "gia":               gia,
            "trangthai":         self.cbo_trangthai1.currentText(),
            "tienich":           self.txt_tienich1.toPlainText().strip(),
            "ghichu":            self.txt_mota1.toPlainText().strip(),
            "nguoiphutrach":     "",
            "thongtinkhachthue": "",
            "mota":              self.txt_mota1.toPlainText().strip()
        }
        # Gọi inset_row_table của Admin()
        self.admin.insert_row_table(
            self.admin.tableWidget_Room,
            room,
            "data/rooms.json",
            "room"
        )
        
        self.admin.update_room_stats()
        QMessageBox.information(self, "Thông báo", "Thêm phòng thành công!")
        self.close()
    
    def handle_edit_room(self):
        if not self.is_editing:
            self.enable_edit_room()
            self.btn_chinhsua1.setText("Cập nhật")
            self.is_editing = True
        else:
            self.update_room_json()
            self.disable_edit_room()
            self.btn_chinhsua1.setText("Chỉnh sửa")
            self.is_editing = False
    
    def enable_edit_room(self):
        for w in [self.lne_sophong2, self.lne_loaiphong2,
                  self.lne_dientich2, self.lne_giathue2, self.lne_nguoiphutrach1]:
            w.setReadOnly(False)
        self.cbo_trangthai2.setEnabled(True)
        self.txt_mota2.setReadOnly(False)
        self.txt_tienich2.setReadOnly(False)
        self.txt_ttkhachthue1.setReadOnly(False)
    
    def disable_edit_room(self):
        for w in [self.lne_sophong2, self.lne_loaiphong2,
                  self.lne_dientich2, self.lne_giathue2, self.lne_nguoiphutrach1]:
            w.setReadOnly(True)
        self.cbo_trangthai2.setEnabled(False)
        self.txt_mota2.setReadOnly(True)
        self.txt_tienich2.setReadOnly(True)
        self.txt_ttkhachthue1.setReadOnly(True)
        
    def update_room_json(self):
        room_id = self.lne_sophong2.text()
        with open("data/rooms.json", "r", encoding="utf-8") as f:
            rooms = json.load(f)
        for i, r in enumerate(rooms):
            if r["phong"] == room_id:
                rooms[i] = {
                    "phong":              room_id,
                    "loai":               self.lne_loaiphong2.text(),
                    "dientich":           self.lne_dientich2.text(),
                    "gia":                self.lne_giathue2.text(),
                    "trangthai":          self.cbo_trangthai2.currentText(),
                    "nguoiphutrach":      self.lne_nguoiphutrach1.text(),
                    "thongtinkhachthue":  self.txt_ttkhachthue1.toPlainText(),
                    "mota":               self.txt_mota2.toPlainText(),
                    "tienich":            self.txt_tienich2.toPlainText()
                }
                break
            
        with open("data/rooms.json", "w", encoding="utf-8") as f:
            json.dump(rooms, f, ensure_ascii=False, indent=4)
        QMessageBox.information(self, "Thông báo", "Chỉnh sửa phòng thành công!")
        self.close()
        self.admin.load_table_json(self.admin.tableWidget_Room,"data/rooms.json","room")
        self.admin.update_room_stats()
        
        