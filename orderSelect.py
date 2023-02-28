import logging
import parsing as ps
import requests
import matching

sel_logger = logging.getLogger("orderSelect")


def select(url, insSelect):
    orderSelect = f'/api/V1/{insSelect.selectCntrId}/{insSelect.selectZoneId}/' \
                  f'select/order/{insSelect.selectOrderDate}/{insSelect.selectOrderId}'
    url = url + orderSelect
    sel_logger.info("select_url: {url}".format(url=str(url)))

    # jsonData = None
    payload = ""
    # headers 초기화
    headers = {"CertNum": matching.getKey(insSelect.srcSelect, insSelect.srcUser)}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        jsonData = response.json()
        rst = ps.parsing_select(jsonData, insSelect.zoneSubject)
        sel_logger.info("Type of Select Response: {rst}".format(rst=str(type(rst))))
        return rst
