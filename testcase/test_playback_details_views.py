#! python3
import requests
import unittest
import configure
import comm_method

'''
对直播回放观看权限进行判断（/live/view/）
    16301：已付费
    16302：密码正确
    16303：会员类型正确
    16321：未付费（在权限在test_live_details_payment.py已经验证）
    16322：密码错误
    16323：需要购买会员类型
    16324：需要购买其它会员类型
    16331：未登录
'''

class LiveDetailsViews(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        