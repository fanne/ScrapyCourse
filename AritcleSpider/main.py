# -*- coding:utf-8 -*-

__Author__ = '7zGame Fanne'
__Date__ = '2017/8/22 16:59'


import sys
import os
from scrapy.cmdline import execute
# 调用execute可以执行scrapy脚本

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "jobbole"])
execute(["scrapy", "crawl", "zhihu"])

