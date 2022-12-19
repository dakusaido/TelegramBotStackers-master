class Helper:
    message = 0

    def __init__(self, msg):
        self.message = msg

    def rename_msg(self, msg):
        self.message = msg

    def get_msg(self):
        return self.message
