# -*- coding: utf-8 -*-
"""
room_ext.py
Chứa Room — tất cả logic liên quan đến quản lý Phòng.
Được kế thừa bởi class Admin trong QuanLyPhongTro_Ext.py
"""
import json
from PyQt6.QtWidgets import QMessageBox, QMainWindow


class RoomService:
# ======================================== MỞ THÔNG TIN PHÒNG CHI TIẾT ========================================
    def open_room_detail(self, row):
        from addInfo_ext import addInfo  # import ở đây để tránh circular import

        room_id = self.tableWidget_Room.item(row, 0).text()

        with open("data/rooms.json", "r", encoding="utf-8") as f:
            rooms = json.load(f)

        for r in rooms:
            if r["phong"] == room_id:
                self.info_window = addInfo(self)
                self.info_window.stackedWidget.setCurrentIndex(1)

                self.info_window.lne_sophong2.setText(r["phong"])
                self.info_window.lne_loaiphong2.setText(r["loai"])
                self.info_window.lne_dientich2.setText(r["dientich"])
                self.info_window.lne_giathue2.setText(r["gia"])
                self.info_window.cbo_trangthai2.setCurrentText(r["trangthai"])
                self.info_window.lne_nguoiphutrach1.setText(r.get("nguoiphutrach", ""))
                self.info_window.txt_ttkhachthue1.setPlainText(r.get("thongtinkhachthue", ""))
                self.info_window.txt_mota2.setPlainText(r.get("mota", ""))
                self.info_window.txt_tienich2.setPlainText(r.get("tienich", ""))


                self.info_window.disable_edit_room()
                self.info_window.btn_chinhsua1.clicked.connect(self.info_window.handle_edit_room)
                
                self.info_window.show()
                return
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# ======================================== CẬP NHẬT THỐNG KÊ PHÒNG ========================================
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def update_room_stats(self):
        total = self.tableWidget_Room.rowCount()
        rented = 0
        empty = 0

        for row in range(total):
            item = self.tableWidget_Room.item(row, 4)
            if item:
                status = item.text().strip()
                if status.lower() == "đã cho thuê":
                    rented += 1
                else:
                    empty += 1

        self.lne_sumRoom.setText(str(total))
        self.lne_room_dangthue.setText(str(rented))
        self.lne_db_room_dangthue.setText(str(rented))
        self.lne_db_room_trong.setText(str(empty))
        self.lne_phongTrong.setText(str(empty))
        


