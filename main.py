import logging
import orderSelect
import orderRequest
import pandas as pd
import matching
from classDef import *

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s:%(name)s:%(asctime)s] %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')



if __name__=='__main__':

    main_logger = logging.getLogger("main")
    init = pd.read_csv("init.csv", encoding='utf-8', dtype=object)
    init = init.squeeze() #1차원화
    print(type(init.selectOrderDate))

    srcUrl = matching.getUrl(init['srcSelect'])
    main_logger.info("srcURL: {url}".format(url=str(srcUrl)))
    dstUrl = matching.getUrl(init['dstRequest'])
    main_logger.info("dstURL: {url}".format(url=str(dstUrl)))

    insSelect = Select(init)
    insRequest = Request(init)

    # 조회 후 연속적으로 주문 요청 여부 , 최적화 요청 여부
    insRequest.set_flag(True, False)

    rst = orderSelect.select(srcUrl, insSelect)
    #주문요청할 파일명
    filename = "orderAPI_" + str(insRequest.zoneSubject) + insSelect.selectOrderId + ".json"

    res = orderRequest.request(dstUrl, rst, insRequest, filename)


