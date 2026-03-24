# -*- coding: utf-8 -*-
"""
contract_ext.py
Chứa Contract — tất cả logic liên quan đến quản lý Hợp Đồng.
Được kế thừa bởi class Admin trong QuanLyPhongTro_Ext.py
"""

import json
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from PyQt6.QtCore import QDate



class ContractService:

    # ======================================== MỞ THÔNG TIN HỢP ĐỒNG CHI TIẾT ========================================
    def open_contract_detail(self, row):
        from fix_contract_ext import fix_Contract  # import ở đây để tránh circular import

        contract_id = self.tableWidget_Contract.item(row, 0).text()

        with open("data/contracts.json", "r", encoding="utf-8") as f:
            contracts = json.load(f)

        for c in contracts:
            if c["maHD"] == contract_id:
                self.info_window = fix_Contract(self)
                self.info_window.stackedWidget.setCurrentIndex(2)

                # thông tin đầu hợp đồng
                self.info_window.lne_mahopdong_2.setText(c.get("maHD", ""))
                self.info_window.lne_sophong_2.setText(c.get("sophong", ""))
                self.info_window.lne_dientich_2.setText(str(c.get("dientich", "")))
                self.info_window.lne_mucdich_2.setText(c.get("mucdich", ""))

                ngaytao_str = c.get("ngaytao", "")
                if ngaytao_str:
                    qdate_ngaytao = QDate.fromString(ngaytao_str, "dd/MM/yyyy")
                    if qdate_ngaytao.isValid():
                        self.info_window.date_ngaytao_2.setDate(qdate_ngaytao)

                # người thuê
                nguoithue = c.get("nguoithue", {})
 
                hoten   = c.get("hoten",    "") or nguoithue.get("hoten",    "")
                gioitinh= c.get("gioitinh", "") or nguoithue.get("gioitinh", "")
                ngaysinh= c.get("ngaysinh", "") or nguoithue.get("ngaysinh", "")
                cccd    = c.get("cccd",     "") or nguoithue.get("cccd",     "")
                diachi  = c.get("diachi",   "") or nguoithue.get("diachi",   "")
 
                self.info_window.lne_hoten_4.setText(hoten)
                self.info_window.cbo_gioitinh_3.setCurrentText(gioitinh)
                self.info_window.lne_cccd_3.setText(cccd)
                self.info_window.lne_dcthuongtru_4.setText(diachi)
 
                if ngaysinh:
                    d = QDate.fromString(ngaysinh, "dd/MM/yyyy")
                    if d.isValid():
                        self.info_window.date_namsinh_4.setDate(d)
 
                self.info_window.cbo_trangthai_2.setCurrentText(c.get("trangthai", ""))
 
                ngaybd_str = c.get("ngaybd", "")
                if ngaybd_str:
                    d = QDate.fromString(ngaybd_str, "dd/MM/yyyy")
                    if d.isValid():
                        self.info_window.date_ngaybd_2.setDate(d)
 
                ngaykt_str = c.get("ngaykt", "")
                if ngaykt_str:
                    d = QDate.fromString(ngaykt_str, "dd/MM/yyyy")
                    if d.isValid():
                        self.info_window.date_ngaykt_2.setDate(d)
 
                self.info_window.lne_giathue_2.setText(str(c.get("giathue", "")))
                self.info_window.lne_tiencoc_2.setText(str(c.get("tiencoc", "")))
                self.info_window.lne_ngaythanhtoan_2.setText(c.get("ngaythanhtoan", ""))
                self.info_window.lne_htthanhtoan_2.setText(c.get("hinhthucthanhtoan", ""))
 
                self.info_window.show()
                self.info_window.disable_edit_contract()
                return

    def update_contract_stats(self):
        total = self.tableWidget_Contract.rowCount()
        active = 0
        pending = 0
        expiring = 0

        for row in range(total):
            item = self.tableWidget_Contract.item(row, 3)  # cột trạng thái
            if item:
                status = item.text().strip().lower()

                if status == "có hiệu lực":
                    active += 1
                elif status == "đang chờ hiệu lực":
                    pending += 1
                elif status == "sắp hết hạn":
                    expiring += 1

        self.lne_sumContract.setText(str(total))
        self.lne_validContract.setText(str(active))
        self.lne_waitingContract.setText(str(pending))
        self.lne_abtoEContract.setText(str(expiring))