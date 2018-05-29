
from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))#调用主目录
execute(["scrapy","crawl","jobbole"])
