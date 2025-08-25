class MenuNotFoundException(Exception):
    def __init__(self, message="메뉴를 찾을 수 없습니다."):
        self.message = message
        super().__init__(self.message)

class MenuOptionNotFoundException(Exception):
    def __init__(self, message="메뉴 옵션을 찾을 수 없습니다."):
        self.message = message
        super().__init__(self.message)

class MenuValidationException(Exception):
    def __init__(self, message="메뉴 데이터가 유효하지 않습니다."):
        self.message = message
        super().__init__(self.message) 