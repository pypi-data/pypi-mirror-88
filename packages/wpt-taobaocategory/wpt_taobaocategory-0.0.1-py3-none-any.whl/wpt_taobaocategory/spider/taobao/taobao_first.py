# -*- coding: utf-8 -*-
"""淘宝卖家商品类目，获取第三级类目"""
from wpt_taobaocategory.config.taobao_settings import cookie

class TaoBaoOne(object):

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
        super(TaoBaoOne, self).__init__()

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
        # get
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
        categoryone = self.params.get("categoryone")
        categorytwo = self.params.get("categorytwo")
        data = response.json()
        catethree_list = data.get("data", {}).get("dataSource")
        for catethree in catethree_list:
            catethree_name = catethree.get("name")
            catethree_id = catethree.get("id")
            hasleaf = True if catethree.get("leaf") == False else False  # 是否有下一级分类
            final_url = None
            if hasleaf:
                callback = "TaoBaoTwo"
            else:
                final_url = "https://item.upload.taobao.com/router/" + catethree.get("action", {}).get("url")
                callback = "TaoBaoFour"
            result_list.append({
                "categoryone": categoryone,
                "categorytwo": categorytwo,
                "categorythree": catethree_name,
                "category_id": catethree_id,
                "final_url": final_url,
                "callback": callback
            })
        self.params["result_list"] = result_list
        return self.params
