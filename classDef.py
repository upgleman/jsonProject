class Select(object):
    def __init__(self, init):
        self.srcSelect = init['srcSelect']
        self.srcUser = init['srcUser']
        self.selectCntrId = init['selectCntrId']
        self.selectZoneId = init['selectZoneId']
        self.selectOrderDate = init['selectOrderDate']
        self.selectOrderId = init['selectOrderId']
        self.zoneSubject = init['zoneSubject']


class Request(object):
    def __init__(self, init):
        self.dstRequest = init['dstRequest']
        self.dstUser = init['dstUser']
        self.requestCntrId = init['requestCntrId']
        self.requestZoneId = init['requestZoneId']
        self.requestOrderDate = init['requestOrderDate']
        self.zoneSubject = init['zoneSubject']
        self.seqFlag = False  #주문 정보 조회 후 연속적으로 주문 요청 여부
        self.optmFlag = False #최적화 요청 활성화 여부

    def set_flag(self, seqFlag, optmFlag):
        self.seqFlag = seqFlag
        self.optmFlag = optmFlag
