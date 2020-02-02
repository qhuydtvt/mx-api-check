class ApiException(Exception):
  def __init__(self, url):
    Exception.__init__(self)
    self.url = url