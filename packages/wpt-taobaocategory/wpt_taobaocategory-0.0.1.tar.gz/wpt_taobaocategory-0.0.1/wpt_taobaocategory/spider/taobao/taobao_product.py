# -*- coding: utf-8 -*-
"""淘宝卖家类目生产者"""
from wpt_taobaocategory.config.taobao_settings import cookie

class TaoBaoProduct(object):

    def __init__(self, *args, **kwargs):
        self.params = {}
        self.start_url = "https://item.upload.taobao.com/router/asyncOpt.htm?optType=categorySelectChildren"
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
        super(TaoBaoProduct, self).__init__()

    def get_token(self):
        """
        获取渠道所需auth或cookie
        :return:
        """
        return ""

    def structure_params(self):
        """
        构造参数&请求url
        :param params: 请求需要的参数
        :return:
        """
        # get
        kwargs = {
            "url": self.start_url,
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
        data = response.json()
        cateone_list = data.get("data", {}).get("dataSource")
        for cateone in cateone_list:
            cateone_name = cateone.get("groupName")
            catetwo_list = cateone.get("children")
            for catetwo in catetwo_list:
                catetwo_name = catetwo.get("name")
                catetwo_id = catetwo.get("id")
                result_list.append({
                    "categoryone": cateone_name,
                    "categorytwo": catetwo_name,
                    "category_id": catetwo_id,
                    "callback": "TaoBaoOne"
                })
        self.params["result_list"] = result_list
        return self.params
