class ApiException(Exception):
  def __init__(self, url, message=''):
    Exception.__init__(self)
    self.url = url
    self.message = message
  
  def __str__(self):
    return self.message