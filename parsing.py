import logging
import re

parsing_logger = logging.getLogger("parsing")


def parsing_select(res, zoneSubject):
    data = res['data']  # 딕션너리
    data2 = res['data']['orderDetl']  # 리스트
    parsing_logger.info("['orderDetl']: {data2}".format(data2=str(type(data2))))

    znName = re.search(r'\w+', zoneSubject)
    parsing_logger.info("Dest Name Infix : {znName}".format(znName=znName.group()))

    cnt = 0
    for dic in data2:
        del (dic['orderDetlId'])  # orderDetlId 삭제
        del (dic['destId'])  # destId 삭제
        dic['destNm'] = "dest" + str(znName.group()) + str(cnt)
        for item in dic['orderItem']:
            del (item['orderDetlItemId'])  # orderDetlItemId 삭제
        cnt += 1

    return data


def parsing_response(res):
    cndShipEarl = "50"
    cndShipLate = "50"
    cndSlaPerc = "50"
    dispatch = {
        "cndShipEarl": cndShipEarl,
        "cndShipLate": cndShipLate,
        "cndSlaPerc": cndSlaPerc
    }

    orderData = res['data']
    orderId = orderData['orderId']
    orderDetlData = res['data']['orderDetl']
    #     print(orderId)
    for orderDetl in orderDetlData:
        del (orderDetl['orderDetltem'])
        orderDetl['firstOrderNum'] = orderDetl["orderDetlId"]
        #뒷자리 다르게 보이기 위함
        lastOrderNum = int(orderDetl["orderDetlId"]) + 1111
        orderDetl['lastOrderNum'] = '{0:012d}'.format(lastOrderNum)

    del (orderData['orderId'])
    dispatch.update(orderData)
    parsing_logger.info("Complete parsing the order Response Data")

    return orderId, dispatch
