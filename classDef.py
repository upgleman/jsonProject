class Select(object):
    def __init__(self, srcSelect, srcUser,
                 selectCntrId, selectZoneId, selectOrderDate, selectOrderId, zoneSubject):
        self.srcSelect = srcSelect
        self.srcUser = srcUser
        self.selectCntrId = selectCntrId
        self.selectZoneId = selectZoneId
        self.selectOrderDate = selectOrderDate
        self.selectOrderId = selectOrderId
        self.zoneSubject = zoneSubject


class Request(object):
    def __init__(self, dstRequest, dstUser, requestCntrId, requestZoneId, requestOrderDate, zoneSubject):
        self.dstRequest = dstRequest
        self.dstUser = dstUser
        self.requestCntrId = requestCntrId
        self.requestZoneId = requestZoneId
        self.requestOrderDate = requestOrderDate
        self.zoneSubject = zoneSubject
