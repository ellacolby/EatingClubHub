from req_lib import ReqLib

def get_name(uid):
    req_lib = ReqLib()
    result = req_lib.getJSON('/users', uid=uid)
    return result[0]['displayname']
def get_email(uid):
    req_lib = ReqLib()
    result = req_lib.getJSON('/users', uid=uid)
    return result[0]['mail']
def get_all(uid):
    req_lib = ReqLib()
    result = req_lib.getJSON('/users', uid=uid)
    return result[0]

if __name__ == "__main__":
    uid = 'ec9834'
    user_info = get_all(uid)
    print(user_info)