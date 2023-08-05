from NCMB.NCMBRequest import NCMBRequest

class NCMBObject:
  NCMB = None
  def __init__(self, class_name):
    self.class_name = class_name
    self.fields = {}
  def get(self, key):
    if key in self.fields.keys():
      return self.fields[key]
    else:
      return None
  def set(self, key, value):
    self.fields[key] = value
    return self
  def sets(self, data):
    for k in data:
      self.set(k, data[k])
  def save(self):
    req = NCMBRequest()
    if 'objectId' in self.fields.keys():
      # Update current object
      d = req.put(self.class_name, self.fields, self.fields['objectId'])
    else:
      # Create new object
      d = req.post(self.class_name, self.fields)
    self.sets(d)
  def to_json(self):
    if self.get('objectId') == None:
      self.save()
    return {
      '__type': 'Pointer',
      'className': self.class_name,
      'objectId': self.get('objectId')
    }
