import json
import os
from PyQt6.QtWidgets import QMessageBox


class addInfo_Contract:
    def add_contract(self):
        # lấy thông tin người dùng
        ma_hd = self.lne_mahopdong_3.text().strip()
        ngaytao = self.date_ngaytao_3.date().toString("dd/MM/yyyy")
        so_phong = self.lne_sophong_3.text().strip()
        dien_tich = self.lne_dientich_3.text().strip()
        muc_dich = self.lne_mucdich_3.text().strip()
        trangthai = self.cbo_trangthai_3.currentText(),

        ho_ten = self.lne_hoten_5.text().strip()
        gioi_tinh = self.cbo_gioitinh_6.currentText()
        ngaysinh = self.date_namsinh_5.date().toString("dd/MM/yyyy")
        cccd = self.lne_cccd_6.text().strip()
        dia_chi = self.lne_dcthuongtru_5.text().strip()

        ngaybd = self.date_ngaybd_3.date().toString("dd/MM/yyyy")
        ngaykt = self.date_ngaykt_3.date().toString("dd/MM/yyyy")
        gia_thue = self.lne_giathue_3.text().strip()
        tien_coc = self.lne_tiencoc_3.text().strip()
        ngay_thanh_toan = self.lne_ngaythanhtoan_3.text().strip()
        hinh_thuc_tt = self.lne_htthanhtoan_3.text().strip()



        # kiểm tra dữ liệu rỗng
        if not ma_hd:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập mã hợp đồng!")
            return
        if not so_phong:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập số phòng!")
            return
        if not dien_tich:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập diện tích!")
            return
        if not ho_ten:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập họ tên người thuê!")
            return
        if not cccd:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập số CCCD người thuê!")
            return
        if not gia_thue:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập giá thuê!")
            return
        if not tien_coc:
            QMessageBox.warning(self, "Thông báo", "Vui lòng nhập tiền cọc!")
            return

        contracts = []
        if os.path.exists("data/contracts.json"):
            try:
                with open("data/contracts.json", "r", encoding="utf-8") as f:
                    contracts = json.load(f)
            except Exception:
                contracts = []

        # trùng mã hợp đồng
        if any(c.get("maHD") == ma_hd for c in contracts):
            QMessageBox.warning(self, "Thông báo", "Mã hợp đồng đã tồn tại! Vui lòng nhập mã khác.")
            self.lne_mahopdong_3.setFocus()
            self.lne_mahopdong_3.selectAll()
            return

        # trùng số phòng với hợp đồng còn hiệu lực
        if any(c.get("sophong") == so_phong and c.get("trangthai", "").strip().lower() == "có hiệu lực"
            for c in contracts):
            QMessageBox.warning(self, "Thông báo", "Phòng này đã có hợp đồng còn hiệu lực!")
            self.lne_sophong_3.setFocus()
            self.lne_sophong_3.selectAll()
            return

        contract = {
            "maHD": ma_hd,
            "ngaytao": ngaytao,
            "sophong": so_phong,
            "dientich": dien_tich,
            "mucdich": muc_dich,
            "trangthai": trangthai,
            "makh": "",
            "hoten": ho_ten,
            "gioitinh": gioi_tinh,
            "ngaysinh": ngaysinh,
            "cccd": cccd,
            "diachi": dia_chi,
            "ngaybd": ngaybd,
            "ngaykt": ngaykt,
            "giathue": gia_thue,
            "tiencoc": tien_coc,
            "ngaythanhtoan": ngay_thanh_toan,
            "hinhthucthanhtoan": hinh_thuc_tt}

        contracts.append(contract)
        # ghi dữ liệu xuống file json
        with open("data/contracts.json", "w", encoding="utf-8") as f:
            json.dump(contracts, f, ensure_ascii=False, indent=4)

        # reload bảng
        self.admin.loadTables()
        # cập nhật lại trên dashboard
        self.admin.update_contract_stats()
        QMessageBox.information(self, "Thông báo", "Thêm hợp đồng thành công!")
        self.close()

    def handle_edit_contract(self):
        if not self.is_editing:
            self.enable_edit_contract()
            self.btn_capnhat_2.setText("Cập nhật")
            self.is_editing = True
        else:
            self.update_contract_json()
            self.disable_edit_contract()
            self.btn_capnhat_2.setText("Chỉnh sửa")
            self.is_editing = False

   # hàm có thể chỉnh sửa
    def enable_edit_contract(self):
        # thông tin hợp đồng
        for lne in [
            self.lne_mahopdong_2,
            self.lne_sophong_2,
            self.lne_dientich_2,
            self.lne_mucdich_2,
            self.lne_hoten_4,
            self.lne_cccd_3,
            self.lne_cccd_4,
            self.lne_dcthuongtru_3,
            self.lne_dcthuongtru_4,
            self.lne_stk_2,
            self.lne_giathue_2,
            self.lne_tiencoc_2,
            self.lne_ngaythanhtoan_2,
            self.lne_htthanhtoan_2
        ]:
            lne.setReadOnly(False)

        for cbo in [
            self.cbo_gioitinh_4,
            self.cbo_trangthai_2,
            self.date_ngaytao_2,
            self.date_namsinh_3,
            self.date_namsinh_4,
            self.date_ngaybd_2,
            self.date_ngaykt_2
        ]:
            cbo.setEnabled(True)

    # hàm không cho chỉnh sửa
    def disable_edit_contract(self):
        # thông tin hợp đồng
        for lne in [
            self.lne_mahopdong_2,
            self.lne_sophong_2,
            self.lne_dientich_2,
            self.lne_mucdich_2,
            self.lne_hoten_4,
            self.lne_cccd_3,
            self.lne_cccd_4,
            self.lne_dcthuongtru_3,
            self.lne_dcthuongtru_4,
            self.lne_stk_2,
            self.lne_giathue_2,
            self.lne_tiencoc_2,
            self.lne_ngaythanhtoan_2,
            self.lne_htthanhtoan_2
        ]:
            lne.setReadOnly(True)

        for cbo in [
            self.cbo_gioitinh_4,
            self.cbo_trangthai_2,
            self.date_ngaytao_2,
            self.date_namsinh_3,
            self.date_namsinh_4,
            self.date_ngaybd_2,
            self.date_ngaykt_2
        ]:
            cbo.setEnabled(False)

    # xoá hợp đồng
    def delete_contract(self):
        contract_id = self.lne_mahopdong_2.text().strip()

        reply = QMessageBox.question(self, "Xác nhận xoá", f"Bạn có chắc chắn muốn xoá hợp đồng {contract_id} không?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.No:
            return

        with open("data/contracts.json", "r", encoding="utf-8") as f:
            contracts = json.load(f)

       # xoá bằng cách chỉ giữ lại những hợp đồng không phải là hợp đồng đã chọn
        new_contracts = []
        for c in contracts:
            if c.get("maHD") != contract_id:
                new_contracts.append(c)

        with open("data/contracts.json", "w", encoding="utf-8") as f:
            json.dump(contracts, f, ensure_ascii=False, indent=4)

        QMessageBox.information(self, "Thông báo", "Huỷ hợp đồng thành công!")
        self.close()
        self.admin.loadTables()
        self.admin.update_contract_stats()


    def update_contract_json(self):
        contract_id = self.lne_mahopdong_2.text()

        with open("data/contracts.json", "r", encoding="utf-8") as f:
            contracts = json.load(f)

        for i, c in enumerate(contracts):
            if c["maHD"] == contract_id:
                contracts[i] = {
                    "maHD": contract_id,
                    "ngaytao": self.date_ngaytao_2.date().toString("dd/MM/yyyy"),
                    "sophong": self.lne_sophong_2.text(),
                    "dientich": self.lne_dientich_2.text(),
                    "mucdich": self.lne_mucdich_2.text(),
                    "trangthai": self.cbo_trangthai_2.currentText(),
                    "nguoithue": {
                        "makh": c.get("nguoithue", {}).get("makh", ""),
                        "hoten": self.lne_hoten_4.text(),
                        "gioitinh": self.cbo_gioitinh_4.currentText(),
                        "ngaysinh": self.date_namsinh_4.date().toString("dd/MM/yyyy"),
                        "cccd": self.lne_cccd_3.text(),
                        "diachi": self.lne_dcthuongtru_4.text()
                    },
                    "ngaybd": self.date_ngaybd_2.date().toString("dd/MM/yyyy"),
                    "ngaykt": self.date_ngaykt_2.date().toString("dd/MM/yyyy"),
                    "giathue": self.lne_giathue_2.text(),
                    "tiencoc": self.lne_tiencoc_2.text(),
                    "ngaythanhtoan": self.lne_ngaythanhtoan_2.text(),
                    "hinhthucthanhtoan": self.lne_htthanhtoan_2.text()
                }
                break

        # tiếp tục lưu xuống file
        with open("data/contracts.json", "w", encoding="utf-8") as f:
            json.dump(contracts, f, ensure_ascii=False, indent=4)

        QMessageBox.information(self, "Thông báo", "Chỉnh sửa hợp đồng thành công!")
        self.close()
        self.admin.loadTables()
        self.admin.update_contract_stats()

