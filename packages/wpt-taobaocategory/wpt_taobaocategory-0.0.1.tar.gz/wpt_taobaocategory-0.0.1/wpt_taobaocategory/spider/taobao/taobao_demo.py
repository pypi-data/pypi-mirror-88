# -*- coding: utf-8 -*-

import requests
import re
import json
from urllib.parse import urlencode, quote

# cookie = "x-gpf-render-trace-id=2108222316076555880488779ebb06; miid=975864022015243912; cookie2=1079c41c8d76acb27a7a67976fb038b0; t=a0b26a4d7642f6284fa57489a51f67d9; _tb_token_=737765853339; _samesite_flag_=true; cna=E/xVGEEIlycCAXPuK4JcNGCr; lgc=%5Cu96F7%5Cu6653%5Cu660E12036815; dnk=%5Cu96F7%5Cu6653%5Cu660E12036815; tracknick=%5Cu96F7%5Cu6653%5Cu660E12036815; mt=ci=3_1; thw=cn; v=0; _m_h5_tk=3d4e04ffb112b3b834dd11137ba0c499_1607504342698; _m_h5_tk_enc=a259d806bf88e03860c62c32970110c9; enc=mOMDCBcw6B%2FwXzxD028BUmjm6dvuXQ5DLSN9d69NDUEVq4h0SPxYEw%2FNNRUJVhqHKGQ29VHzLioWBdg61UCuig%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; XSRF-TOKEN=61e307f0-b438-41e1-88c4-dda4d3addf1f; everywhere_tool_welcome=true; xlly_s=1; sgcookie=E100KsDGlrs0ncLkQ9xNhjzoZdxAKxPPYEozUW8%2FpQvRTvtwYz7m3cK5TRC7Ay5dsbdb3aGCIJSz4pUBz0WBc8Xzcg%3D%3D; unb=1813271788; uc1=pas=0&cookie21=VT5L2FSpccV6%2BGPAVCK7&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&cookie14=Uoe0al40Xzk%2F%2FA%3D%3D&existShop=true&cookie15=UtASsssmOIJ0bQ%3D%3D; uc3=lg2=VFC%2FuZ9ayeYq2g%3D%3D&vt3=F8dCuAJ2QhNPMUSawgc%3D&nk2=o8r%2FDYG%2BgOjQXMt9icI%3D&id2=UonaVttVU0q6Fg%3D%3D; csg=ed0dd048; cookie17=UonaVttVU0q6Fg%3D%3D; skt=fa23d3ffb6bc73a9; existShop=MTYwNzY1NTU4Nw%3D%3D; uc4=nk4=0%40oZyH2Xzde91z5JXvRhtAuW5nWmZO8aB0HA%3D%3D&id4=0%40UOEw6QqI0JvtOYx4BPLV4UvMUhTA; _cc_=WqG3DMC9EA%3D%3D; _l_g_=Ug%3D%3D; sg=588; _nk_=%5Cu96F7%5Cu6653%5Cu660E12036815; cookie1=U%2BbLxMI3XmJ%2FRLotRcdds8geV2Zq%2B6mwdoApxchyRo8%3D; tfstk=cSjPBjqceHfb9txQW3tERQH0RNnRZwIGvjJBrw9T-MZ0MKLliAcpnOPWuFOTmUf..; l=eBE05qwqODsJ58s9BOfwourza77OSIRAguPzaNbMiOCP_RC95OWhWZJqucLpC3GVhsGvR3-n_RoHBeYBcQAonxvtjVl8pJHmn; isg=BPj4EpeG04mOED8OLoi0GomByaCKYVzrLCAJYzJpRDPmTZg32nEsew5vAUV9HRTD"
cookie = "x-gpf-submit-trace-id=0b51064716075907291266909eb212; x-gpf-render-trace-id=210822f416076706347122530eae4e; miid=975864022015243912; cookie2=1079c41c8d76acb27a7a67976fb038b0; t=a0b26a4d7642f6284fa57489a51f67d9; _tb_token_=737765853339; _samesite_flag_=true; cna=E/xVGEEIlycCAXPuK4JcNGCr; lgc=%5Cu96F7%5Cu6653%5Cu660E12036815; dnk=%5Cu96F7%5Cu6653%5Cu660E12036815; tracknick=%5Cu96F7%5Cu6653%5Cu660E12036815; mt=ci=3_1; thw=cn; v=0; _m_h5_tk=3d4e04ffb112b3b834dd11137ba0c499_1607504342698; _m_h5_tk_enc=a259d806bf88e03860c62c32970110c9; enc=mOMDCBcw6B%2FwXzxD028BUmjm6dvuXQ5DLSN9d69NDUEVq4h0SPxYEw%2FNNRUJVhqHKGQ29VHzLioWBdg61UCuig%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; XSRF-TOKEN=61e307f0-b438-41e1-88c4-dda4d3addf1f; everywhere_tool_welcome=true; xlly_s=1; sgcookie=E100U%2F3hWYnVKCEpxY2SqTNY3KDFVN4tDHhVr6GcvEwLoRwSywBzW1CM3PkbUQK3SSM55df1pGVTe3vwDuH1rGmNWQ%3D%3D; unb=1813271788; uc1=existShop=true&cookie14=Uoe0al42IAXnPQ%3D%3D&pas=0&cookie21=VFC%2FuZ9aiKcVcS5M9%2B3X&cookie15=V32FPkk%2Fw0dUvg%3D%3D&cookie16=UIHiLt3xCS3yM2h4eKHS9lpEOw%3D%3D; uc3=id2=UonaVttVU0q6Fg%3D%3D&nk2=o8r%2FDYG%2BgOjQXMt9icI%3D&vt3=F8dCuAJ2QFA6P7BDpxo%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; csg=221266dd; cookie17=UonaVttVU0q6Fg%3D%3D; skt=79d8e5e9431d8be2; existShop=MTYwNzY3MDYzNA%3D%3D; uc4=nk4=0%40oZyH2Xzde91z5JXvRhtAuW5nWmZM1fb6Bg%3D%3D&id4=0%40UOEw6QqI0JvtOYx4BPLV4Umo2QnJ; _cc_=UIHiLt3xSw%3D%3D; _l_g_=Ug%3D%3D; sg=588; _nk_=%5Cu96F7%5Cu6653%5Cu660E12036815; cookie1=U%2BbLxMI3XmJ%2FRLotRcdds8geV2Zq%2B6mwdoApxchyRo8%3D; tfstk=ci7OB_YKIWhOooAdaGEnc62AXuvAaiEp3c9ok7-LbZii7mumus45raeNL5OSBeFd.; isg=BObmXcTthaI3EVEEzC5CwAt_N1poxyqBbu5n6dCOmomCU4dtOFOukfViq09feyKZ; l=eBE05qwqODsJ5Tg5BO5anurza77trIOb8sPzaNbMiIncC6CldJJTgvtQK6BPnCtRR8XAGQLB4HcaQD2tjUp37sDmndLhYEqB1xDDB"
traceid = "0b5106e616076713506091352ec7d0"

