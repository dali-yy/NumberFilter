# -*- coding: utf-8 -*-
# @Time : 2022/7/14 6:35
# @Author : XXX
# @Site : 
# @File : test.py
# @Software: PyCharm
import re

pattern = (r'\d{1,2} '*4).strip()
print(re.search(pattern, '01 02 03  04 05 06'))