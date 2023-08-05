import datetime
import copy
import json
import urllib.request
from NCMB.NCMBSignature import NCMBSignature
import NCMB.NCMBObject
import NCMB.Client

class NCMBRequest:
  NCMB = None
  def post(self, class_name, data):
    # Create data
    return self.exec("POST", class_name, {}, data)
  def put(self, class_name, data, objectId):
    # Update data
    return self.exec("PUT", class_name, {}, data, objectId)
  def get(self, class_name, queries, objectId = None):
    # Retribute data
    return self.exec("GET", class_name, queries, {}, objectId)
  def exec(self, method, class_name, queries, data, objectId = None):
    time = datetime.datetime.now().isoformat()
    # Generate signature
    sig = NCMBSignature.create(method, time, class_name, queries, objectId)
    headers = {
      'X-NCMB-Signature': sig,
      'Content-Type': 'application/json'
    }
    headers[NCMB.Client.NCMB.applicationKeyName] = self.NCMB.applicationKey
    headers[NCMB.Client.NCMB.timestampName] = time
    if self.NCMB.session_token is not None:
      headers[NCMB.Client.NCMB.sessionTokenHeader] = self.NCMB.session_token
    url = self.NCMB.url(class_name, queries, objectId)
    res = self.fetch(method, url, headers, data)
    if 'code' in res:
      raise Exception(res.error)
    if method == 'DELETE' and res == '':
      return {}
    return res
  def data(self, data):
    data = copy.copy(data)
    for key in ['createData', 'updateDate', 'objectId']:
      if key in data.keys():
        data.pop(key)
    for key in data.keys():
      if type(data[key]) in [datetime.datetime, datetime.date]:
        data[key] = {
          '__type': 'Date',
          'iso': data[key].strftime('%Y-%m-%dT%H:%M:%S.%fZ').replace('000Z', 'Z')
        }
      if 'to_json' in dir(data[key]):
        data[key] = data[key].to_json()
    return data
  def fetch(self, method, url, headers, data):
    if method in ['POST', 'PUT']:
      data = self.data(data)
      print(data)
    try:
      req = urllib.request.Request(url, data=json.dumps(data, separators=(',', ':')).encode(), method=method, headers=headers)
      with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
      return json.loads(e.read())
