import json
import urllib.parse
from NCMB.NCMBObject import NCMBObject
from NCMB.NCMBRequest import NCMBRequest
from NCMB.NCMBSignature import NCMBSignature
from NCMB.NCMBQuery import NCMBQuery
from NCMB.NCMBAcl import NCMBAcl
from NCMB.NCMBUser import NCMBUser
from NCMB.NCMBGeoPoint import NCMBGeoPoint

class NCMB:
  fqdn = 'mbaas.api.nifcloud.com'
  version = '2013-09-01'
  applicationKeyName = 'X-NCMB-Application-Key'
  timestampName = 'X-NCMB-Timestamp'
  sessionTokenHeader = 'X-NCMB-Apps-Session-Token'
  
  def __init__(self, applicationKey, clientKey):
    self.applicationKey = applicationKey
    self.clientKey = clientKey
    self.session_token = None
    NCMBObject.NCMB = self
    NCMBRequest.NCMB = self
    NCMBSignature.NCMB = self
    NCMBQuery.NCMB = self
    NCMBUser.NCMB = self
    self.User = NCMBUser

  def Object(self, class_name):
    return NCMBObject(class_name)
  def Query(self, class_name):
    return NCMBQuery(class_name)
  def Acl(self):
    return NCMBAcl()
  def GeoPoint(self, lat, lng):
    return NCMBGeoPoint(lat, lng)
  def path(self, class_name, objectId):
    if class_name[0] == '/':
      return f'/{NCMB.version}{class_name}/{objectId or ""}'
    if class_name in ['installations', 'users', 'files', 'push']:
      return f'/{NCMB.version}/{class_name}/{objectId or ""}'
    return f'/{NCMB.version}/classes/{class_name}/{objectId or ""}'

  def encodeQuery(self, queries):
    encoded_queries = []
    for key in sorted(queries.items(), key=lambda x:x[0]):
      value = queries[key[0]]
      if value is None:
        continue
      if type(value) in (list, dict):
        value = json.dumps(value, separators=(',', ':'))
      safe = ":" if key[0] == 'X-NCMB-Timestamp' else ""
      if type(value) is int:
        encoded_queries.append(f'{key[0]}={value}')
      else:
        encoded_queries.append(f'{key[0]}={urllib.parse.quote(value, safe=safe)}')
    return '&'.join(encoded_queries)
  def url(self, class_name, queries, objectId):
    query = self.encodeQuery(queries)
    if query != "":
      query = f'?{query}'
    return f'https://{NCMB.fqdn}{self.path(class_name, objectId)}{query}'
