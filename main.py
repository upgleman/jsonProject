import logging
import orderSelect
import orderRequest
from classDef import *


logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s:%(name)s:%(asctime)s] %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

# logger = logging.getLogger("Main")
# stream_handler = logging.StreamHandler()
# logger.addHandler(stream_handler)

url_dict = {
    'local':'http://localhost:8092',
    'tb':'https://devopenapilgl.lodix.co.kr',
    'prd':'https://openapilgl.lodix.co.kr'
}

if __name__=='__main__':
    #주문조회 받기 => Source 정하기
    #주문 생성 하기 => Target 정하기
    main_logger = logging.getLogger("main")

    srcSelect = 'prd'
    srcUser = 'lglmart002'

    selectCntrId='0000000260'
    # zoneId='0000000468'
    # orderId = '000000023980'
    selectOrderDate='20230224'
    selectZoneId='0000000469'
    selectOrderId = '000000023981'
    zoneSubject= "01회차 (온라인)"

    # zoneId='0000000470'
    # orderId = '000000023982'
    dstRequest = 'tb'
    dstUser = 'kttest01'
    requestCntrId = '0000000078'
    requestZoneId = '0000001741'
    requestOrderDate = '20230227'

    #호출
    srcUrl = url_dict.get(srcSelect)
    dstUrl = url_dict.get(dstRequest)

    insSelect = Select(srcSelect, srcUser,selectCntrId, selectZoneId, selectOrderDate, selectOrderId, zoneSubject)
    insRequest = Request(dstRequest, dstUser, requestCntrId, requestZoneId, requestOrderDate, zoneSubject)

    main_logger.info("srcURL: {url}".format(url=str(srcUrl)))
    rst = orderSelect.select(srcUrl,insSelect)

    main_logger.info("dstURL: {url}".format(url=str(dstUrl)))
    res = orderRequest.request(dstUrl, rst, insRequest)
    # print(res)


