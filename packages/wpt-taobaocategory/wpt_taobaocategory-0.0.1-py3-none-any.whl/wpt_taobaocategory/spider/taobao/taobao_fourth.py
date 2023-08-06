# -*- coding: utf-8 -*-
"""淘宝卖家商品类目，品牌跳转接口"""
from wpt_taobaocategory.config.taobao_settings import cookie

class TaoBaoFour(object):

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
            "x-requested-with": "XmlhTtprequest",
        }
        super(TaoBaoFour, self).__init__()

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
        # get
        kwargs = {
            "url": self.params.get("final_url"),
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
            if response.json.get("models"):
                return True
        return False

    def parse_response(self, response):
        """
        解析响应结果,获取所需字段
        :return:
        """
        result_list = []
        categoryone = self.params.get("categoryone")
        categorytwo = self.params.get("categorytwo")
        categorythree = self.params.get("categorythree")
        categoryfour = self.params.get("categoryfour")
        categoryfive = self.params.get("categoryfive")
        category_id = self.params.get("category_id")
        data = response.json()
        rest = data.get("models", {}).get("formValues", {}).get("selectProp")
        select_type = list(rest.keys())[0]
        select_name = rest.get(select_type).get("text")
        select_id = rest.get(select_type).get("value")
        result_list.append({
            "categoryone": categoryone,
            "categorytwo": categorytwo,
            "categorythree": categorythree,
            "categoryfour": categoryfour,
            "categoryfive": categoryfive,
            "category_id": category_id,
            "select_type": select_type,
            "select_name": select_name,
            "select_id": select_id,
            "callback": "TaoBaoFive"
        })
        self.params["result_list"] = result_list
        return self.params
