import os
import logging
import json
import matching
import requests
import parsing as ps
import optm
import re

req_logger = logging.getLogger("orderRequest")


def req_function(dstUrl, insRequest, reqJson=None, reqFile=None):
    orderRequest = f'/api/V1/{insRequest.requestCntrId}/{insRequest.requestZoneId}/' \
                   f'order/byitem/{insRequest.requestOrderDate}'
    url = dstUrl + orderRequest
    req_logger.info("request_url: {url}".format(url=str(url)))

    # jsonData = None
    if os.path.isfile(reqFile) & (insRequest.seq==False):
        with open(reqFile, 'r', encoding="utf-8") as f:
            req_logger.info("order request json file exist")
            payload = json.load(f)
            # json 문자열로 다시 전달
            payload = json.dumps(payload)
    else:
        req_logger.info("order request json Object exist")
        payload = json.dumps(reqJson)
        # payload = reqJson

    # json.load(파일 객체) 함수는 딕션너리형으로 반환
    # req_logger.info("Type of request json: {data}".format(data=str(type(payload))))
    # 요청할때는 "json 문자열"로 전달할 필요하기 때문에 dumps로 사용필요
    req_logger.info("Type of request json dump: {data}".format(data=str(type(payload))))
    # payload = reqFile
    # print(payload)
    # headers 초기화
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    headers["CertNum"] = matching.getKey(insRequest.dstRequest, insRequest.dstUser)
    response = requests.request("POST", url, headers=headers, data=payload)

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


def request(dstUrl, reqJson, insRequest, filename):
    res = None
    # filename = "orderAPI_" + str(insRequest.zoneSubject) +  + ".json"

    if reqJson:
        # 초기화
        orderReq = {"zoneSubject": insRequest.zoneSubject}
        # 딕션너리 병합
        res = orderReq.update(reqJson)
        #자동화 자동 연동 모드
        if insRequest.seq:
            req_logger.info("Sequential Process : Select => Request")
            #orderReq로 zoneSubject 추가된 객체 넘김
            req_function(dstUrl, insRequest, orderReq, filename)

        # json 파일 생성, indent 옵션 : json 파일 정렬하기 위한 단위
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(orderReq, file, ensure_ascii=False, indent="\t")
            req_logger.info("Order Request Json 파일 생성 완료")
    else:
        req_logger.debug("order request Json Empty")
        req_function(dstUrl, insRequest, reqJson, filename)

    return res
