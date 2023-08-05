import hmac
import hashlib
import base64
import NCMB.Client
import copy

class NCMBSignature:
  NCMB = None
  signatureMethodName = 'SignatureMethod'
  signatureMethodValue = 'HmacSHA256'
  signatureVersionName = 'SignatureVersion'
  signatureVersionValue = '2'

  @classmethod
  def create(self, method, time, class_name, queries = {}, objectId = None):
    ncmb = NCMBSignature.NCMB
    path = ncmb.path(class_name, objectId)
    queries = copy.copy(queries)
    queries[NCMBSignature.signatureMethodName] = NCMBSignature.signatureMethodValue
    queries[NCMBSignature.signatureVersionName] = NCMBSignature.signatureVersionValue
    queries[NCMB.Client.NCMB.applicationKeyName] = ncmb.applicationKey
    queries[NCMB.Client.NCMB.timestampName] = time
    encoded_queries = ncmb.encodeQuery(queries)
    string = "\n".join([method, ncmb.fqdn, path, encoded_queries])
    digest = hmac.new(ncmb.clientKey.encode('utf-8'), string.encode('utf-8'), hashlib.sha256).digest()
    return base64.b64encode(digest).decode('utf-8')
