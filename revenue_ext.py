# -*- coding: utf-8 -*-
import json
from datetime import date
 
 
class RevenueService:
 
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