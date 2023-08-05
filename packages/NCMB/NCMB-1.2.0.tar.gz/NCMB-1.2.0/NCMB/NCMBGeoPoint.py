class NCMBGeoPoint:
  def __init__(self, lat, lng):
    self.lat = lat
    self.lng = lng
  def to_json(self):
    return {
      '__type': 'GeoPoint',
      'latitude': self.lat,
      'longitude': self.lng
    }
