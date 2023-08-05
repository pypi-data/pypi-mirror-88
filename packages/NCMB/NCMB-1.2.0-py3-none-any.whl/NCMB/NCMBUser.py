from NCMB.NCMBObject import NCMBObject
from NCMB.NCMBRequest import NCMBRequest

class NCMBUser(NCMBObject):
  def __init__(self):
    super(NCMBUser, self).__init__('users')
  @classmethod
  def login(cls, user_name, password):
    req = NCMBRequest()
    queries = {
      'userName': user_name,
      'password': password
    }
    data = req.get('/login', queries)
    user = NCMBUser()
    user.sets(data)
    cls.NCMB.session_token = data['sessionToken']
    return user
