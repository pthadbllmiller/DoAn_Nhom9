# -*- coding: utf-8 -*-
import json
from datetime import date
 
 
class RevenueService:
    
    def open_revenue_detail(self, row):
        from addInfo_ext import addInfo
 
        thangnam = self.tableWidget_Revenue.item(row, 0).text()
 
        # Tính tổng từ bills.json theo tháng
        try:
            with open("data/bills.json", "r", encoding="utf-8") as f:
                bills = json.load(f)
        except Exception as e:
            print(f"[ERROR] Lỗi đọc bills.json: {e}")
            return
 
        tienphong = tiendien = tiennuoc = phivesinh = phiguixe = phiwifi = phikhac = 0
 
        for b in bills:
            if b.get("thangnam") == thangnam and b.get("trangthai") == "Đã thanh toán":
                tienphong += int(b.get("tienphong", 0) or 0)
                tiendien  += int(b.get("tiendien",  0) or 0)
                tiennuoc  += int(b.get("tiennuoc",  0) or 0)
                phivesinh += int(b.get("phivesinh", 0) or 0)
                phiguixe  += int(b.get("phiguixe",  0) or 0)
                phiwifi   += int(b.get("phiwifi",   0) or 0)
                phikhac   += int(b.get("phikhac",   0) or 0)
 
        tong = tienphong + tiendien + tiennuoc + phivesinh + phiguixe + phiwifi + phikhac
 
        def fmt(so):
            return f"{int(so):,}".replace(",", ".")
 
        self.info_window = addInfo(self)
        self.info_window.stackedWidget.setCurrentIndex(16)  # page_81
 
        self.info_window.lne_thangnam6.setText(thangnam)
        self.info_window.lne_ttienphong1.setText(fmt(tienphong))
        self.info_window.lne_ttiendien1.setText(fmt(tiendien))
        self.info_window.lne_ttiennuoc1.setText(fmt(tiennuoc))
        self.info_window.lne_tphivs1.setText(fmt(phivesinh))
        self.info_window.lne_tphigiuxe1.setText(fmt(phiguixe))
        self.info_window.lne_tongphiwifi1.setText(fmt(phiwifi))
        self.info_window.lne_phikhac15.setText(fmt(phikhac))
        self.info_window.lne_tong1.setText(fmt(tong))
 
        self.info_window.show()
    def load_revenue(self):
        try:
            with open("data/bills.json", "r", encoding="utf-8") as f:
                bills = json.load(f)
        except:
            return
 
        from collections import defaultdict
        monthly = defaultdict(lambda: {'tienphong':0,'tiendien':0,'tiennuoc':0,'khac':0})
 
        for b in bills:
            if b.get('trangthai','') == 'Đã thanh toán':
                thang = b.get('thangnam','')
                monthly[thang]['tienphong'] += int(b.get('tienphong', 0))
                monthly[thang]['tiendien']  += int(b.get('tiendien',  0))
                monthly[thang]['tiennuoc']  += int(b.get('tiennuoc',  0))
                monthly[thang]['khac']      += (
                    int(b.get('phivesinh', 0)) +
                    int(b.get('phiguixe',  0)) +
                    int(b.get('phiwifi',   0)) +
                    int(b.get('phikhac',   0))
                )
 
        table = self.tableWidget_Revenue
        table.setRowCount(0)
 
        tong_nam = 0
        thang_hien_tai = f"{date.today().month}/{date.today().year}"
 
        for thang in sorted(monthly.keys()):
            v    = monthly[thang]
            tp   = v['tienphong']
            td   = v['tiendien']
            tn   = v['tiennuoc']
            tong = tp + td + tn + v['khac']
            tong_nam += tong
 
            row = table.rowCount()
            table.insertRow(row)
            for col, val in enumerate([thang, self.fmt(tp), self.fmt(td), self.fmt(tn), self.fmt(tong)]):
                table.setItem(row, col, self.create_item(val))
 
        self.update_revenue_stats(monthly, tong_nam, thang_hien_tai)
 
    def fmt(self, so):
        return f"{int(so):,}".replace(",", ".")
 
    def update_revenue_stats(self, monthly, tong_nam, thang_hien_tai):
        # Dùng tháng hiện tại nếu có, không thì dùng tháng gần nhất
        if thang_hien_tai in monthly:
            v = monthly[thang_hien_tai]
        elif monthly:
            v = monthly[sorted(monthly.keys())[-1]]
        else:
            return
 
        tong_thang = v['tienphong'] + v['tiendien'] + v['tiennuoc'] + v['khac']
 
        # Dashboard
        self.lne_db_doanhthu.setText(self.fmt(tong_thang))
 
        # Trang báo cáo
        self.lne_doanhthu_month.setText(self.fmt(tong_thang))
        self.lne_doanhthu_year.setText(self.fmt(tong_nam))
        self.lne_sumBillRoom.setText(self.fmt(v['tienphong']))
        self.lne_sumBillE.setText(self.fmt(v['tiendien']))
 
        try:
            self.lne_sumBillW.setText(self.fmt(v['tiennuoc']))
        except:
            pass
        try:
            self.lne_otherCost.setText(self.fmt(v['khac']))
        except:
            pass