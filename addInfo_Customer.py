# -*- coding: utf-8 -*-
class addInfo_Customer:
    def disable_edit_customer(self):
        for w in [self.lne_makhachthue1, self.lne_hoten1,
                  self.lne_ngaysinh1, self.lne_cccd1, self.lne_sophong4, self.lne_sdt1,self.lne_biensoxe1]:
            w.setReadOnly(True)
        self.cbo_gioitinh1.setEnabled(False)
        self.cbo_nguoidaidien1.setEnabled(False)
        self.txt_hkthuongtru1.setReadOnly(True)
        self.txt_ghichu1.setReadOnly(True)


