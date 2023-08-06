# -*- coding: utf-8 -*-
"""淘宝卖家商品类目，获取第五级类目"""
from wpt_taobaocategory.config.taobao_settings import cookie

class TaoBaoThree(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ZH-cn,zh;q=0.9",
            "cookie": cookie,
            "referer": "https://item.upload.taobao.com/router/publish.htm?spm=a211vu.server-web-home.favorite.d48.64f02D58WL0EGD",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "mozilla/5.0 (macintosH; intEl MAC OS X 10_15_7) apPleWebKit/537.36 (KHTMl, liKe geckO) chrome/87.0.4280.88 safari/537.36",
        }
        super(TaoBaoThree, self).__init__()

    def get_token(self):
        """
        获取渠道所需auth或cookie
        :return:
        """
        return ""

    def structure_params(self, params):
        """
        构造参数&请求url
        :param params: 请求需要的参数
        :return:
        """
        self.params = params
        cateid = self.params.get("category_id")
        next_page = self.params.get("next_page")
        if next_page:
            kwargs = {
                "url": 'https://item.upload.taobao.com/router/asyncOpt.htm?optType=taobaoBrandSelectQuery&queryType=more&catId={}&index={}&size=100'.format(cateid, next_page),
                "method": "get",
                "headers": self.headers,
                "session": False,
                "verify": False,
            }
        else:
            kwargs = {
                "url": 'https://item.upload.taobao.com/router/asyncOpt.htm?optType=categorySelectChildren&catId={}'.format(cateid),
                "method": "get",
                "headers": self.headers,
                "session": False,
                "verify": False,
            }

        return kwargs

    def check_response(self, response):
        """
        检查响应是否正确
        :param response: 响应体
        :return:
        """
        if response.status_code == "200":
            if response.json.get("success") == True:
                return True
        return False

    def parse_response(self, response):
        """
        解析响应结果,获取所需字段
        :return:
        """
        result_list = []
        next_page = self.params.get("next_page")
        categoryone = self.params.get("categoryone")
        categorytwo = self.params.get("categorytwo")
        categorythree = self.params.get("categorythree")
        categoryfour = self.params.get("categoryfour")
        cateid = self.params.get("category_id")
        data = response.json()
        catefive_list = data.get("data", {}).get("dataSource")
        # TODO 判断是否是第一页，并判断是否有下一页
        is_first = True if data.get("data", {}).get("label") else False
        if is_first:
            next_page = 2 if len(catefive_list) >= 50 else 0
        else:
            next_page = (int(next_page) + 1) if len(catefive_list) >= 100 else 0
        for catefive in catefive_list:
            catefive_name = catefive.get("name")
            catefive_id = catefive.get("id")
            hasleaf = True if catefive.get("leaf") == False else False
            final_url = None
            if hasleaf:
                callback = "TaoBaoFour"
            else:
                callback = "TaoBaoFour"
                final_url = "https://item.upload.taobao.com/router/" + catefive.get("action", {}).get("url")
            result_list.append({
                "categoryone": categoryone,
                "categorytwo": categorytwo,
                "categorythree": categorythree,
                "categoryfour": categoryfour,
                "categoryfive": catefive_name,
                "category_id": catefive_id,
                "callback": callback,
                "final_url": final_url
            })
        self.params["result_list"] = result_list
        if next_page == 0:
            return self.params
        else:
            self.params["next_page"] = {
                "categoryone": categoryone,
                "categorytwo": categorytwo,
                "categorythree": categorythree,
                "categoryfour": categoryfour,
                "category_id": cateid,
                "callback": "TaoBaoThree",
                "next_page": next_page
            }
            return self.params
