import os
import logging
import json
import matching
import requests
import parsing as ps
import optm
import re

req_logger = logging.getLogger("orderRequest")


def req_function(dstUrl, insRequest, reqFile=None):
    orderRequest = f'/api/V1/{insRequest.requestCntrId}/{insRequest.requestZoneId}/' \
                   f'order/byitem/{insRequest.requestOrderDate}'
    url = dstUrl + orderRequest
    req_logger.info("request_url: {url}".format(url=str(url)))

    # jsonData = None
    if os.path.isfile(reqFile):
        with open(reqFile, 'r', encoding="utf-8") as f:
            req_logger.info("order request json file exist")
            payload = json.load(f)
            # json 문자열로 다시 전달
            payload = json.dumps(payload)
    else:
        req_logger.info("order request json Object exist")
        return

    # json.load(파일 객체) 함수는 딕션너리형으로 반환
    # 요청할때는 "json 문자열"로 전달할 필요하기 때문에 dumps로 사용필요
    req_logger.info("Type of request json dump: {data}".format(data=str(type(payload))))

    # headers setting
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    headers["CertNum"] = matching.getKey(insRequest.dstRequest, insRequest.dstUser)
    response = requests.request("POST", url, headers=headers, data=payload)
    req_logger.info("Response Code of orderRequest : " + str(response.status_code))

    if response.status_code == 200:
        jsonData = response.json()
        req_logger.info("Type of request Response: {rst}".format(rst=str(type(jsonData))))
        orderResData = ps.parsing_response(jsonData)
        orderId = orderResData[0]
        # 최적화 함수 요청 조건  TB 및 상용만
        if bool(re.findall(r'lodix', dstUrl)) & insRequest.optmFlag:
            req_logger.info("Only TB | PRD optimization request OK")
            optm.optm_request(dstUrl, insRequest, orderId)

        dispatchFile = "distPatchAPI_" + insRequest.zoneSubject + str(orderId) + ".json"

        if not os.path.isfile(dispatchFile):
            with open(dispatchFile, 'w', encoding="utf-8") as file:
                json.dump(orderResData[1], file, ensure_ascii=False, indent="\t")
                req_logger.info("Dispatch Json 파일 생성 완료")
    else:
        req_logger.info("Fail order request")
        return


def request(dstUrl, insRequest, filename):
    if insRequest.seqFlag:
        req_logger.info("Sequential Process : Select => Request")
        req_function(dstUrl, insRequest, filename)
    else:
        req_logger.debug("Don't progress the order request")

