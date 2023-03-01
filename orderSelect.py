import logging
import parsing as ps
import requests
import matching
import json

sel_logger = logging.getLogger("orderSelect")


def select(url, insSelect, filename):
    orderReq = None

    orderSelect = f'/api/V1/{insSelect.selectCntrId}/{insSelect.selectZoneId}/' \
                  f'select/order/{insSelect.selectOrderDate}/{insSelect.selectOrderId}'
    url = url + orderSelect
    sel_logger.info("select_url: {url}".format(url=str(url)))

    # jsonData = None
    payload = ""
    # headers 초기화
    headers = {"CertNum": matching.getKey(insSelect.srcSelect, insSelect.srcUser)}

    response = requests.request("GET", url, headers=headers, data=payload)
    sel_logger.info("Response Code of orderSelect : " + str(response.status_code))

    if response.status_code == 200:
        jsonData = response.json()
        rst = ps.parsing_select(jsonData, insSelect.zoneSubject)
        sel_logger.info("Type of Select Response: {rst}".format(rst=str(type(rst))))

        if rst:
            orderReq = {"zoneSubject": insSelect.zoneSubject}
            # 딕션너리 병합
            res = orderReq.update(rst)
            # json 파일 생성, indent 옵션 : json 파일 정렬하기 위한 단위
            with open(filename, 'w', encoding="utf-8") as file:
                json.dump(orderReq, file, ensure_ascii=False, indent="\t")
                sel_logger.info("Order Request Json 파일 생성 완료")
            return orderReq
    else:
        sel_logger.info("Fail orderSelect")
        return orderReq
