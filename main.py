# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 11:33:56 2026

@author: ThanhHa
"""

from PyQt6.QtWidgets import QApplication,QMainWindow
from QuanLyPhongTro_Ext import *
import sys

app=QApplication(sys.argv)
w=Login()
w.show()
sys.exit(app.exec())