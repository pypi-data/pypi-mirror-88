# -*- coding:utf-8 -*- 

import os
import codecs

__version__ = codecs.open(os.path.join(os.path.dirname(__file__), 'VERSION.txt')).read()
__author__ = 'ly_peppa'
__email__ = 'iseu1130@sina.cn'

from bilibilirank.crawl import PopularTop100
from bilibilirank.crawl import PopularRank
from bilibilirank.crawl import PopularHot
from bilibilirank.crawl import PopularHistory
from bilibilirank.crawl import PopularWeekly