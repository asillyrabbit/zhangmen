#! python3
import requests
import unittest
import configure
import comm_method
import json
import time

'''
打开直播回放详情页，对各接口返回进行检查
特别是观看权限判断（/live/view/）
    16301：已付费
    16302：密码正确
    16303：会员类型正确
    16321：未付费
    16322：密码错误
    16323：需要购买会员类型
    16324：需要购买其它会员类型
    16331：未登录
'''


class PlaybackDetailsPayment(unittest.TestCase):
    @classmethod
    # 测试数据准备，指定群，指定直播,指定测试账号
    def setUpClass(self):
        self.sharerId = '30440d615c5e5df1eb647c'
        self.circleId = '35505815cd6b34287-7fe7'
        self.liveId = '1872763'
        self.user_info = comm_method.get_user_info('18808150000')

    # 打开直播详情页
    def test_a_entry(self):
        api = '/zhangmen/livenumber/share/entry/?sharerId=' + self.sharerId + '&circleId=' + self.circleId + '&liveId=' + self.liveId + '&from=singlemessage&isappinstalled=0'
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + 'erro_info' + res.text
        # 检查价格、试看时长、回放状态
        self.assertIn('price\":0.01', res.text, erro_info)
        self.assertIn('seeTime\":18000', res.text, erro_info)
        self.assertIn('state\":68', res.text, '\n' + erro_info)

        # 打开直播详情页
    def test_b_role(self):
        api = '/api/v2/circle/member/role/?circleId=' + self.circleId + '&userId=' + self.user_info['userId']
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('code\":0', res.text, '\n' + erro_info)

    def test_c_sf(self):
        api = '/api/sf/' + self.user_info['userId'] + '/belong?userId=' + self.user_info['userId'] + '&circleIds=' + self.circleId + '&sfType=1'
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('message\":\"成功', res.text, '\n' + erro_info)

    def test_d_enterRule(self):
        api = '/api/sf/card/enterRule?circleId=' + self.circleId + '&userId=' + self.user_info['userId'] + '&liveId=' + self.liveId + '&bizType=1'
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"code\":1002,\"message\":\"成功\"', res.text,
                      '\n' + erro_info)

    def test_e_circle_attention_status(self):
        api = '/api/zm/weixin/platform/circle_attention_status/?circleId=' + self.circleId + '&userId=' + self.user_info['userId']
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('message\":\"社群、服务号都未关注', res.text, '\n' + erro_info)

    def test_f_element(self):
        api = '/api/statistic/element?bizType=0&srcType=/zhangmen/livenumber/share/entry/&parentId=' + self.sharerId + '&callback=llpoiiu&currentId=' + self.user_info['userId'] + '&circleId=' + self.circleId
        url = configure.protocol + '://' + configure.bang_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('llpoiiu({\"code\":0})', res.text, '\n' + erro_info)

    def test_g_customMenuProxyService(self):
        api = '/restful/customMenuProxyService/custommenu/circleMenuConfig?circleId=35505815cd6b34287-7fe7&pageType=liveDetail'
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('message\":\"成功\",\"result\":{\"liveDetail', res.text,
                      '\n' + erro_info)

    def test_h_cnt(self):
        api = '/api/zm/live/doc/cnt?liveId=' + self.liveId
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"code\":0,\"message\":\"成功\",\"result\":0}', res.text,
                      '\n' + erro_info)

    def test_i_circle_ad_push(self):
        api = '/api/zm/circle/circle-ad-push/?circleId=' + self.circleId + '&type=1&'
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('code\":0,\"message\":\"成功\",\"result\":[]}', res.text,
                      '\n' + erro_info)

    def test_j_info(self):
        api = '/api/v2/circle/info?circleId=' + self.circleId + '&dataType=2'
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('code\":\"90612244\",\"name\":\"小胖子的周末郊游\"', res.text,
                      '\n' + erro_info)

    def test_k_related_live(self):
        api = '/api/zm/live/circle/related-live/?circleId=' + self.circleId + '&pageNo=1&pageSize=15&userId=' + self.user_info['userId'] + '&liveId=' + self.liveId
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('id\":1872763,\"title\":\"【auto】小胖子的付费直播\"', res.text,
                      '\n' + erro_info)

    def test_l_role_detail(self):
        api = '/api/zm/circle/role-detail?circleId=' + self.circleId + '&type=2&userId=' + self.user_info['userId']
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('code\":\"90612244\",\"name\":\"小胖子的周末郊游', res.text,
                      '\n' + erro_info)

    def test_n_getQiniuSign(self):
        api = '/restful/helpProxyService/encrypt/getQiniuSign'
        url = configure.protocol + '://' + configure.zm_host + api

        data = {
            'playbackUrl':
            'http://vod.live.zm518.cn/recordings/z1.gaiay.5b72a770bad7cf1a4088a3ce/0_1534241019.m3u8'
        }

        res = requests.post(url, data, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:post' + '\n' + 'url:' + url + '\nerro_info' + res.text
        sign = res.json()['result']
        self.assertNotEqual('sign=', sign, erro_info)

    def test_m_view(self):
        api = '/api/live/view/?liveId=' + self.liveId + '&dataType=4&circleId=' + self.circleId + '&token=' + self.user_info['token']
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"views\":{\"1872763\":16321},\"code\":0}', res.text,
                      '\n' + erro_info)

    def test_o_doc(self):
        api = '/api/zm/web/live/doc?userId=' + self.user_info['userId'] + '&circleId=' + self.user_info['userId'] + '&pageNo=1&pageSize=15&liveId=' + self.liveId
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('result\":[],\"code\":0,\"message\":\"ok', res.text,
                      '\n' + erro_info)

    def test_p_share(self):
        api = '/api/weixin/share?url=http://m.zm518.cn/zhangmen/livenumber/share/entry/?sharerId=' + self.sharerId + '&circleId=' + self.circleId + '&liveId=' + self.liveId + '&from=singlemessage&isappinstalled=0'
        url = configure.protocol + '://' + configure.zm_host + api

        res = requests.get(url, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"message\":\"成功\"', res.text, '\n' + erro_info)

    def test_q_buriedPoint(self):
        t = round(time.time(), )
        time_param = t * 1000
        api = '/restful/biProxyService/data/buriedPoint'
        url = configure.protocol + '://' + configure.zm_host + api
        headers = {'content-type': 'application/json'}

        params = {
            'category': 'LINK',
            'channel': '',
            'circleId': self.circleId,
            'liveStatus': 'PLAYBACK',
            'watchType': 'CHARGE'
        }

        data = {
            'points': [{
                'action':
                'BROWSE',
                'appOs':
                'H5',
                'appVersion':
                '',
                'category':
                'LIVE',
                'categoryId':
                self.liveId,
                'categoryType':
                'DETAIL',
                'locale':
                'zh-CN',
                'pageRef':
                '',
                'pageUrl':
                'http://m.zm518.cn/zhangmen/livenumber/share/entry/?sharerId='
                + self.sharerId + '&circleId=' + self.circleId + '&liveId=' +
                self.liveId + '&from=singlemessage&isappinstalled=0',
                'params':
                params,
                'platform':
                'ZM',
                'resolution':
                '414*736',
                'title':
                '【auto】小胖子的付费直播',
                'token':
                self.user_info['token'],
                'time':
                time_param
            }],
            't':
            t,
        }

        res = requests.post(url, json.dumps(data), headers=headers)
        res.encoding = 'utf-8'

        erro_info = 'method:post' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"code\":0,\"message\":\"成功\"', res.text,
                      '\n' + erro_info)

    def test_r_statistics(self):
        api = '/api/zm/w/live/statistics'
        url = configure.protocol + '://' + configure.zm_host + api

        data = {
            'circleId': self.circleId,
            'userId': self.user_info['userId'],
            'liveId': self.liveId
        }

        res = requests.post(url, data, headers=configure.headers)
        res.encoding = 'utf-8'

        erro_info = 'method:get' + '\n' + 'url:' + url + '\nerro_info' + res.text
        self.assertIn('{\"message\":\"成功\",\"code\":0}', res.text,
                      '\n' + erro_info)


if __name__ == '__main__':
    unittest.main()
