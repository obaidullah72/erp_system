class BusinessError(Exception):
    def __init__(self, code, message, status=409):
        self.code, self.message, self.status = code, message, status
