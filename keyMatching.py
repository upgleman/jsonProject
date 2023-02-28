import logging

key_logger = logging.getLogger("keyMatching")

key_head = {
    'local' : {
        'test01':'f7c5e8c6f73b1bb2f0f3b357eed8c95f2b6b387e9dbb07915904ff8253dccc29'
    },
    'tb' : {
        'kttest01' : '8413b45848fc2e87d335fd88295b89ffe35cc646c095b0a75987ca138a226696',
        'lglmart001' : '99df1cb24cb9090ecdd05deb5351fea65f7661fc837eb17519d5478c72d08ca1'
    },
    'prd' : {
        'lglmart001' : '303944bb0bd0ffcebeb7f51e7a509e3cac543ffad711420eb6f135dc30ff8675'
    }
}

def getKey(base, user) :
    try :
        return key_head[base][user]
    except:
        key_logger.error("Key 없음")
        return

