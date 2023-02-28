import logging
import json
import matching
import requests

optm_logger = logging.getLogger("optmRequest")


def optm_request(dstUrl, insRequest, orderId):
    optmRequest = f'/api/V1/{insRequest.requestCntrId}/{insRequest.requestZoneId}/' \
                  f'order/{insRequest.requestOrderDate}/{orderId}/request'
    url = dstUrl + optmRequest
    optionFile = "option.json"
    with open(optionFile, 'r', encoding='utf-8') as file:
        payload = json.load(file)
        payload = json.dumps(payload)
        optm_logger.info("Optimization Option read")

    headers = {'Content-Type': 'application/json; charset=utf-8',
               "CertNum": matching.getKey(insRequest.dstRequest, insRequest.dstUser)}

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        optm_logger.info("Complete Optimization Request")
