# -*- coding: utf-8 -*-

import json
import os

class addInfo_Request:
    def set_read_only_request(self):
        for w in [self.lne_tieude1, self.lne_sophong12, self.lne_hoten3,
                  self.lne_makhachthue3, self.lne_sdt3]:
            w.setReadOnly(True)
        self.txt_chitietyc1.setReadOnly(True)
        self.cbo_trangthai8.setEnabled(False)