def get_categoryone():
    params = {}
    url = 'https://item.upload.taobao.com/router/asyncOpt.htm?optType=categorySelectChildren'
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ZH-cn,zh;q=0.9",
        "cookie":cookie,
        "referer": "https://item.upload.taobao.com/router/publish.htm?spm=a211vu.server-web-home.favorite.d48.64f02D58WL0EGD",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "mozilla/5.0 (macintosH; intEl MAC OS X 10_15_7) apPleWebKit/537.36 (KHTMl, liKe geckO) chrome/87.0.4280.88 safari/537.36",
        "x-requested-with": "XmlhTtprequest",
    }
    resp = requests.get(url, headers=headers, verify=False)
    print(resp.text)
    data = resp.json()
    cateone_list = data.get("data", {}).get("dataSource")
    for cateone in cateone_list:
        cateone_name = cateone.get("groupName")
        catetwo_list = cateone.get("children")
        for catetwo in catetwo_list:
            catetwo_name = catetwo.get("name")
            catetwo_id = catetwo.get("id")
            params.update({
                "categoryone": cateone_name,
                "categorytwo": catetwo_name,
                "catetwo_id": catetwo_id
            })
            print(params)


def get_categorythree(params):
    catethree_data = {}
    catid = params.get("catetwo_id")
    categoryone = params.get("categoryone")
    categorytwo = params.get("categorytwo")
    url = 'https://item.upload.taobao.com/router/asyncOpt.htm?optType=categorySelectChildren&catId={}'.format(catid)
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ZH-cn,zh;q=0.9",
        "cookie":cookie,
        "referer": "https://item.upload.taobao.com/router/publish.htm?spm=a211vu.server-web-home.favorite.d48.64f02D58WL0EGD",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "mozilla/5.0 (macintosH; intEl MAC OS X 10_15_7) apPleWebKit/537.36 (KHTMl, liKe geckO) chrome/87.0.4280.88 safari/537.36",
    }
    resp = requests.get(url, headers=headers, verify=False)
    print(resp.text)
    data = resp.json()
    catethree_list = data.get("data", {}).get("dataSource")
    for catethree in catethree_list:
        catethree_name = catethree.get("name")
        catethree_id = catethree.get("id")
        catethree_data.update({
            "categoryone": categoryone,
            "categorytwo": categorytwo,
            "categorythree": catethree_name,
            "catethree_id": catethree_id
        })
        print(catethree_data)


