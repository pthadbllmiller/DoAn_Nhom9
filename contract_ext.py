# -*- coding: utf-8 -*-
"""
contract_ext.py
Chứa Contract — tất cả logic liên quan đến quản lý Hợp Đồng.
Được kế thừa bởi class Admin trong QuanLyPhongTro_Ext.py
"""

import json
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from addInfo import Ui_AddInfo

class ContractService:

    # ======================================== MỞ THÔNG TIN HỢP ĐỒNG CHI TIẾT ========================================
    def open_contract_detail(self, row):
        from QuanLyPhongTro_Ext import fix_Contract  # import cục bộ tránh circular

        def get_text(r, col):
            item = self.tableWidget_Contract.item(r, col)
            return item.text() if item else ""

        contract_data = {
            "mahd":    get_text(row, 0),
            "makh":    get_text(row, 1),
            "phong":   get_text(row, 2),
            "ngaybd":  get_text(row, 3),
            "ngaykt":  get_text(row, 4),
        }

        self.fc = fix_Contract(self, contract_data)
        self.fc.show()
        
    def update_contract_stats(self):
        total = self.tableWidget_Contract.rowCount()
        self.lne_sumContract.setText(str(total))