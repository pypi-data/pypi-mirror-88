class NCMBAcl:
  def __init__(self):
    self.permissions = {
      '*': {
        'read': True,
        'write': True
      }
    }
  def set_public_read_access(self, bol):
    self.permissions['*']['read'] = bol
    return self
  def set_public_write_access(self, bol):
    self.permissions['*']['write'] = bol
    return self
  def set_user_read_access(self, user, bol):
    self.permissions[user.get('objectId')]['read'] = bol
    return self
  def set_user_write_access(self, user, bol):
    self.permissions[user.get('objectId')]['write'] = bol
    return self
  def set_role_read_access(self, role, bol):
    self.permissions[f'role:{role}']['read'] = bol
    return self
  def set_role_write_access(self, role, bol):
    self.permissions[f'role:{role}']['write'] = bol
    return self
  def to_json(self):
    res = {}
    for key in self.permissions:
      for acl in ['read', 'write']:
        if acl in self.permissions[key] and self.permissions[key][acl]:
          if key not in res:
            res[key] = {}
          res[key][acl] = True
    return res