def get_categoryfour(params):
    catefour_data = {}
    catid = params.get("catethree_id")
    categoryone = params.get("categoryone")
    categorytwo = params.get("categorytwo")
    categorythree = params.get("categorythree")
    url = 'https://item.upload.taobao.com/router/asyncOpt.htm?optType=categorySelectChildren&catId={}'.format(catid)
    headers = {
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
    resp = requests.get(url, headers=headers, verify=False)
    print(resp.text)
    data = resp.json()
    catefour_list = data.get("data", {}).get("dataSource")
    for catefour in catefour_list:
        catefour_name = catefour.get("name")
        catefour_id = catefour.get("id")
        hasleaf = True if catefour.get("leaf") == False else False
        final_url = None
        is_end = False
        if hasleaf:
            pass
        else:
            is_end = True
            final_url = "https://item.upload.taobao.com/router/" + catefour.get("action", {}).get("url")
        catefour_data.update({
            "categoryone": categoryone,
            "categorytwo": categorytwo,
            "categorythree": categorythree,
            "categoryfour": catefour_name,
            "catefour_id": catefour_id,
            "is_end": is_end,
            "final_url": final_url
        })
        print(catefour_data)


def get_categoryfive(params):
    catefive_data = {}
    cateid = params.get("catefour_id")
    categoryone = params.get("categoryone")
    categorytwo = params.get("categorytwo")
    categorythree = params.get("categorythree")
    categoryfour = params.get("categoryfour")
    url = 'https://item.upload.taobao.com/router/asyncOpt.htm?optType=categorySelectChildren&catId={}'.format(cateid)
    headers = {
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
    resp = requests.get(url, headers=headers, verify=False)
    print(resp.text)
    data = resp.json()
    catefive_list = data.get("data", {}).get("dataSource")
    for catefive in catefive_list:
        catefive_name = catefive.get("name")
        catefive_id = catefive.get("id")
        hasleaf = True if catefive.get("leaf") == False else False
        final_url = None
        is_end = False
        if hasleaf:
            pass
        else:
            is_end = True
            final_url = "https://item.upload.taobao.com/router/" + catefive.get("action", {}).get("url")
        catefive_data.update({
            "categoryone": categoryone,
            "categorytwo": categorytwo,
            "categorythree": categorythree,
            "categoryfour": categoryfour,
            "categoryfive": catefive_name,
            "catefive_id": catefive_id,
            "is_end": is_end,
            "final_url": final_url
        })
        print(catefive_data)


def taobao_middle(params):
    middle_data = {}
    categoryone = params.get("categoryone")
    categorytwo = params.get("categorytwo")
    categorythree = params.get("categorythree")
    categoryfour = params.get("categoryfour")
    categoryfive = params.get("categoryfive")
    url = params.get("final_url")
    headers = {
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
    resp = requests.get(url, headers=headers, verify=False)
    print(resp.text)
    data = resp.json()
    rest = data.get("models", {}).get("formValues", {}).get("selectProp")
    select_type = list(rest.keys())[0]
    select_name = rest.get(select_type).get("text")
    select_id = rest.get(select_type).get("value")
    middle_data.update({
        "categoryone": categoryone,
        "categorytwo": categorytwo,
        "categorythree": categorythree,
        "categoryfour": categoryfour,
        "categoryfive": categoryfive,
        "select_type": select_type,
        "select_name": select_name,
        "select_id": select_id
    })
    print(middle_data)



def get_property(category_id, select_type, cateid, catename):
    attr_dict = {}
    start_url = "https://item.publish.taobao.com/sell/publish.htm?"
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "ZH-cn,zh;q=0.9",
        "cookie":cookie,
        "referer": "https://item.upload.taobao.com/",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "mozilla/5.0 (macintosH; intEl MAC OS X 10_15_7) apPleWebKit/537.36 (KHTMl, liKe geckO) chrome/87.0.4280.88 safari/537.36",
    }
    cate_name = quote(catename.encode("utf-8"))
    part_url = 'spm=a211vu.server-web-home.favorite.d48.64f02d58Wl0EGD&catId={}&keyProps=%7B%22{}%22%3A%7B%22value%22%3A{}%2C%22text%22%3A%22{}%22%7D%7D&newRouter=1&x-gpf-submit-trace-id=0b5106e616076713506091352ec7d0'.format(category_id, select_type, cate_name, cateid)
    # url = "https://item.publish.taobao.com/sell/publish.htm?spm=a211vu.server-web-home.favorite.d48.64f02d58Wl0EGD&catId=121454027&keyProps=%7B%22p-20000%22%3A%7B%22value%22%3A78094996%2C%22text%22%3A%22CASTUS%22%7D%7D&newRouter=1&x-gpf-submit-trace-id=0b5106e616076713506091352ec7d0"
    url = start_url + part_url
    print("url",url)
    resp = requests.get(url, headers=headers, verify=False)
    # print(resp.text)
    data = re.search(r'window.Json =(.*?}}});', resp.text, re.S).group(1)
    print("the_data----------->", data)
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

    print(attr_dict)


if __name__ == '__main__':
    # get_categoryone()
    params = {
        "categoryone": "母婴用品",
        "categorytwo": "奶粉/辅食/营养品/零食",
        "catetwo_id": "35",
        "categorythree": "宝宝零食",
        "catethree_id": "121404016",
        "categoryfour": "果肉条",
        "catefour_id": "121454027",
        "categoryfive": "CASTUS",
        "catefive_id": "78094996",
        "final_url": "https://item.upload.taobao.com/router/asyncOpt.htm?optType=selectProp&catId=121454027&kp-20000=78094996&kv-20000=CASTUS"
    }
    category_id = "121454027"
    select_type = "p-20000"
    catename = "78094996"
    cateid = "CASTUS"
    # get_categoryone()
    # get_categorythree(params)
    # get_categoryfour(params)
    # get_categoryfive(params)
    # taobao_middle(params)
    get_property(category_id, select_type, cateid, catename)