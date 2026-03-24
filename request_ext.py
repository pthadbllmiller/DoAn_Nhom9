# -*- coding: utf-8 -*-
"""
request_ext.py
Chứa REquest — tất cả logic liên quan đến quản lý Phòng.
Được kế thừa bởi class Admin trong QuanLyPhongTro_Ext.py
"""

import json
from PyQt6.QtWidgets import QMainWindow


class RequestService:
# ======================================== MỞ THÔNG TIN PHÒNG CHI TIẾT ========================================
    def open_request_detail(self, row):
        from addInfo_ext import addInfo  # import ở đây để tránh circular import

        room_id = self.tableWidget_Request.item(row, 0).text()

        with open("data/requests.json", "r", encoding="utf-8") as f:
            requests = json.load(f)

        for r in requests:
            if r["sophong"] == room_id:
                self.info_window = addInfo(self)
                self.info_window.stackedWidget.setCurrentIndex(11)

                self.info_window.lne_sophong12.setText(r["sophong"])
                self.info_window.lne_tieude1.setText(r["tieude"])
                self.info_window.lne_makhachthue3.setText(r["makh"])
                self.info_window.lne_hoten3.setText(r["khachthue"])
                self.info_window.cbo_trangthai8.setCurrentText(r["trangthai"])
                self.info_window.lne_sdt3.setText(r["sodienthoai"])
                self.info_window.txt_chitietyc1.setPlainText(r.get("chitiet", ""))

                self.info_window.set_read_only_request()
                self.info_window.show()
                return
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# ======================================== CẬP NHẬT THỐNG KÊ REQUEST ========================================
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def update_request_stats(self):
        total = self.tableWidget_Request.rowCount()
        done = 0
        doing = 0
        notDone_yet=0

        for row in range(total):
            item = self.tableWidget_Request.item(row, 3)
            if item:
                status = item.text().strip()
                if status.lower() == "đã xử lý":
                    done += 1
                elif status.lower()=="chưa xử lý":
                    notDone_yet += 1
                else:
                    doing+=1

        self.lne_sumRequest.setText(str(total))
        self.lne_doneRequest.setText(str(done))
        self.lne_doingRequest.setText(str(doing))
        self.lne_notRequest.setText(str(notDone_yet))
        self.lne_db_request.setText(str(notDone_yet))
        

