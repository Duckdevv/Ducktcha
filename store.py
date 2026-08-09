import time


class MemoryStore:

  def __init__(self, expiry=120):
    self.expiry = expiry
    self.data = {}

  def clean(self):
    now = time.time()
    expired = [k for k, v in self.data.items() if now - v['time'] > self.expiry]
    for key in expired:
      del self.data[key]

  def save(self, token, code):
    self.clean()
    self.data[token] = {'code': code.upper(), 'time': time.time()}

  def validate(self, token, user_input):
    self.clean()
    if token not in self.data:
      return False

    real_code = self.data[token]['code']
    del self.data[token]

    return user_input.strip().upper() == real_code
