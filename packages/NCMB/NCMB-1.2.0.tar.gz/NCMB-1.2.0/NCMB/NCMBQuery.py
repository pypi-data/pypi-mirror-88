from NCMB.NCMBRequest import NCMBRequest

class NCMBQuery:
  NCMB = None
  def __init__(self, class_name):
    self.class_name = class_name
    self.queries = {
      'where': None,
      'limit': None,
      'skip': None,
      'order': None,
      'include': None
    }

  def equal_to(self, key, value):
    return self.set_operand(key, value)
  def greater_than_or_equal_to(self, key, value):
    return self.set_operand(key, value, '$gte')
  def not_equal_to(self, key, value):
    return self.set_operand(key, value, '$ne')
  def less_than(self, key, value):
    return self.set_operand(key, value, '$lt')
  def less_than_or_equal_to(self, key, value):
    return self.set_operand(key, value, '$lte')
  def greater_than(self, key, value):
    return self.set_operand(key, value, '$gt')
  def in_value(self, key, values):
    return self.set_operand(key, values, '$in')
  def not_in(self, key, values):
    return self.set_operand(key, values, '$nin')
  def exists(self, key, exist = True):
    return self.set_operand(key, exist, '$exists')
  def regular_expression_to(self, key, regex):
    return self.set_operand(key, regex, '$regex')
  def in_array(self, key, values):
    if type(values) is not list:
      values = [values]
    return self.set_operand(key, values, '$inArray')
  def not_in_array(self, key, values):
    if type(values) is not list:
      values = [values]
    return self.set_operand(key, values, '$ninArray')
  def all_in_array(self, key, values):
    if type(values) is not list:
      values = [values]
    return self.set_operand(key, values, '$all')
  def order(self, field, desc = True):
    symbol = '-' if desc == True else ''
    if self.queries['order'] is None:
      self.queries['order'] = f'{symbol}{field}'
    else:
      self.queries['order'] = f'{self.queries["order"]},{symbol}{field}'
    return self
  def limit(self, number):
    if type(number) is not int:
      raise Exception('Limit accepts only number.')
    if number < 1 or number > 1000:
      raise Exception('Limit must be renge of 1~1000.')
    self.queries['limit'] = number
    return self
  def skip(self, number):
    if type(number) is not int:
      raise Exception('Limit accepts only number.')
    self.queries['skip'] = number
    return self
  """
  near(key: string, location: NCMBGeoPoint): NCMBQuery {
    return self.set_operand(key, location.toJSON(), '$nearSphere')
  }

  withinKilometers(key: string, location: NCMBGeoPoint, maxDistance: number): NCMBQuery {
    self.set_operand(key, maxDistance, '$maxDistanceInKilometers')
    self.set_operand(key, location.toJSON(), '$nearSphere')
    return this
  }

  withinMiles(key: string, location: NCMBGeoPoint, maxDistance: number): NCMBQuery {
    self.set_operand(key, maxDistance, '$maxDistanceInMiles')
    self.set_operand(key, location.toJSON(), '$nearSphere')
    return this
  }

  withinRadians(key: string, location: NCMBGeoPoint, maxDistance: number): NCMBQuery {
    self.set_operand(key, maxDistance, '$maxDistanceInRadians')
    self.set_operand(key, location.toJSON(), '$nearSphere')
    return this
  }

  withinSquare(key: string, southWestVertex: NCMBGeoPoint, northEastVertex: NCMBGeoPoint): NCMBQuery {
    var box = {
      '$box':[
        southWestVertex.toJSON(),
        northEastVertex.toJSON()
      ]
    }
    return self.set_operand(key, box, '$within')
  }
  """

  def set_operand(self, key, value, ope = None):
    if self.queries['where'] is None:
      self.queries['where'] = {}
    if ope is None:
      self.queries['where'][key] = value
      return self
    if key not in self.queries['where']:
      self.queries['where'][key] = {}
    self.queries['where'][key][ope] = value
    return self

  def fetch_all(self):
    req = NCMBRequest()
    ary = req.get(self.class_name, self.queries)
    results = []
    for params in ary['results']:
      o = NCMBQuery.NCMB.Object(self.class_name)
      o.sets(params)
      results.append(o)
    return results
