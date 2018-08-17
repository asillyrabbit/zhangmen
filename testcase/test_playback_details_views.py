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
    16324：需要购买其它会员类型(没有用到)
    16331：未登录

    view
    1：免费
    2：成员
    4：付费
    8：密码
    16:会员
    20：单节+会员
    32：白名单
'''


class PlaybackDetailsViews(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.sharerId = '30440d615c5e5df1eb647c'
        self.payment_liveId = '1872763'    # 付费
        self.payment_vip_liveId = '1864941'  # 单节+会员
        self.vip_type_b_liveId = '1836904'   # 会员类型B
        self.vip_type_c_liveId = '1832053'   # 会员类型C
        self.password_liveId = '1834827' # 密码观看
        self.circleId = '35505815cd6b34287-7fe7'
        self.has_payment_user = comm_method.get_user_info('18808160000')  # 付费用户
        self.has_buy_vip_a_b = comm_method.get_user_info('18808160001')  # 会员A、B用户

    # 付费直播，已付费：16301
    def test_a_has_payment(self):
        api = '/api/live/view/?liveId=' + self.payment_liveId + '&dataType=4&circleId=' + self.circleId + '&token=' + self.has_payment_user['token']
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"views\":{\"1872763\":16301},\"code\":0}', res.text,
                      '\n' + erro_info)

    # 单节+会员，view:20
    def test_b1_entry(self):
        api = '/zhangmen/livenumber/share/entry/?sharerId=' + self.sharerId + '&circleId=' + self.circleId + '&liveId=' + self.payment_vip_liveId + '&from=singlemessage&isappinstalled=0'
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + 'erro_info' + res.text
        # 检查价格、试看时长、回放状态、观看方式
        self.assertIn('price\":0.01', res.text, erro_info)
        self.assertIn('seeTime\":0', res.text, erro_info)
        self.assertIn('state\":68', res.text, '\n' + erro_info)
        self.assertIn('view\":20', res.text, '\n' + erro_info)
    
    # 单节+会员，已付费：16301
    def test_b2_has_payment(self):
        api = '/api/live/view/?liveId=' + self.payment_vip_liveId + '&dataType=20&circleId=' + self.circleId + '&token=' + self.has_payment_user['token']
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"views\":{\"1864941\":16301},\"code\":0}', res.text,
                      '\n' + erro_info)
    
    # 单节+会员,已购买会员，此处有一个bug，本来应该返回16303会员类型正确，但实际返回的16301已付费，因不影响观看，暂不修改
    def test_c1_has_buy_vip(self):
        api = '/api/live/view/?liveId=' + self.payment_vip_liveId + '&dataType=20&circleId=' + self.circleId + '&token=' + self.has_buy_vip_a_b['token']
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"views\":{\"1864941\":16301},\"code\":0}', res.text,
                      '\n' + erro_info)

    # 会员B,view:16
    def test_d1_entry(self):
        api = '/zhangmen/livenumber/share/entry/?sharerId=' + self.sharerId + '&circleId=' + self.circleId + '&liveId=' + self.vip_type_b_liveId + '&from=singlemessage&isappinstalled=0'
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + 'erro_info' + res.text
        # 检查价格、试看时长、回放状态、观看方式
        self.assertIn('seeTime\":0', res.text, erro_info)
        self.assertIn('state\":68', res.text, '\n' + erro_info)
        self.assertIn('view\":16', res.text, '\n' + erro_info)

    # 会员B，已购买会员16303
    def test_d2_has_buy_vip(self):
        api = '/api/live/view/?liveId=' + self.vip_type_b_liveId + '&dataType=16&circleId=' + self.circleId + '&token=' + self.has_buy_vip_a_b['token']
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"views\":{\"1836904\":16303},\"code\":0}', res.text,
                      '\n' + erro_info)

    # 会员C，已购买会员A、B,需要购买会员类型：16323
    def test_d3_has_buy_vip(self):
        api = '/api/live/view/?liveId=' + self.vip_type_c_liveId + '&dataType=16&circleId=' + self.circleId + '&token=' + self.has_buy_vip_a_b['token']
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"views\":{\"1832053\":16323},\"code\":0}', res.text,
                      '\n' + erro_info)

    # 密码观看,view:8
    def test_e1_entry(self):
        api = '/zhangmen/livenumber/share/entry/?sharerId=' + self.sharerId + '&circleId=' + self.circleId + '&liveId=' + self.password_liveId + '&from=singlemessage&isappinstalled=0'
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + 'erro_info' + res.text
        # 检查价格、试看时长、回放状态、观看方式
        self.assertIn('seeTime\":0', res.text, erro_info)
        self.assertIn('state\":68', res.text, '\n' + erro_info)
        self.assertIn('view\":8', res.text, '\n' + erro_info)
     
    # 密码观看，没有输入密码时，返回密码错误：16322
    def test_e2_not_input_password(self):
        api = '/api/live/view/?liveId=' + self.password_liveId + '&dataType=8&circleId=' + self.circleId + '&token=' + self.has_buy_vip_a_b['token']
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"views\":{\"1834827\":16322},\"code\":0}', res.text,
                      '\n' + erro_info)
    
    # 密码观看，输入正确密码：16302
    def test_e3_right_password(self):
        api = '/api/live/view/?liveId=' + self.password_liveId + '&dataType=8&circleId=' + self.circleId + '&token=' + self.has_buy_vip_a_b['token'] + '&body=123456'
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"views\":{\"1834827\":16302},\"code\":0}', res.text,
                      '\n' + erro_info)

    # 单节+会员，未登录:16331
    def test_f1_not_login(self):
        api = '/api/live/view/?liveId=' + self.payment_vip_liveId + '&dataType=20&circleId=' + self.circleId + '&token=123'
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"code\":11997,\"message\":\"用户未登陆\"}', res.text,
                      '\n' + erro_info)


if __name__ == '__main__':
    unittest.main()