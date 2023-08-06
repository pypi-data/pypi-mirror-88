# -*- coding: utf-8 -*-
"""淘宝卖家商品类目，品牌属性信息"""
import json
import re
from urllib.parse import urlencode, quote
from wpt_taobaocategory.config.taobao_settings import cookie

class TaoBaoFive(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ZH-cn,zh;q=0.9",
            "cookie": cookie,
            "referer": "https://item.upload.taobao.com/router/publish.htm?spm=a211vu.server-web-home.favorite.d48.64f02D58WL0EGD",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "mozilla/5.0 (macintosH; intEl MAC OS X 10_15_7) apPleWebKit/537.36 (KHTMl, liKe geckO) chrome/87.0.4280.88 safari/537.36",
        }
        super(TaoBaoFive, self).__init__()

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
        category_id = self.params.get("category_id")
        cateid = self.params.get("select_id")
        catename = quote(self.params.get("select_name").encode("utf-8"))
        select_type = self.params.get("select_type")
        # part_url = urlencode(eval(json.dumps({
        #     "spm": "a211vu.server-web-home.favorite.d48.64f02d58Wl0EGD",
        #     "catId": "50009035",
        #     "keyProps": {select_type:{"value":cateid,"text":catename}},
        #     "newRouter": 1,
        #     "x-gpf-submit-trace-id": trace_id,
        # })))
        # get
        kwargs = {
            "url": 'https://item.publish.taobao.com/sell/publish.htm?spm=a211vu.server-web-home.favorite.d48.64f02d58Wl0EGD&catId={}&keyProps=%7B%22{}%22%3A%7B%22value%22%3A{}%2C%22text%22%3A%22{}%22%7D%7D&newRouter=1&x-gpf-submit-trace-id=0b5106e616076713506091352ec7d0'.format(category_id, select_type, catename, cateid),
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
            return True
        return False

    def parse_response(self, response):
        """
        解析响应结果,获取所需字段
        :return:
        """
        attr_dict = {}
        result_list = []
        categoryone = self.params.get("categoryone")
        categorytwo = self.params.get("categorytwo")
        categorythree = self.params.get("categorythree")
        categoryfour = self.params.get("categoryfour")
        categoryfive = self.params.get("categoryfive")
        data = re.search(r'window.Json =(.*?}}});', response.text, re.S).group(1)
        ret_data = json.loads(data)
        attr_list = ret_data.get("models", {}).get("catProp", {}).get("dataSource")
        for attr in attr_list:
            attr_name = attr.get("label")
            attr_vals = attr.get("dataSource")
            attr_value = ""
            if attr_vals:
                for val in attr_vals:
                    val_name = val.get("text")
                    attr_value += val_name + ","
            attr_dict[attr_name] = attr_value[:-1]

        result_list.append({
            "categoryone": categoryone,
            "categorytwo": categorytwo,
            "categorythree": categorythree,
            "categoryfour": categoryfour,
            "categoryfive": categoryfive,
            "property": attr_dict,
        })
        self.params["result_list"] = result_list
        return self.params
